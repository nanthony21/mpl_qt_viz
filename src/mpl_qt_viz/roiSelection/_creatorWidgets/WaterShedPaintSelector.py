# Copyright 2018-2021 Nick Anthony, Backman Biophotonics Lab, Northwestern University
#
# This file is part of mpl_qt_viz.
#
# mpl_qt_viz is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# mpl_qt_viz is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with mpl_qt_viz.  If not, see <https://www.gnu.org/licenses/>.

from __future__ import annotations
import logging
import typing
from PyQt5 import QtCore
from PyQt5.QtCore import QPoint
from PyQt5.QtWidgets import QDialog, QWidget, QPushButton, QFormLayout
from cycler import cycler
from matplotlib.image import AxesImage
from shapely.geometry import Polygon as shapelyPolygon, LinearRing, MultiPolygon
from matplotlib.patches import Polygon

from mpl_qt_viz.roiSelection._creatorWidgets._segmentation import segmentWatershed
from mpl_qt_viz.roiSelection._creatorWidgets._sharedWidgets import LabeledSlider
from mpl_qt_viz.roiSelection._creatorWidgets._base import CreatorWidgetBase

if typing.TYPE_CHECKING:
    from matplotlib.axes import Axes


class WaterShedPaintCreator(CreatorWidgetBase):
    """Uses Watershed technique in an attempt to highlight all bright selectable regions in a fluorescence image.

    Args:
        ax: The matplotlib `Axes` that you want to interact with.
        im: A reference to a matplotlib `AxesImage`. The data from this object is used to detect bright regions.
        onselect: A callback that will be called when the user hits 'enter'. Should have signature (polygonCoords, sparseHandleCoords).
    """
    def __init__(self, ax: Axes, im: AxesImage, onselect=None):
        super().__init__(ax, im, onselect=onselect)
        self.dlg = WaterShedPaintDialog(self, self.ax.figure.canvas)

        self._cachedRegions = None  # We cache the detected polygons. No need to redetect if nothing has changed between selections.
        self._cachedImage = None  # We cache a reference to the image data as a way of detecting when the image data has changed.

        self._checkImageChangeTimer = QtCore.QTimer()  # This timer checks if the image data has been changed. If it has then redetect regions.
        self._checkImageChangeTimer.setInterval(1000)
        self._checkImageChangeTimer.setSingleShot(False)
        self._checkImageChangeTimer.timeout.connect(lambda: self.paint(forceRedraw=False))
        self._checkImageChangeTimer.start()

    def __del__(self):
        self._checkImageChangeTimer.stop()

    @staticmethod
    def getHelpText():
        return "Segment a full image using Watershed techniques."

    def reset(self):
        """Reset the state of the selector so it's ready for a new selection."""
        self.removeArtists()
        self.updateAxes()

    def set_active(self, active: bool):
        super().set_active(active)
        if active:
            self.dlg.show()
            # Move dialog to the side
            rect = self.dlg.geometry()
            parentRect = self.ax.figure.canvas.geometry()
            rect.moveTo(self.ax.figure.canvas.mapToGlobal(QPoint(parentRect.x() - rect.width(), parentRect.y())))
            self.dlg.setGeometry(rect)
            self.paint()
        else:
            self.dlg.close()

    def _drawRois(self, polys: typing.List[shapelyPolygon]):
        """Convert a list of shapely `Polygon` objects into matplotlib `Polygon`s and display them."""
        self._cachedRegions = polys
        if len(polys) > 0:
            alpha = 0.3
            colorCycler = cycler(color=[(1, 0, 0, alpha), (0, 1, 0, alpha), (0, 0, 1, alpha), (1, 1, 0, alpha), (1, 0, 1, alpha)])
            for poly, color in zip(polys, colorCycler()):
                if isinstance(poly, MultiPolygon):
                    logging.getLogger(__name__).error("FullImPaintSelector.drawRois tried to draw a polygon of a shapely.MultiPolygon object.")
                    continue
                p = Polygon(poly.exterior.coords, color=color['color'], animated=True)
                self.addArtist(p)

    def _press(self, event):
        """If a displayed polygon is clicked on then execute the `onselect` callback."""
        if event.button == 1 and self.onselect is not None:  # Left Click
            coord = (event.xdata, event.ydata)
            for artist in self._artists:
                assert isinstance(artist, Polygon)
                if artist.get_path().contains_point(coord):
                    l = shapelyPolygon(LinearRing(artist.xy))
                    l = l.simplify(l.length / 2e2, preserve_topology=False)
                    if isinstance(l, MultiPolygon):  # There is a chance for this to convert a Polygon to a Multipolygon.
                        l = max(l, key=lambda a: a.area)  # To fix this we extract the largest polygon from the multipolygon
                    handles = l.exterior.coords
                    self.onselect(artist.xy, handles)
                    break

    def paint(self, forceRedraw: bool = True):
        """Refresh the detected regions.

        Args:
            forceRedraw: If `True` then polygons will be cleared and redrawn even if we don't detect that our status is `stale`
        """
        if not self.get_active():
            return  # Sometimes we instantiate the class but don't have it active. avoid drawing stuff.
        stale = False
        if self.image.get_array() is not self._cachedImage:  # The image has been changed.
            self._cachedImage = self.image.get_array()
            stale = True
        if self.dlg.isStale():
            stale = True
        if stale:
            try:
                polys = segmentWatershed(self.image.get_array(), **self.dlg.getSettings())
            except Exception as e:
                logging.getLogger(__name__).warning(f"adaptive segmentation failed with error:")
                logging.getLogger(__name__).exception(e)
                return
        else:
            if forceRedraw:
                polys = self._cachedRegions
            else:
                return
        self.removeArtists()
        self._drawRois(polys)
        self.updateAxes()


class WaterShedPaintDialog(QDialog):
    """The dialog used by the FullImPaintSelector. Can adjust detection parameters.

    Args:
        parentSelector: A reference the the `FullImPaintSelector` that is being used with this dialog.
        parent: A QWidget to serve as the Qt parent for this QWidget.
    """
    def __init__(self, parentSelector: WaterShedPaintCreator, parent: QWidget):
        super().__init__(parent=parent)
        self.setWindowFlags(QtCore.Qt.Window | QtCore.Qt.WindowTitleHint | QtCore.Qt.CustomizeWindowHint) #Get rid of the close button. this is handled by the selector widget active status
        self.parentSelector = parentSelector
        self.setWindowTitle("Watershed Painter")

        self._stale = True  # Keeps track of if the settings have changed.

        self._paintDebounce = QtCore.QTimer()  # This timer prevents the selectionChanged signal from firing too rapidly.
        self._paintDebounce.setInterval(200)
        self._paintDebounce.setSingleShot(True)
        self._paintDebounce.timeout.connect(self.parentSelector.paint)

        def _valChanged():
            """When a setting is changed it should call this to schedule a repaint."""
            self._stale = True
            self._paintDebounce.start()

        self.closingSlider = LabeledSlider(0, 50, 1, 10, self)
        self.closingSlider.valueChanged.connect(_valChanged)

        self.openingSlider = LabeledSlider(0, self.closingSlider.value(), 1, 10, self)
        self.openingSlider.valueChanged.connect(_valChanged)

        self.minAreaSlider = LabeledSlider(5, 300, 1, 100, self)
        self.minAreaSlider.valueChanged.connect(_valChanged)

        self.refreshButton = QPushButton("Refresh", self)
        def refreshAction():
            self._stale = True  # Force a full refresh
            self.parentSelector.paint()
        self.refreshButton.released.connect(refreshAction)

        self.closingSlider.setToolTip("The number of pixels that the polygons should be binary closed by.")
        self.openingSlider.setToolTip("The number of pixels that the polygons should be binary opened by.")
        self.minAreaSlider.setToolTip("Detected regions with a pixel area lower than this value will be discarded.")

        l = QFormLayout()
        l.addRow("Closing (px):", self.closingSlider)
        l.addRow("Opening (px):", self.openingSlider)
        l.addRow("Minimum Area (px):", self.minAreaSlider)
        l.addRow(self.refreshButton)
        self.setLayout(l)

    def isStale(self):
        """Returns if True if the settings have changed since the last time `getSettings` was called."""
        return self._stale

    def getSettings(self) -> dict:
        self._stale = False
        return dict(
            closingRadius=self.closingSlider.value(), openingRadius=self.openingSlider.value(),
            minimumArea=self.minAreaSlider.value()
        )


if __name__ == '__main__':
    import matplotlib.pyplot as plt
    import numpy as np
    from PyQt5.QtWidgets import QApplication

    app = QApplication([])

    size = 1000

    im = np.ones((size, size))
    x = y = np.linspace(0, 1, num=size)
    X, Y = np.meshgrid(x, y)
    im = im * np.sin(20*X) * np.sin(20*Y)

    fig, ax = plt.subplots()
    im = ax.imshow(im, cmap='gray')
    sel = WaterShedPaintCreator(ax, im, onselect=lambda verts, handles: print("excellent choice!"))
    fig.show()
    plt.pause(.1)
    sel.set_active(True)
    plt.show()

    app.exec()

    a = 1