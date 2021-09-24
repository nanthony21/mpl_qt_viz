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

import typing as t_
import os
from PyQt5 import QtCore, QtGui
from PyQt5.QtCore import QTimer
from PyQt5.QtWidgets import QMainWindow, QApplication, QDockWidget, QWidget, QGridLayout, QMenuBar, QFileDialog
import matplotlib.pyplot as plt
from matplotlib.backend_bases import ResizeEvent
from matplotlib.backends.backend_qt5 import NavigationToolbar2QT
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg


class MyFigureCanvas(FigureCanvasQTAgg):
    """ Subclass canvas to catch the resize event. Resizes are debounced out to a default of 50 ms. """
    def __init__(self, figure: plt.Figure, resizeDelayMs: int = 100):
        super().__init__(figure)
        self._debounce = QTimer(self)
        self._debounce.setInterval(resizeDelayMs)
        self._debounce.setSingleShot(True)
        self._debounce.timeout.connect(self._resize)
        self._ev = None

    def resizeEvent(self, event):
        # store the event size for later use
        self._ev = event.size()
        self._debounce.start()

    def _resize(self):
        event = QtGui.QResizeEvent(self._ev, QtCore.QSize(1, 1))
        super().resizeEvent(event)


class DockablePlotWindow(QMainWindow):
    _DEFAULT_FIG_SIZE = (6.4, 4.8)  # Got this from https://matplotlib.org/api/_as_gen/matplotlib.figure.Figure.html#matplotlib-figure-figure
    _DOCKAREAMAP = {'top': QtCore.Qt.TopDockWidgetArea, 'bottom': QtCore.Qt.BottomDockWidgetArea,
               'left': QtCore.Qt.LeftDockWidgetArea, 'right': QtCore.Qt.RightDockWidgetArea}
    """
    A window with that can create interactive Matplotlib figures docked within it.

    Args:
        title: The title for the window.
    """
    def __init__(self, title: str = "Dockable Plots"):
        super().__init__(parent=None)
        self.setWindowTitle(title)
        self._plots: t_.List[DockablePlot] = []  # A list of all added DockablePlots
        self._dockedWidgets: t_.List[GenericDockableWidget] = []  # List of all add dock widgets that are not plots.
        self.setDockOptions(QMainWindow.AnimatedDocks | QMainWindow.AllowNestedDocks | QMainWindow.AllowTabbedDocks | QMainWindow.GroupedDragging)
        self.resize(1024, 768)
        # Set up menu
        self._menu = QMenuBar(self)
        exportMenu = self._menu.addMenu("Export")
        pdfAction = exportMenu.addAction("Save to PDF")
        pdfAction.triggered.connect(self._pdfSaveAction)
        self.setMenuBar(self._menu)

        self.show()

    @property
    def _docked(self) -> t_.List[QDockWidget]:
        """Provides quick access to a list of all dock widgets that have been added regardless of type."""
        return self._plots + self._dockedWidgets

    def addWidget(self, widget: QWidget, title: str, dockArea: str = 'top'):
        """
        Add any Qt widget to a dockable widget in our window.
        
        Args:
            widget: Any Qt Widget
            title: The title of the new dockable widget.
            dockArea: The dock area of the window to add the dockable widget to.

        """
        try:
            dockArea = self._DOCKAREAMAP[dockArea]
        except KeyError:
            raise ValueError(f"Dock are `{dockArea}` is not supported. must be: {list(self._DOCKAREAMAP.keys())}")
        dockWidg = GenericDockableWidget(widget, title, parent=self)
        self._addDockToArea(dockWidg, dockArea)
        self._dockedWidgets.append(dockWidg)
        
    def addFigure(self, fig: plt.Figure, title: str, dockArea: str = 'top'):
        """
        Add a pre-existing Matplotlib Figure to a new dockable widget in the window.
        
        Args:
             fig: A pre-existing Matplotlib Figure
             title: The title for the new dockable widget
             dockArea: The side of the window that the new plot should be initially placed in. If a figure has already been
                created on that side of the window then the new figure will be docked with the existing one. Accepted values
                are: 'left', 'right', 'top', and 'bottom'.
        """
        try:
            dockArea = self._DOCKAREAMAP[dockArea]
        except KeyError:
            raise ValueError(f"Dock are `{dockArea}` is not supported. must be: {list(self._DOCKAREAMAP.keys())}")
        suffix = 0
        finalTitle = title
        titles = [i.title for i in self._plots]
        while finalTitle in titles:
            suffix += 1
            finalTitle = f"{title}_{suffix}"
        plot = DockablePlot(fig, finalTitle, self)
        self._addDockToArea(plot, dockArea)
        self._plots.append(plot)

    def subplots(self, title: str, dockArea: str = 'top', subplots_kwargs: dict = None, subplot_kw: dict = None):
        """
        Create a new docked figure within the main window.

        Args:
            title: The title for the new figure.
            dockArea: The side of the window that the new plot should be initially placed in. If a figure has already been
                created on that side of the window then the new figure will be docked with the existing one. Accepted values
                are: 'left', 'right', 'top', and 'bottom'.
            subplots_kwargs: This dictionary will be passed as the kwargs for `pyplot.subplots`
            subplot_kw: This dictionary will be passed to the `subplot_kw` arg of `pyplot.subplots`

        Returns:
             The return values are the same as the return values of `pyplot.subplots`. Usually taking the form of (figure, axes).
        """
        if subplot_kw is None:
            subplot_kw = {}
        if subplots_kwargs is None:
            subplots_kwargs = {}
        interactive = False
        if plt.isinteractive():  # Turn of interactive mode so our new figure doesn't automatically appear in it's own window.
            interactive = True
            plt.ioff()
        fig, ax = plt.subplots(subplot_kw=subplot_kw, **subplots_kwargs)
        if interactive:
            plt.ion()  # Set back to interactive if it originally was.
        fig.suptitle(title)
        self.addFigure(fig, title, dockArea=dockArea)
        # suffix = 0
        # finalTitle = title
        # titles = [i.title for i in self._plots]
        # while finalTitle in titles:
        #     suffix += 1
        #     finalTitle = f"{title}_{suffix}"
        # plot = DockablePlot(fig, finalTitle, self)
        # self._addDockToArea(plot, dockArea)
        # self._plots.append(plot)
        return fig, ax

    def _addDockToArea(self, dock: QDockWidget, dockArea):
        dockAreas = [self.dockWidgetArea(i) for i in self._docked]
        if dockArea not in dockAreas:
            self.addDockWidget(dockArea, dock)
        else:
            existing = self._docked[dockAreas.index(dockArea)]
            self.tabifyDockWidget(existing, dock)

    @property
    def figures(self) -> t_.Dict[str, plt.Figure]:
        """A dictionary of all the dockable figures in this window keyed by their titles."""
        return {i.title: i.figure for i in self._plots}

    def _pdfSaveAction(self):
        """Triggered when the user clicks the save to pdf menu"""
        fName, filterUsed = QFileDialog.getSaveFileName(self, "Save PDF", os.path.expanduser('~'), "PDF (*.pdf)")
        if fName == '':  # Save dialog was cancelled
            return
        self.saveToPDF(fName)

    def saveToPDF(self, filePath: str):  # TODO make this callable from a Qt menubar
        import datetime
        from matplotlib.backends.backend_pdf import PdfPages
        if not filePath.endswith(".pdf"):
            filePath = f"{filePath}.pdf"
        with PdfPages(filePath) as pdf:
            for k, fig in self.figures.items():
                origSize = fig.get_size_inches()
                fig.set_size_inches(self._DEFAULT_FIG_SIZE) # Set to the original figure size for saving.
                pdf.savefig(fig)  # saves the current figure into a pdf page
                fig.set_size_inches(*origSize)  # Go back to the original size.

            # We can also set the file's metadata via the PdfPages object:
            d = pdf.infodict()
            d['Title'] = 'DockablePlotWindow Multipage PDF'
            d['Author'] = 'mpl_qt_viz'
            d['CreationDate'] = datetime.datetime.today()
            d['ModDate'] = datetime.datetime.today()


class DockablePlot(QDockWidget):
    def __init__(self, figure: plt.Figure, title: str, parent: QWidget = None):
        super().__init__(title, parent=parent)
        self._canv = MyFigureCanvas(figure=figure)
        self._canv.setFocusPolicy(QtCore.Qt.ClickFocus)
        self._canv.setFocus()
        self._bar = NavigationToolbar2QT(self._canv, self)
        l = QGridLayout()
        l.addWidget(self._canv, 0, 0)
        l.addWidget(self._bar, 1, 0)
        self._contentWidget = QWidget(self)
        self._contentWidget.setLayout(l)
        self.setWidget(self._contentWidget)

    @property
    def title(self) -> str:
        return self.windowTitle()

    @property
    def figure(self) -> plt.Figure:
        return self._canv.figure


class GenericDockableWidget(QDockWidget):
    def __init__(self, widget: QWidget, title: str, parent: QWidget = None):
        super().__init__(title, parent=parent)
        self.setWidget(widget)


if __name__ == '__main__':
    import numpy as np
    import random

    names = ['plot', 'data', 'bs']
    areas = ['left', 'right', 'bottom', 'top']

    def plot(ax):
        x = np.linspace(0, 1)
        y = np.random.random(x.size)
        ax.plot(x, y, ls='--')

    def im(ax):
        d = np.random.random((50, 50))
        ax.imshow(d)

    funcs = [plot, im]

    app = QApplication([])

    w = DockablePlotWindow()
    for i in range(10):

        fig, ax = w.subplots(random.choice(names), dockArea=random.choice(areas))
        random.choice(funcs)(ax)

    w2 = DockablePlotWindow(title="2nd Plot Window")
    for i in range(10):
        x = np.linspace(0, 1)
        y = np.random.random(x.size)
        fig, ax = w2.subplots(random.choice(names), dockArea=random.choice(areas))
        ax.plot(x, y, ls='--')

    app.exec()

    a = 1