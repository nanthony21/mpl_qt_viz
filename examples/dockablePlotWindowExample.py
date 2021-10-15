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
    x = np.linspace(0, 10)
    # y = np.random.random(x.size)
    freq1 = .5 + np.random.rand()
    freq2 = .5 + np.random.rand()
    ax.plot(x, np.sin(freq1 * x))
    ax.plot(x, np.cos(freq2 * x), ls='--')


def makeImage(ax):
    """Generate a random image plot on ax."""
    freq = 1 + 10 * np.random.rand()
    X, Y = np.meshgrid(np.linspace(-1, 1), np.linspace(-1, 1))
    R = X**2 + Y**2
    arr = np.sin(freq * R)
    ax.imshow(arr, cmap='jet')

plotTypes = [('plot', makePlot), ('image', makeImage)]


app = QApplication([])  # Make an application for the widgets to run in.

w = DockablePlotWindow("My Dockable Plot Window")
for i in range(10):
    name, func = random.choice(plotTypes)
    # Use the widget's `subplots` method to generate matplotlib plots docked in the widget.
    fig, ax = w.subplots(name, dockArea=random.choice(areas))
    func(ax)

w2 = DockablePlotWindow(title="My 2nd Plot Window")
for i in range(10):
    x = np.linspace(0, 1)
    y = np.random.random(x.size)
    fig, ax = w2.subplots(random.choice(names), dockArea=random.choice(areas))
    ax.plot(x, y)

sys.exit(app.exec())  # Run the application until all windows are closed
