# Copyright 2018-2020 Nick Anthony, Backman Biophotonics Lab, Northwestern University
#
# This file is part of PWSpy.
#
# PWSpy is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# PWSpy is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with PWSpy.  If not, see <https://www.gnu.org/licenses/>.

from __future__ import annotations
from abc import abstractmethod, ABCMeta
from matplotlib.image import AxesImage
from pwspy.utility.matplotlibWidgets.coreClasses import AxManager
import typing
from pwspy.utility.matplotlibWidgets.widgetBase import InteractiveWidgetBase


class CreatorWidgetBase(InteractiveWidgetBase, metaclass=ABCMeta):
    """Base class for other selection widgets in this package. These widgets are used to create a polygon region from scratch. Requires to be managed by an AxManager. Inherited classes
    can implement a number of action handlers like mouse actions and keyboard presses.

    Args:
        axMan: A reference to the `AxManager` object used to manage drawing the matplotlib `Axes` that this selector widget is active on.
        image: A reference to a matplotlib `AxesImage`. Selectors may use this reference to get information such as data values from the image
            for computer vision related tasks.
        onselect: A callback function that will be called when the selector finishes a selection. See the `onselect` method
            for the appropriate signature.

    Attributes:
        state (set): A `set` that stores strings indicating the current state (Are we dragging the mouse, is the shift
            key pressed, etc.
        artists (list): A `list` of matplotlib widgets managed by the selector.
        axMan (AxManager): The manager for the Axes. Call its `update` method when something needs to be drawn.
        image (AxesImage): A reference to the image being interacted with. Can be used to get the image data.
    """

    #Typing aliases
    PolygonCoords = typing.Sequence[typing.Tuple[float, float]]
    SelectionFunction = typing.Callable[[PolygonCoords, PolygonCoords], None]

    def __init__(self, axMan: AxManager, image: typing.Optional[AxesImage] = None,
                 onselect: typing.Optional[SelectionFunction] = None):
        super().__init__(axMan, image)
        self._onselect = onselect

    @staticmethod
    @abstractmethod
    def getHelpText():
        """Return a description of the selector which can be used as a tooltip."""
        return "This Selector has no help text."

    @abstractmethod
    def reset(self):
        """Reset the state of the selector so it's ready for a new selection."""
        pass

    def onselect(self, verts: PolygonCoords, handles: PolygonCoords):  # This method only exists to make the signature of onselect more obvious
        """This method should be called when the interaction is done to execute whatever finalization function was specified
        in the constructor.

        Args:
            verts: A sequence of 2-tuple coordinates that fully define the polygon.
            handles: A reduced sequence of coordinates that define special points onthe shape to potentially be used as draggable handles for a modifier.
        """
        self._onselect(verts, handles)