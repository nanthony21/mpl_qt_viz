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
from abc import ABC, abstractmethod
import numpy as np
import matplotlib.pyplot as plt
if typing.TYPE_CHECKING:
    from matplotlib.artist import Artist

lw = 0.75


class PlotBase(ABC):
    """An abstract class for the plots in the ND plotter widget. Dimension is the numpy array dimensions associated
    with this plot. For an image plot it should be a tuple of the two dimensions."""
    def __init__(self, ax: plt.Axes, dimensions: typing.Tuple[int, ...]):
        self.ax = ax  # The axes object that this plot exists on.
        self.dimensions = dimensions # The dimensions of ND-array that this plot visualized. 2d for an image, 1d for a plot
        self.background = None

    def updateBackground(self):
        """Refresh the background, this is for the purposes of blitting."""
        self.background = self.ax.figure.canvas.copy_from_bbox(self.ax.bbox)

    def drawArtists(self):
        """Redraw each matplotlib artist managed by this object."""
        for artist in self.artists:
            self.ax.draw_artist(artist)

    @property
    @abstractmethod
    def artists(self) -> typing.Iterable[Artist]:
        """Derived classes should have an `artist` attribute list of all matplotlib `Artists` that are managed by the
        compoenent. This is used to redraw the artists each time a change is made."""
        pass

    @property
    @abstractmethod
    def data(self) -> np.ndarray:
        """Subclasses should have a settable `data` property that refers to the data currently displayed by the plot."""
        pass

    @abstractmethod
    def setRange(self, Min, Max):
        """Set the range of values that can be viewed. this can be the matplotlib `clim` for an image or the yrange for a plot"""
        pass

    @abstractmethod
    def setMarker(self, pos: typing.Tuple):
        """Set the position of marker line. for an image this is 2d. for a plot it is 1d."""
        pass


class ImPlot(PlotBase):
    """This class manages a 2D image plot of data with a crosshair formed by a vertical and horizontal line.

    Args:
        ax: The matplotlib `Axes` object to draw on.
        verticalIndex: See documentation for the `setIndices` method.
        horizontalIndex: See documentation for the `setIndices` method.
        dims: In the context of composite plot (PlotNd) representing higher dimensional data this is used to keep track
            of which dimensions of the data this plot is representing.

    """
    def __init__(self, ax: plt.Axes, verticalIndex, horizontalIndex, dims: typing.Tuple[int, int], cmap=None):
        super().__init__(ax, dims)
        self.shape = (len(verticalIndex), len(horizontalIndex))
        self.im = self.ax.imshow(np.zeros(self.shape), aspect='auto', animated=True, interpolation=None, cmap=cmap)
        self.setIndices(verticalIndex, horizontalIndex)
        self.ax.get_yaxis().set_visible(False)
        self.ax.get_xaxis().set_visible(False)
        self.vLine = self.ax.plot([100, 100], [self._indices[0][0], self._indices[0][-1]], 'r', linewidth=lw, animated=True)[0]
        self.hLine = self.ax.plot([self._indices[1][0], self._indices[1][-1]], [100, 100], 'r', linewidth=lw, animated=True)[0]
        self.range = (0, 1)

    @property
    def artists(self) -> typing.Iterable[Artist]:
        return [self.im, self.hLine, self.vLine]

    def setRange(self, Min, Max):
        """Sets the value range (clim) of the image."""
        self.range = (Min, Max)
        self.im.set_clim(*self.range)

    def setMarker(self, pos: typing.Tuple[float, float]):
        """Set the position of the crosshairs.

        Args:
            pos: a (y, x) tuple of coordinates to set the crosshairs to. The values should be in terms of the horizontal
                and vertical indexes of the plot.
        """
        assert len(pos) == 2
        y, x = pos
        y = self._verticalCoordToValue(y)
        x = self._horizontalCoordToValue(x)
        self.hLine.set_data([self._indices[1][0], self._indices[1][-1]], [y, y])
        self.vLine.set_data([x, x], [self._indices[0][0], self._indices[0][-1]])

    @property
    def data(self):
        """The 2D image data of the plot"""
        return self.im.get_data()

    @data.setter
    def data(self, data: np.ndarray):
        """Set the 2D image data of the plot."""
        self.im.set_data(data)

    def setIndices(self, verticalIndex: typing.Iterable[float], horizontalIndex: typing.Iterable[float]):
        """If we want the X and Y dimensions of our image to be considered to span a range given by something other than
        just the integer element coordinates in the array ([0, 1, 2, ...]) then we can provide a vertical and horizontal
        index. For example if we want the image to span from -1 to 1 vertically and from 0 to 100 horizontally we could
        call `self.setIndices(np.linspace(-1, 1, num=self.data.shape[0]), np.linspace(0, 100, num=self.data.shape[1])`"""
        self._indices = (tuple(verticalIndex), tuple(horizontalIndex))
        self.shape = (len(verticalIndex), len(horizontalIndex))
        self.im.set_extent((horizontalIndex[0], horizontalIndex[-1], verticalIndex[-1], verticalIndex[0]))  # It seems like the verticalIndex items are backwards here. But this is how it had to be to get axis rotation to work properly. I suspect this has to do with using the invertAxis option of sideplot that is next to the ImPlot in the PlotNd widget.

    def _horizontalCoordToValue(self, coord):
        """Given a coordinate of the ND-array being visualized ( 0, 1, 2, ...) return the value of this plot's index.

        Args:
            coord: The axis=1 coordinate in the `data` numpy array that we are interested in. E.G. for element data[i,j]
                `coord` would be j

        Returns:
            The value of the horizontal index of the plot corresponds to `coord`.
        """
        return self._indices[1][coord]

    def _verticalCoordToValue(self, coord):
        """Given a coordinate of the ND-array being visualized ( 0, 1, 2, ...) return the value of this plot's index.


        Args:
            coord: The axis=0 coordinate in the `data` numpy array that we are interested in. E.G. for element data[i,j]
                `coord` would be i

        Returns:
            The value of the vertical index of the plot corresponds to `coord`.
        """
        return self._indices[0][coord]

    def verticalValueToCoord(self, value: float):
        """Given a value of this plot's index return the nearest corresponding coordinate [0, 1, 2, ...]"""
        coord = np.where(np.abs(self._indices[0] - value) == np.min(np.abs(self._indices[0] - value)))[0]
        return int(coord)

    def horizontalValueToCoord(self, value: float):
        """Given a value of this plot's index return the nearest corresponding coordinate [0, 1, 2, ...]"""
        coord = np.where(np.abs(self._indices[1] - value) == np.min(np.abs(self._indices[1] - value)))[0]
        return int(coord)


class SidePlot(PlotBase):
    """This class manages a 1D plot of data with a marker formed by a single line.

    Args:
        ax: The matplotlib `Axes` object to draw on.
        index: See documentation for the `setIndex` method.
        dimension: In the context of composite plot (PlotNd) representing higher dimensional data this is used to keep
            track of which dimensions of the data this plot is representing.
        invertAxis: Change the data direction. this can be used to make the image orientation match the orientation of
            other images.
        title: The name to display for this plot.

    """
    def __init__(self, ax, index: typing.Iterable, vertical: bool, dimension: int, invertAxis: bool = False, title: str = None):
        super().__init__(ax, (dimension,))
        self.vertical = vertical
        self.setIndex(index)
        if title:
            self.ax.set_title(title)
        limFunc = self.ax.set_ylim if vertical else self.ax.set_xlim

        if invertAxis:
            limFunc(index[-1], index[0])
        else:
            limFunc(index[0], index[-1])
        self.range = (0, 1)
        markerData = (self.range, (0, self.dimLength))
        if self.vertical:
            markerData = markerData[1] + markerData[0]
        self.plot = self.ax.plot([0], [0], animated=True)[0]
        self.markerLine = self.ax.plot(*markerData, color='r', linewidth=lw, animated=True)[0]

    @property
    def artists(self) -> typing.Iterable[Artist]:
        return [self.plot, self.markerLine]

    def setMarker(self, pos: typing.Tuple[float]):
        """Set the position of the marker line. Should be given in terms of this plot's `index`"""
        assert len(pos) == 1
        pos = self._coordToValue(pos[0])
        data = ((pos, pos), self.range)
        if self.vertical:
            data = (data[1],) + (data[0],)
        self.markerLine.set_data(*data)

    def _coordToValue(self, coord):
        """Given a coordinate of the ND-array being visualized ( 0, 1, 2, ...) return the value of this plot's index."""
        return self.index[coord]

    def valueToCoord(self, value):
        """Given a value of this plot's index return the nearest corresponding coordinate [0, 1, 2, ...]"""
        coord = np.argmin(np.abs(self.index - value))
        return int(coord)

    def setRange(self, Min, Max):
        """Set the y-axis range of the plot."""
        self.range = (Min, Max)
        if self.vertical:
            _ = self.ax.set_xlim
        else:
            _ = self.ax.set_ylim
        _(*self.range)

    def setIndex(self, index: typing.Iterable):
        """
        If we want the dimensions of our plot to be considered to span a range given by something other than
        just the integer element coordinates in the data ([0, 1, 2, ...]) then we can provide an index. For example
        if we want the plot to span from -1 to 1 we could call `self.setIndex(np.linspace(-1, 1, num=self.data.shape[0])`
        """
        self.index = tuple(index)
        self.dimLength = len(index)
        if self.vertical:
            _ = self.ax.set_ylim
        else:
            _ = self.ax.set_xlim
        _(self.index[0], self.index[-1])

    @property
    def data(self):
        return self._data

    @data.setter
    def data(self, data):
        self._data = data
        if self.vertical:
            data = (data, self.index)
        else:
            data = (self.index, data)
        self.plot.set_data(*data)

    def getIndex(self):
        return self.index


class CBar:
    """The colorbar at the top of the ND plotter."""
    def __init__(self, ax: plt.Axes, im):
        self.ax = ax
        self.cbar = ax.figure.colorbar(im, cax=self.ax, orientation='horizontal')
        self.ax.xaxis.set_ticks_position("top")
        self.artists = [None]

    def draw(self):
        self.ax.xaxis.set_ticks_position("top")  # The ticks keep wanting to move to the bottom :(
