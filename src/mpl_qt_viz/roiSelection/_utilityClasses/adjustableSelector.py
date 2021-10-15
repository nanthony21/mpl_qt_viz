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
from .._modifierWidgets import PolygonModifier
if typing.TYPE_CHECKING:
    from matplotlib.axes import Axes
    from matplotlib.image import AxesImage
    from .._creatorWidgets._base import CreatorWidgetBase


class AdjustableSelector:
    """This class manages an roi selector. By setting `adjustable` true then when the selector calls its `onselect` function
    the results will be passed on to a PolygonInteractor for further tweaking. Tweaking can be confirmed by pressing enter.
    at the end the selector will pass a set of coordinates to the `onfinished` function if it has been set.

    Args:
        ax: A matplotlib `Axes` to interact with.
        image: A matplotlib `AxesImage`. Some selectors use the data in this image for their selection.
        selectorClass: A class that implements `SelectorWidgetBase`. This will be the intial selector used.
        onfinished: a callback function when the selection finished. The function should accept a single input argument
            which is a list of the 2d coordinated outlining the selected polygon.
    """
    def __init__(self, ax: Axes, image: AxesImage, selectorClass: typing.Type[CreatorWidgetBase],
                 onfinished: typing.Optional[typing.Callable] = None, onPolyTuningCancelled: typing.Optional[typing.Callable] = None):
        self.ax = ax
        self.image = image
        self.selector: CreatorWidgetBase = selectorClass(self.ax, self.image, onselect=self._goPoly)
        self.selector.active = False
        self.adjuster = PolygonModifier(self.ax, onselect=self.finish, onCancelled=onPolyTuningCancelled)
        self.adjuster.active = False
        self.adjustable = False
        self.onfinished = onfinished

    def reset(self):
        """Clear all artists used by the selector. :todo: Shouldn't this check if the `adjuster` is active and reset it as well?"""
        self.selector.reset()

    @property
    def adjustable(self) -> bool:
        """Determines whether or not the polygon interactor will be used to adjust the selection at the end of the initial
        selection."""
        return self._adjustable

    @adjustable.setter
    def adjustable(self, enabled: bool):
        self._adjustable = enabled
        if enabled:
            self.selector.onselect = self._goPoly
        else:
            self.selector.onselect = self.finish

    def setActive(self, active: bool):
        """This activates the selector. for a looping selection you should call this method from the onfinished function."""
        if active:
            self.selector.set_active(True)
        else:
            self.adjuster.set_active(False)
            self.selector.set_active(False)

    def setSelector(self, selectorClass: typing.Type):
        """Remove the current selector and replace it with a new type of selector.

        Args:
            selectorClass: A class the implements `SelectorWidgetBase`.
        """
        self.selector.removeArtists()
        self.selector.set_active(False)
        self.selector = selectorClass(self.ax, self.image)
        self.adjustable = self.adjustable

    def _goPoly(self, verts: typing.Sequence[typing.Tuple[float, float]], handles: typing.Sequence[typing.Tuple[float, float]]):
        """This callback is registered with the selectorWidget when we are in adjustable mode. Upon completion of the
        initial selection this callback passes the handles to the polygon adjuster."""
        self.selector.set_active(False)
        self.adjuster.set_active(True)
        self.adjuster.initialize([handles])  # It's important that this happens after `set_active` otherwise we get weird drawing issues

    def finish(self, verts, handles):
        """This callback is registered with the selectorWidget when we are not in adjustable mode. In adjustable mode it
        is instead registered with the polygon adjuster. It deactivates the class and calls the `onfinished` callback."""
        self.setActive(False)
        if self.onfinished is not None:
            if self.adjustable:
                self.onfinished(verts[0])  # The polygon interactor has a slightly different signature than the `creatorwidgets`
            else:
                self.onfinished(verts)
