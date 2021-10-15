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
import matplotlib as mpl
from PyQt5 import QtCore, QtGui
from PyQt5.QtCore import QSizeF, QTimer
from PyQt5.QtWidgets import QWidget, QGridLayout, QApplication, QPushButton, QGraphicsView, \
    QGraphicsScene, QGroupBox, QVBoxLayout, QCheckBox, QButtonGroup
from matplotlib import pyplot

from matplotlib.backends.backend_qt5 import NavigationToolbar2QT, FigureCanvasQT
import numpy as np
from mpl_qt_viz.roiSelection import LassoCreator, SquareCreator, AdjustableSelector, PointCreator
from mpl_qt_viz.visualizers._PlotNd._canvas import PlotNdCanvas
from mpl_qt_viz.visualizers._sharedWidgets import AnimationDlg, QRangeSlider


class _MyView(QGraphicsView):
    """This is a version of QGraphicsView that takes a Qt FigureCanvas from matplotlib and automatically resized the
    canvas to fill as much of the view as possible. A debounce timer is used to prevent lag due to attempting the resize
    the canvas too quickly. This allows for relatively smooth operation. This is essential for us to include a matplotlib
    plot that can maintain it's aspect ratio within a Qt layout.

    Args:
        plot: A matplotlib FigureCanvas that is compatible with Qt (FigureCanvasQT or FigureCanvasQTAgg)

    """
    def __init__(self, plot: FigureCanvasQT):
        super().__init__()
        self.setHorizontalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOff)
        self.setVerticalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOff)

        scene = QGraphicsScene(self)
        scene.addWidget(plot)
        self.plot = plot
        self.setScene(scene)
        self._debounce = QTimer()  # If the resizeEvent doesn't reset the timer within the 50ms timeout interval then _resizePlot will be called.
        self._debounce.setSingleShot(True)
        self._debounce.setInterval(50)
        self._debounce.timeout.connect(self._resizePlot)

    def _resizePlot(self):
        """This method is indirectly called by the resizeEvent through the debounce timer and sets the size of the plot
        to maximize its size without changing aspect ratio."""
        w, h = self.size().width(), self.size().height()
        r = self.scene().sceneRect()
        s = min([w, h])  # Get the side length of the biggest square that can fit within the rectangle view area.
        self.plot.resize(s, s)  # Set the plot to the size of the square that fits in view.
        r.setSize(QSizeF(s, s))
        self.scene().setSceneRect(r)  # Set the scene size to the square that fits in view.

    def resizeEvent(self, event: QtGui.QResizeEvent):
        """Every time that the view is resized this event will fire and start the debounce timer. The timer will only
        actually time out if this event doesn't restart it within the timeout period."""
        self._debounce.start()
        super().resizeEvent(event)


class PlotNd(QWidget):  # TODO add function and GUI method to set coordinates of cursor.
    """A convenient widget for visualizing data that is 3D or greater. This is a standalone widget which extends the
    functionality of `PlotNdCanvas`.

    Args:
        data: A 3D or greater numpy array of numeric values.
        names: A sequence of labels for each axis of the data array.
        initialCoords: An optional sequence of the coordinates to initially se the ND crosshair to. There should be one
            coordinate for each axis of the data array.
        title: A title for the window.
        parent: The Qt Widget that serves as the parent for this widget.
        indices: An optional tuple of 1d arrays of values to set as the indexes for each dimension of the data. Elements of the list can be set to `None` to skip
            setting a custom index for that dimension.
        flags: See the `flags` constructor argument for a QWidget. Default value is `Window`

    Attributes:
        data: A reference the the 3D or greater numpy array. This can be safely modified.
    """
    _defaultNames = ('y', 'x', 'z', '4th', '5th', '6th', '7th', '8th', '9th', '10th', '11th')

    def __init__(self, data: np.ndarray, names: t_.Tuple[str, ...] = None,
                 initialCoords: t_.Optional[t_.Tuple[int, ...]] = None, title: t_.Optional[str] = '',
                 parent: t_.Optional[QWidget] = None, indices: t_.Sequence[np.ndarray] = None, flags=QtCore.Qt.Window):
        super().__init__(parent=parent, flags=flags)


        self.setWindowTitle(str(title))  # Convert to string just in case

        if names is None:
            names = PlotNd._defaultNames[:len(data.shape)]

        if data.dtype == bool:
            data = data.astype(np.uint8)

        self.canvas = PlotNdCanvas(data, names, initialCoords, indices)
        self.view = _MyView(self.canvas)
        self.slider = QRangeSlider(self)
        self.slider.setMaximumHeight(20)
        self.slider.setMax(np.nanmax(data))
        self.slider.setMin(np.nanmin(data))
        self.slider.setEnd(np.nanmax(data))
        self.slider.setStart(np.nanmin(data))

        _ = lambda: self.canvas.updateLimits(self.slider.end(), self.slider.start())
        self.slider.startValueChanged.connect(_)
        self.slider.endValueChanged.connect(_)

        self._lastButton = None
        self.selector = AdjustableSelector(self.canvas.image.ax, self.canvas.image.im, LassoCreator,
                                           onfinished=self._selectorFinished)

        self.buttonWidget = QGroupBox("Control", self)
        self.buttonWidget.setLayout(QVBoxLayout())
        check = QCheckBox("Cursor Active")
        self.buttonWidget.layout().addWidget(check)
        check.setChecked(self.canvas.spectraViewActive)  # Get the right initial value
        check.stateChanged.connect(lambda state: self.canvas.setSpectraViewActive(state != 0))

        self.buttonGroup = QButtonGroup()
        self.pointButton = QPushButton("Point")
        self.buttonGroup.addButton(self.pointButton)
        self.buttonWidget.layout().addWidget(self.pointButton)

        self.lassoButton = QPushButton("Lasso")
        self.buttonGroup.addButton(self.lassoButton)
        self.buttonWidget.layout().addWidget(self.lassoButton)

        self.noneButton = QPushButton("None")
        self.buttonGroup.addButton(self.noneButton)
        self.buttonWidget.layout().addWidget(self.noneButton)

        for b in self.buttonGroup.buttons():
            b.setCheckable(True)
        self.noneButton.setChecked(True)
        self.buttonGroup.buttonReleased.connect(self._handleButtons)

        self.rotateButton = QPushButton("Rotate Axes")
        self.rotateButton.released.connect(self.canvas.rollAxes)

        self.saveButton = QPushButton("Save Animation")
        self.saveButton.released.connect(self._saveAnimation)

        layout = QGridLayout()
        layout.addWidget(self.view, 0, 0, 8, 8)
        layout.addWidget(self.buttonWidget, 0, 8, 4, 1)
        layout.addWidget(self.rotateButton, 5, 8)
        layout.addWidget(self.saveButton, 6, 8)
        layout.addWidget(NavigationToolbar2QT(self.canvas, self), 10, 0, 1, 8)
        layout.setRowStretch(0, 1)
        layout.addWidget(self.slider, 8, 0, 1, 7)
        self.setLayout(layout)

        self.show()

    def _saveAnimation(self):
        def animationUpdaterFunc(z: int):
            """Used by the animation saver to iterate through the 3rd dimension of the data."""
            self.canvas.coords = self.canvas.coords[:2] + (z,) + self.canvas.coords[3:]
            self.canvas.updatePlots()

        dlg = AnimationDlg(self.canvas.fig, (animationUpdaterFunc, range(self.canvas.data.shape[2])), self)
        dlg.exec()

    def _updateLimits(self):
        """"""
        self.canvas.updateLimits(self.slider.end(), self.slider.start())

    def _handleButtons(self, button: QPushButton):
        """Acts as a callback when one of the ROI drawing buttons is pressed. Activates the corresponding ROI selector

        Args:
            button: The button that was just pressed.
        """
        if button is self.pointButton and button is not self._lastButton:
            self.selector.setSelector(PointCreator)
            self.selector.setActive(True)
        if button is self.lassoButton and button is not self._lastButton:
            self.selector.setSelector(LassoCreator)
            self.selector.setActive(True)
        if button is self.noneButton and button is not self._lastButton:
            self.selector.setActive(False)

        self._lastButton = button

    def _selectorFinished(self, verts: np.ndarray):
        """When an ROI selector finishes selecting a region the vertex coordinates of the selection are passed to this
        function. The function then uses the vertices to plot the average of the data in the ROI"""
        import cv2
        newVerts = []
        for vert in verts:  # Convert `verts` from being in terms of the values in self.canvas._indexes to being in terms of the element locations of the data array.
            v1 = self.canvas.image.verticalValueToCoord(vert[1])
            v0 = self.canvas.image.horizontalValueToCoord(vert[0])
            newVerts.append((v0, v1))
        verts = newVerts

        # Convert from vertices to a boolean mask
        iVerts = np.rint([verts]).astype(np.int32)  # The brackets here convert to a 3d array which is what cv2.fillpoly expects. We have to round to integers for cv2 to work.
        mask = np.zeros(self.canvas.data.shape[:2], dtype=np.int32)
        cv2.fillPoly(mask, iVerts, 1)
        mask = mask.astype(bool)

        selected = self.canvas.data[mask]  # For a 3d data array this will now be 2d . For a 4d array it will be 3d etc. The 0th axis is one element for each selected pixel.
        selected = selected.mean(axis=0)  # Get the average over all selected pixels. We are now down to 1d for a 3d data array, 2d for a 4d data array, et.
        if len(selected.shape) == 1:
            fig, ax = pyplot.subplots()
            ax.plot(self.canvas.indexes[2], selected)
            ax.set_xlabel(self.canvas.names[2])
            fig.show()
        elif len(selected.shape) == 2:
            fig, ax = pyplot.subplots()
            im = ax.imshow(selected)
            im.set_extent([self.canvas.indexes[3][0], self.canvas.indexes[3][-1], self.canvas.indexes[2][0], self.canvas.indexes[2][-1]])
            ax.set_xlabel(self.canvas.names[3])
            ax.set_ylabel(self.canvas.names[2])
            fig.show()
        else:  # selected must be 3d or greater. This means our original data was 5d or greater.
            p = PlotNd(selected, names=self.canvas.names[2:], indices=self.canvas.indexes[2:])

        self.selector.setActive(True)  # Reset the selector.

    # API
    @property
    def data(self):
        return self.canvas.data

    @data.setter
    def data(self, data: np.ndarray):
        self.canvas.data = data

    def setLimits(self, Min: float, Max: float):
        """
        Set the limits of the colormap.

        Args:
             Min: The data value that will correspond to the minimum of the colormap.
             Max: The data value that will correspond to the maximum of the colormap.
        """
        return self.canvas.updateLimits(Max, Min)

    def setColorMap(self, cmap: t_.Union[str, mpl.colors.Colormap]):
        """
         Set the colormap used to display data.

         Args:
              cmap: This value will be have the same effect as the argument of Matplotlib's `AxesImage.set_cmap()`
         """
        self.canvas.setColorMap(cmap)


if __name__ == '__main__':
    import sys
    print("Starting")
    x = np.linspace(0, 1, num=100)
    y = np.linspace(0, 1, num=50)
    z = np.linspace(0, 3, num=101)
    # t = np.linspace(0, 1, num=3)
    # c = np.linspace(12, 13, num=3)
    X, Y, Z = np.meshgrid(x, y, z)
    arr = np.sin(2 * np.pi * 1 * Z) + .5 * X + np.cos(2*np.pi*4*Y)# * T**1.5 * C*.1
    app = QApplication(sys.argv)
    p = PlotNd(arr[:,:,:], names=('y', 'x', 'z'), indices=[y, x, z])  # 3d
    # p = PlotNd(arr[:,:,:,:,0], names=('y', 'x', 'z', 't'), indices=[y, x, z, t]) #4d
    # p = PlotNd(arr, names=('y', 'x', 'z', 't', 'c'), indices=[y, x, z, t, c]) #5d
    sys.exit(app.exec_())

