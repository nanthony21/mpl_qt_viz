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


from typing import List

from PyQt5 import QtCore
from PyQt5.QtWidgets import QWidget, QGridLayout, QPushButton, QApplication
import numpy as np
from matplotlib.artist import Artist
from matplotlib.axes import Axes
from matplotlib.backends.backend_qt5 import NavigationToolbar2QT
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg
from matplotlib.figure import Figure
import matplotlib.pyplot as plt
from ._sharedWidgets import AnimationDlg


class MultiPlot(QWidget):
    """
    A widget that allows the user to flip through a set of matplotlib artists (images, plots, etc.)

    Args:
        artists: A list of lists of matplotlib 'Artists`. each list will comprise a single frame, just like the matplotlib `ArtistAnimation` works.
        title (str): The name for the title of the window
    """
    def __init__(self, artists: List[List[Artist]], title: str, parent=None):
        QWidget.__init__(self, parent=parent, flags=QtCore.Qt.Window)
        self.setWindowTitle(title)
        layout = QGridLayout()
        self._artists = artists
        self.figure: Figure = artists[0][0].figure  # We are assuming that all artists use the same figure.
        self.ax: Axes = self._artists[0][0].axes

        self._canvas = FigureCanvasQTAgg(self.figure)
        self._canvas.setFocusPolicy(QtCore.Qt.ClickFocus) #Not sure what this is for
        self._canvas.setFocus()

        self.previousButton = QPushButton('←')
        self.nextButton = QPushButton('→')
        self.previousButton.released.connect(self.showPreviousIm)
        self.nextButton.released.connect(self.showNextIm)

        self.saveButton = QPushButton("Save Animation")
        self.saveButton.released.connect(lambda: AnimationDlg(self.figure, self._artists, self).exec())

        layout.addWidget(self._canvas, 0, 0, 8, 8)
        layout.addWidget(self.previousButton, 9, 1, 1, 1)
        layout.addWidget(self.nextButton, 9, 2, 1, 1)
        layout.addWidget(self.saveButton, 9, 7, 1, 1)
        layout.addWidget(NavigationToolbar2QT(self._canvas, self), 10, 0, 1, 4)

        layout.setRowStretch(0, 1)  # This causes the plot to take up all the space that isn't needed by the other widgets.
        self.setLayout(layout)

        self._index = 0  # Keeps track of which frame we are currently viewing.
        self._updateDisplayedImage()
        plt.close(self.figure)  # A separate figure window will have been opened during the creation of our artists. This is extra and should be closed.
        self.show()

    def showPreviousIm(self):
        """Display the previous set of display elements."""
        self._index -= 1
        if self._index < 0:
            self._index = len(self._artists) - 1
        self._updateDisplayedImage()

    def showNextIm(self):
        """Display the next set of display elements."""
        self._index += 1
        if self._index >= len(self._artists):
            self._index = 0
        self._updateDisplayedImage()

    def imshow(self, *args, **kwargs):
        """Mirrors the pyplot.imshow function. Adds a new image to the set of images shown by this widget."""
        self._artists.append([self.ax.imshow(*args, **kwargs)])
        self._index = len(self._artists) - 1
        self._updateDisplayedImage()

    def _updateDisplayedImage(self):
        for i, frame in enumerate(self._artists):
            for artist in frame:
                artist.set_visible(self._index == i)
        self._canvas.draw_idle()


if __name__ == '__main__':
    import sys
    import matplotlib.pyplot as plt
    app = QApplication(sys.argv)
    sh = (1024, 1024)
    ims = [[plt.imshow(np.random.random(sh)), plt.text(100, 100, str(i))] for i in range(3)]
    mp = MultiPlot(ims, "Hey")
    plt.gcf().subplots_adjust(left=0, bottom=0, right=1, top=1, wspace=0, hspace=0)
    mp.ax.get_xaxis().set_visible(False)
    mp.ax.get_yaxis().set_visible(False)
    [mp.imshow(np.random.random(sh)) for i in range(3)]
    mp.show()

    fig, ax = plt.subplots()
    lines = [ax.plot(np.random.random((50,))) for i in range(3)]
    mp2 = MultiPlot(lines, 'Lines')
    mp2.show()

    sys.exit(app.exec())
