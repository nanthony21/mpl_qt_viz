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

"""
A Matplotlib backend that docks every pyplot figure into a shared `DockablePlotWindow`.

Activate it before importing `matplotlib.pyplot`::

    import matplotlib
    matplotlib.use("module://mpl_qt_viz.backends.backend_dockableagg")
    import matplotlib.pyplot as plt

From then on ordinary pyplot code (`plt.subplots()`, `plt.figure("title")`, `plt.plot()`,
`plt.show()`) produces figures that appear as tabs inside one `DockablePlotWindow` -- no
`QApplication` boilerplate required. Use `newWindow()` to open a fresh window and route
subsequent figures into it.
"""

import matplotlib as mpl
from matplotlib import _api
from matplotlib.backend_bases import FigureManagerBase
from matplotlib.backends.backend_qt import _BackendQT, FigureManagerQT
from PyQt6 import QtCore

from mpl_qt_viz.visualizers._dockPlot import MyFigureCanvas, DockablePlotWindow

# --- current-window management -------------------------------------------------------
_currentWindow = None


def _get_window() -> DockablePlotWindow:
    """Return the window new figures should dock into, creating one lazily if needed."""
    global _currentWindow
    if _currentWindow is None:
        newWindow("Figures")
    return _currentWindow


def newWindow(title: str = "Figures") -> DockablePlotWindow:
    """
    Open a new `DockablePlotWindow` and make it the target for future pyplot figures.

    Args:
        title: The title for the new window.

    Returns:
        The newly created window.
    """
    global _currentWindow
    win = DockablePlotWindow(title)  # `__init__` already calls `self.show()`
    win.destroyed.connect(_onWindowDestroyed)
    _currentWindow = win
    return win


def setCurrentWindow(win: DockablePlotWindow):
    """Route subsequent pyplot figures into an existing `DockablePlotWindow`."""
    global _currentWindow
    _currentWindow = win


def _onWindowDestroyed(*args):
    # The current window was closed; drop the reference so the next figure builds a fresh one.
    global _currentWindow
    _currentWindow = None


# --- canvas + manager ----------------------------------------------------------------
class DockableFigureManager(FigureManagerQT):
    """A figure manager that docks its canvas into the shared `DockablePlotWindow`."""

    def __init__(self, canvas, num):
        self._dock = None  # set below; guards title accessors called during base __init__
        # Deliberately call FigureManagerBase (grandparent), NOT FigureManagerQT, so that
        # no standalone QMainWindow is created. The base still wires up event handling and
        # builds `self.toolbar`, which we reuse inside the dock.
        FigureManagerBase.__init__(self, canvas, num)
        self._dockWindow = _get_window()
        self.window = self._dockWindow  # kept so any inherited method touching it won't crash
        title = str(canvas.figure.get_label() or num)
        self._dock = self._dockWindow._addCanvasDock(
            canvas, self.toolbar, title, dockArea="top"
        )
        canvas.setFocusPolicy(QtCore.Qt.FocusPolicy.StrongFocus)
        canvas.setFocus()

    def show(self):
        self._dockWindow.show()
        if mpl.rcParams["figure.raise_window"]:
            self._dockWindow.activateWindow()
            self._dockWindow.raise_()

    def destroy(self, *args):
        try:
            self._dockWindow._removeDock(self._dock)
        except RuntimeError:
            # The underlying Qt window was already deleted (e.g. during interpreter
            # shutdown after the user closed it); nothing left to remove.
            pass
        FigureManagerBase.destroy(self)

    def resize(self, width, height):
        # Resize the canvas widget only -- the base implementation resizes the whole window,
        # which here is the shared window hosting every figure.
        dpr = self.canvas.device_pixel_ratio
        self.canvas.resize(int(width / dpr), int(height / dpr))

    def get_window_title(self):
        if self._dock is None:
            return None
        return self._dock.windowTitle()

    def set_window_title(self, title):
        # May be called by the base __init__ before the dock exists; the real title is set
        # from the figure label when the dock is created.
        if self._dock is not None:
            self._dock.setWindowTitle(title)


class DockableFigureCanvas(MyFigureCanvas):
    """The debounced Qt-agg canvas, bound to the dockable figure manager."""

    manager_class = _api.classproperty(lambda cls: DockableFigureManager)


@_BackendQT.export
class _BackendDockableAgg(_BackendQT):
    FigureCanvas = DockableFigureCanvas
    FigureManager = DockableFigureManager
    # `mainloop` is inherited from `_BackendQT` (FigureManagerQT.start_main_loop).
