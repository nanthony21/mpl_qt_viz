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
from cycler import cycler
from matplotlib.image import AxesImage
from matplotlib.patches import Rectangle, Polygon
from shapely.geometry import Polygon as shapelyPolygon, LinearRing, MultiPolygon
import shapely
from ._segmentation import segmentOtsu
from ._base import CreatorWidgetBase

if typing.TYPE_CHECKING:
    from matplotlib.axes import Axes


class RegionalPaintCreator(CreatorWidgetBase):
    """A widget allowing the user to select a rectangular region with a bright region in it such as a fluorescent
    nucleus. Otsu thresholding will then be used to draw an ROI on the bright region.

     Args:
        ax: A reference to the matplotlib `Axes` that this selector widget is active on.
        image: A reference to a matplotlib `AxesImage`. Selectors may use this reference to get information such as data values from the image
            for computer vision related tasks.
        onselect: A callback function that will be called when the selector finishes a selection.

     """
    def __init__(self, ax: Axes, im: AxesImage, onselect=None):
        super().__init__(ax, im)
        self.onselect = onselect
        self.started = False
        self.selectionTime = False
        self.contours = []
        self.box = Rectangle((0, 0), 0, 0, facecolor=(1, 0, 1, 0.01), edgecolor=(0, 0, 1, 0.4), animated=True)
        self.addArtist(self.box)

    @staticmethod
    def getHelpText():
        return "Click and drag to select a rectangular region to search for objects. Then click the object you would like to select."

    def reset(self):
        """Reset the state of the selector so it's ready for a new selection."""
        self.started = False
        [self.removeArtist(i) for i in self.contours]
        self.contours = []
        self.selectionTime = False
        self.updateAxes()

    def findContours(self, rect: Rectangle):
        """Detect bright regions within the specified rectangle and draw them.

        Args:
            rect: A matplotlib `Rectangle` used to specify the search region of the image for bright regions.
        """
        x, y = rect.xy
        x = int(x)
        y = int(y)
        x2 = int(x + rect.get_width())
        y2 = int(y + rect.get_height())
        xslice = slice(x, x2+1) if x2 > x else slice(x2, x+1)
        yslice = slice(y, y2+1) if y2 > y else slice(y2, y+1)
        image = self.image.get_array()[(yslice, xslice)]
        polys = segmentOtsu(image)
        for i in range(len(polys)):
            polys[i] = shapely.affinity.translate(polys[i], xslice.start, yslice.start)  # Apply offset so that coordinates are globally correct.
            polys[i] = polys[i].simplify(3)  # Simplify the polygon a little bit for much faster saving.
        self._drawRois(polys)

    def _drawRois(self, polys: typing.List[shapelyPolygon]):
        """Draw ROIs detected by `findContours."""
        if len(polys) > 0:
            alpha = 0.3
            colorCycler = cycler(color=[(1, 0, 0, alpha), (0, 1, 0, alpha), (0, 0, 1, alpha), (1, 1, 0, alpha), (1, 0, 1, alpha)])
            for poly, color in zip(polys, colorCycler()):
                if isinstance(poly, MultiPolygon):  # There is a chance for this a Multipolygon rather than just a Polygon.
                    poly = max(poly, key=lambda a: a.area)  # To fix this we extract the largest polygon from the multipolygon
                p = Polygon(poly.exterior.coords, color=color['color'], animated=True)
                self.addArtist(p)
                self.contours.append(p)
            self.updateAxes()

    def _press(self, event):
        if event.button == 1:  # Left Click
            if not self.started and not self.selectionTime:
                self.started = True
                self.box.set_visible(True)
                self.box.set_xy((event.xdata, event.ydata))
            elif self.selectionTime:
                coord = (event.xdata, event.ydata)
                for artist in self.contours:
                    assert isinstance(artist, Polygon)
                    if artist.get_path().contains_point(coord):
                        l = shapelyPolygon(LinearRing(artist.xy))
                        l = l.simplify(l.length / 100, preserve_topology=False)
                        if isinstance(l, MultiPolygon):# There is a chance for this to convert a Polygon to a Multipolygon.
                            l = max(l, key=lambda a: a.area) #To fix this we extract the largest polygon from the multipolygon
                        handles = l.exterior.coords
                        self.onselect(artist.xy, handles)
                        break
                self.reset()

    def _ondrag(self, event):
        if self.started and event.button == 1:
            x, y = self.box.xy
            dx = event.xdata - x
            dy = event.ydata - y
            self.box.set_width(dx)
            self.box.set_height(dy)
            self.updateAxes()

    def _release(self, event):
        if event.button == 1 and self.started:
            self.findContours(self.box)
            self.selectionTime = True
            self.started = False

