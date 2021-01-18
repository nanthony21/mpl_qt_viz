import numpy as np
import random
from PyQt5.QtWidgets import QApplication
from mpl_qt_viz.visualizers import DockablePlotWindow
import sys

# Plot names that will be randomly selected from in this example
names = ['plot', 'data', 'other']
# Valid plot location specifiers that will be randomly selected from in this example
areas = ['left', 'right', 'bottom', 'top']


def makePlot(ax):
    """Generate a random line plot on ax."""
    x = np.linspace(0, 1)
    y = np.random.random(x.size)
    ax.plot(x, y, ls='--')


def makeImage(ax):
    """Generate a random image plot on ax."""
    d = np.random.random((50, 50))
    ax.imshow(d)


app = QApplication([])  # Make an application for the widgets to run in.

w = DockablePlotWindow()
for i in range(10):
    # Use the widget's `subplots` method to generate matplotlib plots docked in the widget.
    fig, ax = w.subplots(random.choice(names), dockArea=random.choice(areas))
    random.choice([makePlot, makeImage])(ax)

w2 = DockablePlotWindow(title="2nd Plot Window")
for i in range(10):
    x = np.linspace(0, 1)
    y = np.random.random(x.size)
    fig, ax = w2.subplots(random.choice(names), dockArea=random.choice(areas))
    ax.plot(x, y, ls='--')

sys.exit(app.exec())  # Run the application until all windows are closed
