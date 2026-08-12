"""
Using mpl_qt_viz as a Matplotlib backend.

Activating the backend lets ordinary pyplot code render every figure as a tab inside a
shared DockablePlotWindow -- no QApplication boilerplate and no DockablePlotWindow calls.
The backend must be selected before `matplotlib.pyplot` is imported.
"""

import matplotlib

matplotlib.use("module://mpl_qt_viz.backends.backend_dockableagg")

import matplotlib.pyplot as plt
import numpy as np
from mpl_qt_viz.backends.backend_dockableagg import newWindow

# Figures dock into a lazily-created window titled "Figures". The figure label becomes the
# tab title.
plt.figure("Sine")
plt.plot(np.sin(np.linspace(0, 10)))

plt.figure("Image")
plt.imshow(np.random.random((50, 50)))

# subplots() works too -- an unnamed figure is titled by its number.
fig, ax = plt.subplots()
ax.plot(np.cos(np.linspace(0, 10)))

# Open a second window and make it the current target for subsequent figures.
newWindow("Second Group")
plt.figure("Scatter")
plt.scatter(np.random.rand(50), np.random.rand(50))

plt.show(block=True)  # Opens the windows and runs the Qt event loop until they are closed.
