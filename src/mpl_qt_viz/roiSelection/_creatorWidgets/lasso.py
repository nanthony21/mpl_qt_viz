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
import typing
from matplotlib.image import AxesImage
from matplotlib.patches import Polygon
from shapely.geometry import Polygon as shapelyPolygon, LinearRing, MultiPolygon
from mpl_qt_viz.roiSelection._creatorWidgets._base import CreatorWidgetBase

if typing.TYPE_CHECKING:
    from matplotlib.axes import Axes


class LassoCreator(CreatorWidgetBase):
    """Allows the user to select a region with freehand drawing.

    Args:
        ax: A reference to the matplotlib `Axes` that this selector widget is active on.
        image: A reference to a matplotlib `AxesImage`. Selectors may use this reference to get information such as data values from the image
            for computer vision related tasks.
        onselect: A callback function that will be called when the selector finishes a selection.
    """
    def __init__(self, ax: Axes, image: AxesImage, onselect=None):
        super().__init__(ax, image)
        self.onselect = onselect
        self.verts = None
        self.polygon = Polygon([[0, 0]], facecolor=(0, 0, 1, .1), animated=True, edgecolor=(0, 0, 1, .8))
        self.polygon.set_visible(False)
        self.addArtist(self.polygon)
#        self.set_active(True) #needed for blitting to work

    @staticmethod
    def getHelpText():
        return "Click and drag to draw a freehand shape."

    def reset(self):
        self.verts = None
        self.polygon.set_visible(False)

    def _press(self, event):
        self.verts = [(event.xdata, event.ydata)]

    def _release(self, event):
        if event.button == 1: #Left click
            if (self.verts is not None) and (self.onselect is not None):
                try:
                    l = shapelyPolygon(LinearRing(self.verts))
                except ValueError:
                    return  # If the user clicks without dragging there will just be a single coordinate, this will result in an error when trying to convert to a `LinearRing`
                l = l.buffer(0)
                l = l.simplify(l.length ** .5 / 5, preserve_topology=False)
                if isinstance(l, MultiPolygon):  # There is a chance for this to be a Multipolygon.
                    l = max(l, key=lambda a: a.area)  # To fix this we extract the largest polygon from the multipolygon
                handles = l.exterior.coords
                self.onselect(self.verts, handles)

    def _ondrag(self, event):
        if self.verts is None:
            return
        self.verts.append((event.xdata, event.ydata))
        self.polygon.set_xy(self.verts)
        self.updateAxes()

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
    sel = LassoCreator(ax, im, onselect=lambda verts, handles: print("excellent choice!"))
    fig.show()
    plt.pause(.1)
    sel.set_active(True)
    plt.show()

    app.exec()

    a = 1