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
from PyQt5 import QtCore
from PyQt5.QtWidgets import QMainWindow, QApplication, QDockWidget, QWidget, QGridLayout, QMenuBar, QFileDialog
import matplotlib.pyplot as plt
from matplotlib.backends.backend_qt5 import NavigationToolbar2QT
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg


class DockablePlotWindow(QMainWindow):
    DEFAULT_FIG_SIZE = (6.4, 4.8)  # Got this from https://matplotlib.org/api/_as_gen/matplotlib.figure.Figure.html#matplotlib-figure-figure
    """
    A window with that can create interactive Matplotlib figures docked within it.

    Args:
        title: The title for the window.
    """
    def __init__(self, title: str = "Dockable Plots"):
        super().__init__(parent=None)
        self.setWindowTitle(title)
        self._plots: t_.List[DockablePlot] = []
        self.setDockOptions(QMainWindow.AnimatedDocks | QMainWindow.AllowNestedDocks | QMainWindow.AllowTabbedDocks | QMainWindow.GroupedDragging)
        self.resize(1024, 768)
        # Set up menu
        self._menu = QMenuBar(self)
        exportMenu = self._menu.addMenu("Export")
        pdfAction = exportMenu.addAction("Save to PDF")
        pdfAction.triggered.connect(self._pdfSaveAction)
        self.setMenuBar(self._menu)

        self.show()

    def subplots(self, title: str, dockArea: str = 'top', **kwargs):
        """
        Create a new docked figure within the main window.

        Args:
            title: The title for the new figure.
            docArea: The side of the window that the new plot should be initially placed in. If a figure has already been
                created on that side of the window then the new figure will be docked with the existing one. Accepted values
                are: 'left', 'right', 'top', and 'bottom'.
            kwargs: Any additional keyword arguments are passed to `pyplot.subplots`

        Returns:
             The return values are the same as the return values of `pyplot.subplots`. Usually taking the form of (figure, axes).
        """
        dockMap = {'top': QtCore.Qt.TopDockWidgetArea, 'bottom': QtCore.Qt.BottomDockWidgetArea,
                    'left': QtCore.Qt.LeftDockWidgetArea, 'right': QtCore.Qt.RightDockWidgetArea}
        try:
            dockArea = dockMap[dockArea]
        except KeyError:
            raise ValueError(f"Dock are `{dockArea}` is not supported. must be: {list(dockMap.keys())}")
        interactive = False
        if plt.isinteractive():
            interactive = True
            plt.ioff()
        fig, ax = plt.subplots(**kwargs)
        if interactive:
            plt.ion()  # Set back to interactive if it originally was.
        fig.suptitle(title)
        suffix = 0
        finalTitle = title
        titles = [i.title for i in self._plots]
        while finalTitle in titles:
            suffix += 1
            finalTitle = f"{title}_{suffix}"
        plot = DockablePlot(fig, finalTitle, self)
        dockAreas = [self.dockWidgetArea(i) for i in self._plots]
        if dockArea not in dockAreas:
            self.addDockWidget(dockArea, plot)
        else:
            existing = self._plots[dockAreas.index(dockArea)]
            self.tabifyDockWidget(existing, plot)
        self._plots.append(plot)
        return fig, ax

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
                fig.set_size_inches(self.DEFAULT_FIG_SIZE) # Set to the original figure size for saving.
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
        self._canv = FigureCanvasQTAgg(figure=figure)
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