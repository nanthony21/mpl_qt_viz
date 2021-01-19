from __future__ import annotations
import typing
from abc import ABCMeta, abstractmethod
from matplotlib.image import AxesImage
from mpl_qt_viz.roiSelection._coreClasses import InteractiveWidgetBase
if typing.TYPE_CHECKING:
    from matplotlib.axes import Axes


class CreatorWidgetBase(InteractiveWidgetBase, metaclass=ABCMeta):
    """Base class for other selection widgets in this package. These widgets are used to create a polygon region from scratch. Inherited classes
    can implement a number of action handlers like mouse actions and keyboard presses.

    Args:
        ax: A reference to the matplotlib `Axes` that this selector widget is active on.
        image: A reference to a matplotlib `AxesImage`. Selectors may use this reference to get information such as data values from the image
            for computer vision related tasks.
        onselect: A callback function that will be called when the selector finishes a selection. See the `onselect` method
            for the appropriate signature.

    Attributes:
        state (set): A `set` that stores strings indicating the current state (Are we dragging the mouse, is the shift
            key pressed, etc.
        artists (list): A `list` of matplotlib artists managed by the selector.
        image (AxesImage): A reference to the image being interacted with. Can be used to get the image data.
    """

    # Typing aliases
    PolygonCoords = typing.Sequence[typing.Tuple[float, float]]
    SelectionFunction = typing.Callable[[PolygonCoords, PolygonCoords], None]

    def __init__(self, ax: Axes, image: typing.Optional[AxesImage] = None,
                 onselect: typing.Optional[SelectionFunction] = None):
        super().__init__(ax, image)
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
        if self._onselect is not None:
            self._onselect(verts, handles)
