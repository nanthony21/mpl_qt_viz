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
import numpy as np
from PyQt5 import QtCore
import matplotlib as mpl
from matplotlib import pyplot as plt, gridspec
from matplotlib.axes import Axes
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg
from ._plots import ImPlot, SidePlot, CBar


def ifactive(func):
    """Decorator so that `func` is only executed if `self.spectraViewActive` is true. For event handlers that shouldn't
    happen when the Nd crosshair is deactivated."""
    def newfunc(self, event):
        if self.spectraViewActive:
            return func(self, event)
    return newfunc


class PlotNdCanvas(FigureCanvasQTAgg):
    """The matplotlib canvas for the PlotND widget.

    Args:
        data: 3D or greater numeric data
        names: The names to label each dimension of the data with.
        initialCoords: An optional tuple of coordinates to set the Nd crosshair to.
        indices: An optional tuple of 1d arrays of values to set as the indexes for each dimension of the data.
    """
    def __init__(self, data: np.ndarray, names: typing.Tuple[str, ...],
                 initialCoords: typing.Optional[typing.Tuple[int, ...]] = None,
                 indices: typing.Optional[typing.List] = None,
                 cmap: mpl.colors.Colormap = plt.cm.gray):
        assert len(data.shape) >= 3
        assert len(names) == len(data.shape)
        fig = plt.Figure(figsize=(6, 6), tight_layout=True)
        self.fig = fig
        super().__init__(self.fig)

        self.childPlots = []
        self.max = self.min = None  # The minimum and maximum for the color scaling

        if indices is None:
            self.indexes = tuple(range(s) for s in data.shape)
        else:
            assert len(indices) == len(data.shape)
            self.indexes = tuple(ind if (ind is not None) else range(s) for ind, s in zip(indices, data.shape))  # If an element is `None` then just use the range of the dimension.

        extraDims = len(data.shape[2:])  # the first two axes are the image dimensions. Any axes after that are extra dimensions that can be scanned through

        gs = gridspec.GridSpec(3, 2 + extraDims, hspace=0,
                               width_ratios=[.2 / (extraDims)] * extraDims + [1, .2],
                               height_ratios=[.1, 1, .2], wspace=0)

        ax: plt.Axes = fig.add_subplot(gs[1, extraDims])
        ax.get_xaxis().set_visible(False)
        ax.get_yaxis().set_visible(False)
        self.image = ImPlot(ax, self.indexes[0], self.indexes[1], (0, 1), cmap=cmap)

        ax: plt.Axes = fig.add_subplot(gs[1, extraDims + 1], sharey=self.image.ax)
        ax.yaxis.set_ticks_position('right')
        ax.get_xaxis().set_visible(False)
        self.spY = SidePlot(ax, self.indexes[0], True, 0)

        ax: plt.Axes = fig.add_subplot(gs[2, extraDims], sharex=self.image.ax)
        ax.xaxis.set_label_coords(.5, .95)
        ax.get_yaxis().set_visible(False)
        self.spX = SidePlot(ax, self.indexes[1], False, 1)

        ax: plt.Axes = fig.add_subplot(gs[0, extraDims])
        self.cbar = CBar(ax, self.image.im)

        extra = [fig.add_subplot(gs[1, i]) for i in range(extraDims)]
        [extra[i].set_ylim(0, data.shape[2 + i] - 1) for i in range(extraDims)]
        [extra[i].get_xaxis().set_visible(False) for i in range(extraDims)]
        self.extra = []
        for i, ax in enumerate(extra):
            self.extra.append(SidePlot(ax, self.indexes[2 + i], True, 2 + i))

        self.artistManagers = [self.spX, self.spY, self.image] + self.extra
        self.names = None
        self.setAxesNames(names)

        self.setFocusPolicy(QtCore.Qt.ClickFocus)
        self.setFocus()

        self._data = data

        Max = np.percentile(self.data[np.logical_not(np.isnan(self.data))], 99.99)
        Min = np.percentile(self.data[np.logical_not(np.isnan(self.data))], 0.01)
        self.updateLimits(Max, Min)

        self.coords = tuple(i // 2 for i in data.shape) if initialCoords is None else initialCoords

        self.spectraViewActive = True
        self.mpl_connect('button_press_event', self._onclick)
        self.mpl_connect('motion_notify_event', self._ondrag)
        self.mpl_connect('scroll_event', self._onscroll)
        self.mpl_connect('draw_event', self._updateBackground)
        self.updatePlots(blit=False)

    def setSpectraViewActive(self, active: bool):
        """Determines whether or not the Nd crosshair respons to mouse input. Allows us to disable the crosshair if we
        want the mouse to trigger other sorts of actions (e.g. ROI drawing)"""
        self.spectraViewActive = active
        if not active:
            self.draw() #This will clear the spectraviewer related crosshairs and plots.

    def _updateBackground(self, event):
        """This handler is tied to the matplotlib `draw_event` event. loops through all `artistManagers` and draws
        their artists efficiently"""
        for artistManager in self.artistManagers:
            artistManager.updateBackground()
        self.cbar.draw()

    def updatePlots(self, blit=True):
        """This should be called after `self.coords` have been changed to update the data of each plot.

        Args:
            blit: If `True` then drawing will be done more efficiently through `blitting`. Sometimes this needs to be false
                to trigger a full redraw though.
        """
        for plot in self.artistManagers:
            slic = tuple(c if i not in plot.dimensions else slice(None) for i, c in enumerate(self.coords))
            newData = self.data[slic]
            plot.data = newData
            newCoords = tuple(c for i, c in enumerate(self.coords) if i in plot.dimensions)
            plot.setMarker(newCoords)
        if blit:
            self.performBlit()
        else:
            self.draw()

    def performBlit(self):
        """Re-render the axes efficiently using matplotlib `blitting`."""
        for artistManager in self.artistManagers: # The fact that spX is first here makes it not render on click. sometimes not sure why.
            if artistManager.background is not None:
               self.restore_region(artistManager.background)
            artistManager.drawArtists() #Draw the artists
            self.blit(artistManager.ax.bbox)

    def updateLimits(self, Max: float, Min: float):
        """Update the range of values displayed. Similar to the set_clim method of a matplotlib image.

        Args:
            Max: The maximum value displayed
            Min: The minimum value displayed

        """
        self.min = Min
        self.max = Max
        self.image.setRange(self.min, self.max)
        self.spY.setRange(self.min, self.max)
        self.spX.setRange(self.min, self.max)
        for sp in self.extra:
            sp.setRange(self.min, self.max)
        self.cbar.draw()
        self.draw_idle()
        try:
            self.updatePlots()  # This will fail when this is run in the constructor.
        except:
            pass

    def setAxesNames(self, names: typing.Iterable[str]):
        """Set the names of to label each plot.
        Args:
            names: the order of the names should match the order of each corresponding axis in the data array.
        """
        self.names = tuple(names)
        self.spY.ax.set_title(self.names[0])
        self.spX.ax.set_xlabel(self.names[1])
        for i in range(len(self.extra)):
            self.extra[i].ax.set_title(self.names[2+i])

    def setIndices(self, indices: typing.Sequence[typing.Sequence[float]]):
        """Set the index values for each dimension of the array.

        Args:
            indices: A list or tuple of index values for each dimension of the data array.
        """
        self.indexes = indices
        for plot in self.artistManagers:
            if isinstance(plot, SidePlot):
                [plot.setIndex(ind) for i, ind in enumerate(self.indexes) if i in plot.dimensions]
            elif isinstance(plot, ImPlot):
                plot.setIndices(self.indexes[plot.dimensions[0]], self.indexes[plot.dimensions[1]])

    def rollAxes(self):
        """Change the order of the axes of the data. Allows viewing the sideview of the data."""
        self.setAxesNames([self.names[-1]] + list(self.names[:-1]))
        self.setIndices((self.indexes[-1],) + tuple(self.indexes[:-1]))
        self.coords = (self.coords[-1],) + tuple(self.coords[:-1])
        axes = list(range(len(self.data.shape)))
        self.data = np.transpose(self.data, [axes[-1]] + axes[:-1])
        self.draw()

    @property
    def data(self) -> np.ndarray:
        return self._data

    @data.setter
    def data(self, d: np.ndarray):
        self._data = d
        self.updatePlots()

    @ifactive
    def _onscroll(self, event):
        """Connected to the matplotlib 'scroll_event'. Increment the coords of the plot that the mouse is over."""
        if event.inaxes is None: # Don't do anyhing if the mouse wasn't over a plot.
            return
        elif event.inaxes == self.image.ax: # Don't respond to scrolling over the image plot.
            return
        if (event.button == 'up') or (event.button == 'down'):  # Only respond to up and down scrolling.
            step = int(4 * event.step)
            try:
                plot = [plot for plot in self.artistManagers if plot.ax == event.inaxes][0]
            except IndexError:  # No plot is being moused over
                return
            self.coords = tuple((c + step) % self.data.shape[plot.dimensions[0]] if i in plot.dimensions else c for i, c in enumerate(self.coords))
            self.updatePlots()

    @ifactive
    def _onclick(self, event):
        """Connected to the matplotlib 'button_press_event'."""
        if event.inaxes is None:  # Don't do anything if the mouse wasn't over a plot.
            return
        if event.dblclick:  # If it was a double click then open a new window visualizers the current data of the plot that was clicked on.
            am = [artistManager for artistManager in self.artistManagers if artistManager.ax == event.inaxes][0]
            if isinstance(am, SidePlot):
                fig, ax = plt.subplots()
                ax.plot(am.getIndex(), am.data)
                self.childPlots.append(fig)
                fig.show()
        self._processMouse(event.inaxes, event.xdata, event.ydata)

    def _processMouse(self, ax: Axes, x: float, y: float):
        """This is called by both the mouse click and mouse drag event handlers.

        Args:
            ax: The matplotlib `Axes` that the mouse event occurred in.
            x: The matplotlib x coordinate of the event
            y: The matplotlib y coordinate of the event
        """
        if ax == self.image.ax:
            self.coords = (self.image.verticalValueToCoord(y), self.image.horizontalValueToCoord(x)) + self.coords[2:]
        elif ax == self.spY.ax:
            self.coords = (self.spY.valueToCoord(y),) + self.coords[1:]
        elif ax == self.spX.ax:
            self.coords = (self.coords[0], self.spX.valueToCoord(x)) + self.coords[2:]
        elif ax in [sp.ax for sp in self.extra]:
            idx = [sp.ax for sp in self.extra].index(ax)
            sp = [sp for sp in self.extra if sp.ax is ax][0]
            ycoord = sp.valueToCoord(y)
            self.coords = self.coords[:2 + idx] + (int(ycoord),) + self.coords[3 + idx:]
        self.updatePlots()

    @ifactive
    def _ondrag(self, event):
        """This is called by the matplotlib `motion_notify_event` event."""
        if event.inaxes is None:  # Don't do anything if the event wasn't within a plot
            return
        if event.button != 1:  # Only respond to a left click.
            return
        self._processMouse(event.inaxes, event.xdata, event.ydata)

    def setColorMap(self, cmap: typing.Union[str, mpl.colors.Colormap]):
        """
        Set the colormap used to display data.

        Args:
             cmap: This value will be have the same effect as the argument of Matplotlib's `AxesImage.set_cmap()`
        """
        self.image.im.set_cmap(cmap)
        #TODO update the colormap too.