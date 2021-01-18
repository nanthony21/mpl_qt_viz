import sys
import matplotlib.pyplot as plt
from PyQt5.QtWidgets import QApplication
import numpy as np
from mpl_qt_viz.visualizers import MultiPlot

app = QApplication(sys.argv)

# Generate a list of lists of artists and create a new MultiPlot with them.
ims = [[plt.imshow(np.random.random((512, 512))), plt.text(100, 100, str(i))] for i in range(3)]
mp = MultiPlot(ims, "Images")

#Adjust the figure and axes
plt.gcf().subplots_adjust(left=0, bottom=0, right=1, top=1, wspace=0, hspace=0)
mp.ax.get_xaxis().set_visible(False)
mp.ax.get_yaxis().set_visible(False)
mp.show()  # Show the widget

#Create a second MultiPlot with line plots
fig, ax = plt.subplots()
lines = [ax.plot(np.random.random((50,))) for i in range(3)]
mp2 = MultiPlot(lines, 'Lines')
mp2.show()

sys.exit(app.exec())