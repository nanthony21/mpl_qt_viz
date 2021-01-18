from mpl_qt_viz.visualizers import PlotNd
import numpy as np
from PyQt5.QtWidgets import QApplication
import sys

# Generate a 3-dimensional dimension array with numpy.meshgrid.
# The Plot Nd Widget supports higher dimensionality as well.
x = np.linspace(0, 1, num=75)
y = np.linspace(0, 1, num=100)
z = np.linspace(0, 3, num=40)
X, Y, Z = np.meshgrid(x, y, z)
# Create a 3-dimensional example data array.
arr = np.sin(2 * np.pi * 1 * Z) + .5 * X + np.cos(2 * np.pi * 4 * Y)

#Run an application with the PlotNd widget
app = QApplication(sys.argv)
p = PlotNd(data=arr,
           names=('Dim1', 'D2', 'D3'),  # Manually sets how each dimension is labeled.
           indices=[y, x, z])  # Specifies the data range for each dimension.
p.setColorMap('plasma')
sys.exit(app.exec_())
