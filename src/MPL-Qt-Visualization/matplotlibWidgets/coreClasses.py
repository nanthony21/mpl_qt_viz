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

from matplotlib.artist import Artist
from matplotlib.axes import Axes
from matplotlib.lines import Line2D
from matplotlib.patches import Patch


class AxManager:
    """An object to manage multiple selector tools on a single axes. Only one of these should exist per Axes object.

    Args:
        ax: The matplotlib Axes object to draw on.

    """
    def __init__(self, ax: Axes):
        self.artists = []
        self.ax = ax
        if hasattr(ax, 'pwspyAxisManager'):
            raise Exception("Axes already has an AxManager assiged.")
        ax.pwspyAxisManager = self
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
        self.update()

    def update(self):
        """Re-render the axes. Call this after you know that something has changed with the plot."""
        #TODO what is the return value here?
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