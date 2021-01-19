
if __name__ == '__main__':
    # Just run a quick test
    import numpy as np
    import sys
    from PyQt5.QtWidgets import QApplication

    from mpl_qt_viz.visualizers import PlotNd, DockablePlotWindow
    import mpl_qt_viz.roiSelection as roi
    import matplotlib.pyplot as plt

    print("Starting test of mpl_qt_viz")
    plt.ion()

    data = np.random.random((20, 20, 20))
    app = QApplication([])
    p = PlotNd(data)

    w = DockablePlotWindow("MyWindow")

    fig, ax = w.subplots("Here", 'left')
    fig2, ax2 = w.subplots("There", 'right')

    ax.plot(np.arange(50), np.random.random((50,)))
    ax2.imshow(data.mean(axis=2))

    fig, ax = plt.subplots()
    im = ax.imshow(data.mean(axis=2))
    ellipse = roi.EllipseCreator(ax, im)
    ellipse.set_active(True)

    sys.exit(app.exec())