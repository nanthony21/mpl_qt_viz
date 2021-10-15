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
import copy
import typing

from matplotlib.artist import Artist
from matplotlib.axes import Axes
from matplotlib.lines import Line2D
from matplotlib.patches import Patch
from matplotlib.widgets import AxesWidget
import typing as t_
if typing.TYPE_CHECKING:
    from matplotlib.backend_bases import LocationEvent, KeyEvent, MouseEvent
    from matplotlib.image import AxesImage


class AxManager:
    """An object to manage multiple selector tools on a single axes. Only one of these should exist per Axes object.

    Args:
        ax: The matplotlib Axes object to draw on.

    """
    _AX_ATTR = '_mpl_qt_viz_axManager'  # When a manager is attached to a Matplotlib Axes this attribute will be added to the axis. Allows making sure we only add one manager per axis.

    class ManagerAlreadyAssignedException(Exception):
        def __init__(self, axMan: AxManager):
            self._axMan = axMan

        def getExistingManager(self):
            return self._axMan

    def __init__(self, ax: Axes):
        if hasattr(ax, AxManager._AX_ATTR):
            raise AxManager.ManagerAlreadyAssignedException(getattr(ax, AxManager._AX_ATTR))

        setattr(ax, AxManager._AX_ATTR, self)  # Store reference to self in Axes so we don't assign multiple managers.
        self.artists = []
        self.ax = ax
        self.canvas = self.ax.figure.canvas
        self.canvas.mpl_connect('draw_event', self._update_background)
        self.background = None

    def addArtist(self, artist: Artist):
        """Adds an artist to the manager.

        Args:
            artist: A new matplotlib `Artist` to be managed.
        """
        #TODO implement more cases here.
        self.artists.append(artist)
        if isinstance(artist, Patch):
            self.ax.add_patch(artist)
        elif isinstance(artist, Line2D):
            self.ax.add_line(artist)
        else:
            self.ax.add_artist(artist)

    def removeArtist(self, artist: Artist):
        """Remove a single `Artist` from the manaager

        Args:
            artist: A previously added matplotlib `Artist`.
        """
        self.artists.remove(artist)
        artist.remove()

    def update(self):
        """Re-render the axes. Call this after you know that something has changed with the plot."""
        # TODO what is the return value here?
        if not self.ax.get_visible():
            return False
        if self.canvas.supports_blit:
            if self.background is not None:
                self.canvas.restore_region(self.background)
            for artist in self.artists:
                if artist.get_visible():
                    try:
                        self.ax.draw_artist(artist)
                    except AttributeError:
                        pass  # This can happen if the figure hasn't already had it's initial draw
            try:
                self.canvas.blit(self.ax.bbox)
            except AttributeError: #Sometimes this happens when first opening
                self.canvas.draw_idle()
        else:
            self.canvas.draw_idle()
        return False

    def _update_background(self, event):
        """force an update of the background"""
        # If you add a call to `ignore` here, you'll want to check edge case:
        # `release` can call a draw event even when `ignore` is True.
        if self.canvas.supports_blit:
            self.background = self.canvas.copy_from_bbox(self.ax.bbox)


class InteractiveWidgetBase(AxesWidget):
    """Base class for other selection widgets in this package. Requires to be managed by an AxManager. Inherited classes
    can implement a number of action handlers like mouse actions and keyboard presses.

    Args:
        ax: A reference to the Matplotlib `Axes` that this selector widget is active on.
        image: A reference to a matplotlib `AxesImage`. Selectors may use this reference to get information such as data values from the image
            for computer vision related tasks.

    Attributes:
        state (set): A `set` that stores strings indicating the current state (Are we dragging the mouse, is the shift
            key pressed, etc.
        ax: A reference to the matplotlib Axes that this selector is assigned to.
        image (AxesImage): A reference to the image being interacted with. Can be used to get the image data.
    """

    def __init__(self, ax: Axes, image: typing.Optional[AxesImage] = None):
        AxesWidget.__init__(self, ax)
        try:  # Create a new AxManager, if it already exists for that axes then store a reference to the existing one.
            self._axMan = AxManager(ax)
        except AxManager.ManagerAlreadyAssignedException as e:
            self._axMan = e.getExistingManager()
        self.ax = ax
        self.image = image
        self._artists: t_.Dict[Artist, bool] = {}  # Keeps track of active artists and whether or not they should be visible.
        self.connect_event('motion_notify_event', self.onmove)
        self.connect_event('button_press_event', self.press)
        self.connect_event('button_release_event', self.release)
        self.connect_event('key_press_event', self.on_key_press)
        self.connect_event('key_release_event', self.on_key_release)
        self.connect_event('scroll_event', self.on_scroll)

        self._state_modifier_keys = dict(space=' ', clear='escape', shift='shift', control='control')

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

        # Set the visibility of our artists
        for artist, shouldBeVisible in self._artists.items():
            artist.set_visible(shouldBeVisible and active)
        self.updateAxes()

        # if active:
        #     self._axMan._update_background(None)

    def ignore(self, event):
        """return *True* if *event* should be ignored. No event callbacks will be called if this returns true."""
        if not self.active or not self._axMan.ax.get_visible():
            return True
        if not self.canvas.widgetlock.available(self):  # If canvas was locked
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
        x0, x1 = self._axMan.ax.get_xbound()
        y0, y1 = self._axMan.ax.get_ybound()
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
            if key == self._state_modifier_keys['space']:
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
            # if key == self._state_modifier_keys['clear']: # This kind of thing can be handled individually by subclasses
            #     self.set_visible(False)
            #     return
            for (state, modifier) in self._state_modifier_keys.items():
                if modifier in key:
                    self.state.add(state)
            self._on_key_press(event)

    def on_key_release(self, event: KeyEvent):
        """Key release event handler and validator"""
        if self.active:
            key = event.key or ''
            for (state, modifier) in self._state_modifier_keys.items():
                if modifier in key:
                    self.state.discard(state)
            self._on_key_release(event)

    def setArtistVisible(self, artist: Artist, visible: bool):
        """
        Set visibility of a single artist, invisible artists will not be reenabled with `set_visible`
        True.

        Args:
            artist: The artist to have its visibility set.
            visible: Whether or not the artist should be visible
        """
        self._artists[artist] = visible  # Keep track if the artist should be visible. Used when toggling visibility of entire Interactor.
        artist.set_visible(visible)

    def addArtist(self, artist: Artist):
        """Add a matplotlib artist to be managed."""
        self._axMan.addArtist(artist)
        self._artists[artist] = True  # New artists are assumed that they should be visible.

    def removeArtists(self):
        """Remove all artist objects associated with this selector"""
        while len(self._artists) > 0:  # Using a for loop here has problems since we remove items as we go.
            self.removeArtist(list(self._artists.keys())[0])

    def removeArtist(self, artist: Artist):
        self._artists.pop(artist)
        self._axMan.removeArtist(artist)

    def updateAxes(self):
        """Re-render the axes. Call this after you know that something has changed with the plot."""
        self._axMan.update()

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