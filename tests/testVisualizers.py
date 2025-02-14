from mpl_qt_viz.visualizers import PlotNd, DockablePlotWindow, MultiPlot
from PyQt6.QtWidgets import QApplication
import matplotlib.pyplot as plt
import numpy as np
import random


class TestVisualizers:
    def test_multiplot(self, qapplication):
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
        qapplication.exec()

    def test_plotnd(self, qapplication):
        print("Starting")
        x = np.linspace(0, 1, num=100)
        y = np.linspace(0, 1, num=50)
        z = np.linspace(0, 3, num=101)
        # t = np.linspace(0, 1, num=3)
        # c = np.linspace(12, 13, num=3)
        X, Y, Z = np.meshgrid(x, y, z)
        arr = np.sin(2 * np.pi * 1 * Z) + .5 * X + np.cos(2 * np.pi * 4 * Y)  # * T**1.5 * C*.1
        p = PlotNd(arr[:, :, :], names=('y', 'x', 'z'), indices=[y, x, z])  # 3d
        # p2 = PlotNd(arr[:,:,:,:,0], names=('y', 'x', 'z', 't'), indices=[y, x, z, t]) #4d
        # p3 = PlotNd(arr, names=('y', 'x', 'z', 't', 'c'), indices=[y, x, z, t, c]) #5d
        qapplication.exec()

    def test_dockable_plots(self, qapplication):
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

        qapplication.exec()
