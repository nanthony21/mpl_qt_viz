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
import enum
import typing
from time import time
import numpy as np
from matplotlib.image import AxesImage
from matplotlib.patches import Ellipse, Circle
from mpl_qt_viz.roiSelection._creatorWidgets._base import CreatorWidgetBase

if typing.TYPE_CHECKING:
    from matplotlib.axes import Axes


class _SelectionStatus(enum.Enum):
    """Helps keep track of where we are in the selection process"""
    NotStarted = enum.auto()
    FirstAxis = enum.auto()
    SecondAxis = enum.auto()


class EllipseCreator(CreatorWidgetBase):
    """Allows the user to select an elliptical region.

    Args:
        ax: The matplotlib `Axes` that you want to interact with.
        image: A reference to a matplotlib `AxesImage`. Selectors may use this reference to get information such as data values from the image
            for computer vision related tasks.
        onselect: A callback that will be called when the user hits 'enter'. Should have signature (polygonCoords, sparseHandleCoords).
    """
    def __init__(self, ax: Axes, image: AxesImage, onselect: typing.Callable = None):
        super().__init__(ax, image, onselect=onselect)
        self._status = _SelectionStatus.NotStarted
        self._startPoint: typing.Tuple[float, float] = None
        self._clickTime = time()
        self.patch = Ellipse((0, 0), 0, 0, 0, facecolor=(0, 0, 1, .1), animated=True, edgecolor=(0, 0, 1, .8))
        self.addArtist(self.patch)
        self.circleGuide = Circle((0, 0), animated=True, edgecolor=(1, 0, 0, .6), facecolor=(0, 0, 0, 0), linestyle='dotted')
        self.addArtist(self.circleGuide)

    @staticmethod
    def getHelpText():
        """Return a description of the selector which can be used as a tooltip."""
        return "Click and drag to draw the length of the ellipse. Then click again to set the width."

    def reset(self):
        """Reset the state of the selector so it's ready for a new selection."""
        self._status = _SelectionStatus.NotStarted
        self._startPoint = None

    def _press(self, event):
        """Set the initial point of the selection. Then drag to draw the length of the ellipse.
        If we are drawing the major axis then switch to drawing the second axis. If we are drawing the second axis
        then finalize the selection
        """
        if event.button != 1:
            return
        self._clickTime = time()
        if self._status is _SelectionStatus.NotStarted:
            self._startPoint = (event.xdata, event.ydata)
            self.patch.set_center(self._startPoint)
            self.circleGuide.set_center(self._startPoint)
            self._status = _SelectionStatus.FirstAxis
        elif self._status is _SelectionStatus.FirstAxis:  # If we were on the first axis transition to the second axis.
            self._status = _SelectionStatus.SecondAxis
        elif self._status is _SelectionStatus.SecondAxis:  # If we were on the second axis then finalize.
            self._status = _SelectionStatus.NotStarted
            if self.onselect:
                angle = np.linspace(0, 2*np.pi, num=100)
                x_ = self.patch.width/2 * np.cos(angle) #unrotated ellipse centered at origin
                y_ = self.patch.height/2 * np.sin(angle)
                s = np.sin(np.radians(self.patch.angle))
                c = np.cos(np.radians(self.patch.angle))
                x = x_ * c - y_ * s  # rotate ellipse
                y = x_ * s + y_ * c
                x += self.patch.center[0] #translate ellipse
                y += self.patch.center[1]
                verts = list(zip(x, y))
                handles = [verts[0], verts[len(verts)//4], verts[len(verts)//2], verts[3*len(verts)//4], verts[0]]
                self.onselect(verts, handles)

    def _ondrag(self, event):
        """If an initial point has been selected then draw to draw the length of the ellipse."""
        self._onhover(event) # Dragging and hovering are both allowed.


    def _onhover(self, event):
        """When drawing the first axis allow the angle of the ellipse to be changed. Also update the circle guide.
        When drawing the second axis only allow adjusting width, not angle. Keep the circle guide frozen."""
        if self._status is _SelectionStatus.NotStarted:
            return
        dx = event.xdata - self._startPoint[0]
        dy = event.ydata - self._startPoint[1]
        if self._status is _SelectionStatus.FirstAxis:
            self.patch.height = np.sqrt(dx**2 + dy**2)
            self.patch.width = self.patch.height / 4
            self.patch.set_center([self._startPoint[0] + dx / 2, self._startPoint[1] + dy / 2])
            self.patch.angle = np.degrees(np.arctan2(dy, dx)) - 90
            self.circleGuide.set_center([self._startPoint[0] + dx / 2, self._startPoint[1] + dy / 2])
            self.circleGuide.set_radius(np.sqrt(dx**2 + dy**2)/2)
        elif self._status is _SelectionStatus.SecondAxis:
            h = np.sqrt(dx**2 + dy**2)
            theta = np.arctan2(dy, dx) - np.radians(self.patch.angle)
            self.patch.width = 2*h*np.cos(theta)
        self.updateAxes()

    def _release(self, event):
        if time() - self._clickTime >= 0.3: # In order to make dragging and hovering both behave the same we need to only respond to a release if we think that the mouse has been dragged.
            self._press(event)

if __name__ == '__main__':
    import matplotlib.pyplot as plt
    fig, ax = plt.subplots()
    sel = EllipseCreator(ax, None, lambda verts, handles: print(handles))
    plt.show()
