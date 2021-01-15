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

import os
import traceback
from enum import Enum
from typing import List, Union, Callable, Tuple, Iterable

from PyQt5 import QtGui
from PyQt5.QtWidgets import QDialog, QWidget, QSpinBox, QLineEdit, QPushButton, QComboBox, QVBoxLayout, QHBoxLayout, \
    QLabel, QMessageBox, QFileDialog, QFileIconProvider
from matplotlib import animation
from matplotlib.artist import Artist


class AnimationDlg(QDialog):
    """A dialog box that facilitates the saving an animation.
    Args:
        fig (Figure): The figure to save the animation from.
        input (list(list(Artists)) or tuple(Callable, Iterable)): If this is a list of lists of Artists then it will be passed to matplotlib.animation.ArtistAnimation which
            will be used to save the animation. If this is a tuple of a function and an iterable then the function will be passed to FuncAnimation where the iterable will be passed
            to the `frames` argument.
        parent (QWidget): The widget that this dialog will act as the child for.
    """
    class SaveMethods(Enum):
        MP4 = 'ffmpeg'
        GIF = 'pillow'
        HTML = 'html'

    Extensions = {SaveMethods.GIF: '.gif', SaveMethods.HTML: '.html', SaveMethods.MP4: '.mp4'}

    def __init__(self, fig, input: Union[List[List[Artist]], Tuple[Callable, Iterable]], parent: QWidget):
        super().__init__(parent)
        self.setModal(True)
        self.setWindowTitle("Save Animation")

        self.input = input
        self.figure = fig

        self.intervalSpinBox = QSpinBox(self)
        self.intervalSpinBox.setMinimum(0)
        self.intervalSpinBox.setMaximum(10000)
        self.intervalSpinBox.setSingleStep(50)
        self.intervalSpinBox.setValue(100)

        self.fPath = QLineEdit(self)

        self.browseButton = QPushButton(QFileIconProvider().icon(QFileIconProvider.Folder), '')
        self.browseButton.released.connect(self.browseFile)

        self.methodCombo = QComboBox(self)
        [self.methodCombo.addItem(i.name, i) for i in self.SaveMethods]

        self.saveButton = QPushButton("Save", self)
        self.saveButton.released.connect(self.save)

        layout = QVBoxLayout()
        bottomLay = QHBoxLayout()

        lay = QHBoxLayout()
        lay.addWidget(QLabel("Frame Interval (ms):"))
        lay.addWidget(self.intervalSpinBox)
        layout.addLayout(lay)

        lay = QHBoxLayout()
        lay.addWidget(self.fPath)
        lay.addWidget(self.browseButton)
        layout.addLayout(lay)

        bottomLay.addStretch()
        bottomLay.addWidget(self.methodCombo)
        bottomLay.addWidget(self.saveButton)
        bottomLay.addStretch()
        layout.addLayout(bottomLay)

        self.setLayout(layout)

    def save(self):
        """Save the animation to file depending on the settings of the dialog."""
        try:
            saveMethod = self.methodCombo.currentData()
            savePath = self.fPath.text()
            frameIntervalMs = self.intervalSpinBox.value()
            if os.path.splitext(savePath)[1] != self.Extensions[saveMethod]:  # Make sure we have the right file extension to avoid an error.
                savePath += self.Extensions[saveMethod]
            if callable(self.input[0]):
                ani = animation.FuncAnimation(self.figure, self.input[0], frames=self.input[1], interval=frameIntervalMs)
            else:
                ani = animation.ArtistAnimation(self.figure, self.input, interval=frameIntervalMs)
            Writer = animation.writers[saveMethod.value]
            if Writer is animation.FFMpegWriter:
                writer = Writer(bitrate=-1, fps=1000/frameIntervalMs)  # We previously had codec='libx264' here to improve quality. But starting in matplotlib 3.3.1 this prevented the videos from working on windows.
            else:
                writer = Writer(fps=1000/frameIntervalMs)
            ani.save(savePath, writer=writer)
        except Exception as e:
            traceback.print_exc()
            msg = QMessageBox.warning(self, 'Warning', str(e))
        self.accept()

    def browseFile(self):
        fname, extension = QFileDialog.getSaveFileName(self, 'Save Location', os.getcwd())
        if fname != '':
            self.fPath.setText(fname)