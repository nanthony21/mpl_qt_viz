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
from matplotlib.patches import Circle
from ._base import CreatorWidgetBase
import typing as t_
if typing.TYPE_CHECKING:
    from matplotlib.axes import Axes


class PointCreator(CreatorWidgetBase):
    def __init__(self, ax: Axes, image: AxesImage, onselect=None, markerKwargs: t_.Dict = None):
        """ A selector widget that facilitates the selection of a single point in an image. Displayed by a marker
        Args:
            ax (Axes): A reference to the matplotlib `Axes` that this selector widget is active on.
            image (AxesImage): the matplotlib image object in use.
            onselect (callable): A function that will be executed after the user selects a point.
            sideLength (int): The initial length (in pixels) of the rectangle used to select a point. This can be changed on the fly with the mouse wheel.

        Returns:
            np.ndarray: The 4 XY vertices of the selection square.
        """
        super().__init__(ax, image, onselect=onselect)
        self.onselect = onselect

        self._radius = self.__scale_axis_to_data(.01)  # This scaling is done so that no matter how zoomed in/out the data is we still have a reasonable on-screen size.
        self._patch = Circle((0, 0), radius=self._radius, facecolor=(1, 0, 0, 0.9), animated=True)
        self._patch.set_visible(False)
        self._ghostPatch = Circle((0, 0), radius=self._radius, facecolor=(0, 0, 1, 0.5), animated=True)
        self.addArtist(self._patch)
        self.addArtist(self._ghostPatch)
        self.setArtistVisible(self._patch, False)

    def reset(self):
        self._patch.set_visible(False)

    @staticmethod
    def getHelpText():
        return "For selecting a single point. Scroll to change the marker size`."

    def _onhover(self, event):
        self._ghostPatch.set_center((event.xdata, event.ydata))
        self.updateAxes()

    def _press(self, event):
        if event.button != 1:
            return
        _point = (event.xdata, event.ydata)
        self._patch.set_center(_point)
        self._patch.set_radius(self._radius)
        self.setArtistVisible(self._patch, True)
        if self.onselect:
            verts = (_point, )
            handles = verts
            self.onselect(verts, handles)

    def _on_scroll(self, event):
        delta = event.step
        self._radius *= 1 + delta / 10
        minR = self.__scale_axis_to_data(.005)
        maxR = self.__scale_axis_to_data(0.05)
        print(minR, self._radius)
        if self._radius < minR:
            self._radius = minR
        elif self._radius > maxR:
            self._radius = maxR
        self._ghostPatch.set_radius(self._radius)
        self.updateAxes()

    def __scale_axis_to_data(self, val: float):
        """Convert from axis coords to data coords. Scaling only Assuming even scaling."""
        scale = (self.ax.transAxes + self.ax.transData.inverted()).get_matrix()[0, 0]
        return scale * val
