from __future__ import annotations
import copy
from matplotlib.artist import Artist
from matplotlib.backend_bases import LocationEvent, MouseEvent, KeyEvent
from matplotlib.image import AxesImage
from matplotlib.widgets import AxesWidget
import typing
if typing.TYPE_CHECKING:
    from pwspy.utility.matplotlibWidgets import AxManager


class InteractiveWidgetBase(AxesWidget):
    """Base class for other selection widgets in this package. Requires to be managed by an AxManager. Inherited classes
    can implement a number of action handlers like mouse actions and keyboard presses.

    Args:
        axMan: A reference to the `AxManager` object used to manage drawing the matplotlib `Axes` that this selector widget is active on.
        image: A reference to a matplotlib `AxesImage`. Selectors may use this reference to get information such as data values from the image
            for computer vision related tasks.

    Attributes:
        state (set): A `set` that stores strings indicating the current state (Are we dragging the mouse, is the shift
            key pressed, etc.
        artists (list): A `list` of matplotlib widgets managed by the selector.
        axMan (AxManager): The manager for the Axes. Call its `update` method when something needs to be drawn.
        image (AxesImage): A reference to the image being interacted with. Can be used to get the image data.
    """

    def __init__(self, axMan: AxManager, image: typing.Optional[AxesImage] = None):
        AxesWidget.__init__(self, axMan.ax)
        self.axMan = axMan
        self.image = image
        self._artists = {}
        self.connect_event('motion_notify_event', self.onmove)
        self.connect_event('button_press_event', self.press)
        self.connect_event('button_release_event', self.release)
        self.connect_event('key_press_event', self.on_key_press)
        self.connect_event('key_release_event', self.on_key_release)
        self.connect_event('scroll_event', self.on_scroll)

        self.state_modifier_keys = dict(space=' ', clear='escape', shift='shift', control='control')

        # will save the data (position at mouseclick)
        self.eventpress = None
        # will save the data (pos. at mouserelease)
        self.eventrelease = None
        self._prev_event = None
        self.state = set()

    def __del__(self):
        try:
            self.removeArtists()
        except TypeError:  # Sometimes when the program closes the order that objects are deleted in causes a None typeerror to occur here.
            pass

    def set_active(self, active: bool):
        AxesWidget.set_active(self, active)
        if active:
            self.axMan._update_background(None)

    def ignore(self, event):
        """return *True* if *event* should be ignored. No event callbacks will be called if this returns true."""
        if not self.active or not self.axMan.ax.get_visible():
            return True
        if not self.canvas.widgetlock.available(self): # If canvas was locked
            return True
        if not hasattr(event, 'button'):
            event.button = None
        if self.eventpress is None:  # If no button was pressed yet ignore the event if it was out of the axes
            return event.inaxes != self.ax
        if event.button == self.eventpress.button:  # If a button was pressed, check if the release-button is the same.
            return False
        # If a button was pressed, check if the release-button is the same.
        return event.inaxes != self.ax or event.button != self.eventpress.button

    def __get_data(self, event: LocationEvent):
        """Get the xdata and ydata for event, with limits"""
        if event.xdata is None:
            return None, None
        x0, x1 = self.axMan.ax.get_xbound()
        y0, y1 = self.axMan.ax.get_ybound()
        xdata = max(x0, event.xdata)
        xdata = min(x1, xdata)
        ydata = max(y0, event.ydata)
        ydata = min(y1, ydata)
        return xdata, ydata

    def __clean_event(self, event: LocationEvent):
        """Clean up an event
        Use prev event if there is no xdata
        Limit the xdata and ydata to the axes limits
        Set the prev event
        """
        if event.xdata is None:
            event = self._prev_event
        else:
            event = copy.copy(event)
        event.xdata, event.ydata = self.__get_data(event)
        self._prev_event = event
        return event

    def press(self, event: MouseEvent):
        """Button press handler and validator"""
        if not self.ignore(event):
            event = self.__clean_event(event)
            self.eventpress = event
            key = event.key or ''
            key = key.replace('ctrl', 'control')
            # space state is locked in on a button press
            if key == self.state_modifier_keys['space']:
                self.state.add('space')
            self._press(event)
            return True
        return False

    def release(self, event: MouseEvent):
        """Button release event handler and validator"""
        if not self.ignore(event) and self.eventpress:
            event = self.__clean_event(event)
            self.eventrelease = event
            self._release(event)
            self.eventpress = None
            self.eventrelease = None
            self.state.discard('space')
            return True
        return False

    def onmove(self, event: MouseEvent):
        """Cursor move event handler and validator"""
        if not self.ignore(event):
            event = self.__clean_event(event)
            if self.eventpress:
                self._ondrag(event)
            else:
                self._onhover(event)
            return True
        return False

    def on_scroll(self, event: MouseEvent):
        """Mouse scroll event handler and validator"""
        if not self.ignore(event):
            self._on_scroll(event)

    def on_key_press(self, event: KeyEvent):
        """Key press event handler and validator for all selection widgets"""
        if self.active:
            key = event.key or ''
            key = key.replace('ctrl', 'control')
            # if key == self.state_modifier_keys['clear']: # This kind of thing can be handled individually by subclasses
            #     self.set_visible(False)
            #     return
            for (state, modifier) in self.state_modifier_keys.items():
                if modifier in key:
                    self.state.add(state)
            self._on_key_press(event)

    def on_key_release(self, event: KeyEvent):
        """Key release event handler and validator"""
        if self.active:
            key = event.key or ''
            for (state, modifier) in self.state_modifier_keys.items():
                if modifier in key:
                    self.state.discard(state)
            self._on_key_release(event)

    def set_visible(self, visible: bool):
        """ Set the visibility of our artists """
        for artist, shouldBeVisible in self._artists.items():
            artist.set_visible(shouldBeVisible and visible)
        self.axMan.update()

    def setArtistVisible(self, artist: Artist, visible: bool):
        "set visibility of a single artist, invisible artists will not be reenabled with `set_visible` True."
        self._artists[artist] = visible
        artist.set_visible(visible)

    def addArtist(self, artist: Artist):
        """Add a matplotlib artist to be managed."""
        self.axMan.addArtist(artist)
        self._artists[artist] = True  # New artists are assumed that they should be visible.

    def removeArtists(self):
        """Remove all artist objects associated with this selector"""
        while len(self._artists) > 0:  # Using a for loop here has problems since we remove items as we go.
            self.removeArtist(list(self._artists.keys())[0])

    def removeArtist(self, artist: Artist):
        self._artists.pop(artist)
        self.axMan.removeArtist(artist)

    # Overridable events
    def _on_key_release(self, event: KeyEvent):
        """Key release event handler"""
        pass

    def _on_key_press(self, event: KeyEvent):
        """Key press event handler - use for widget-specific key press actions."""
        pass

    def _on_scroll(self, event: MouseEvent):
        """Mouse scroll event handler"""
        pass

    def _ondrag(self, event: MouseEvent):
        """Cursor move event handler"""
        pass

    def _onhover(self, event: MouseEvent):
        pass

    def _release(self, event: MouseEvent):
        """Button release event handler"""
        pass

    def _press(self, event: MouseEvent):
        """Button press handler"""
        pass