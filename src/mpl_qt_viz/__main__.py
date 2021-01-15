
if __name__ == '__main__':
    # Just run a quick test
    import numpy as np
    import sys
    from PyQt5.QtWidgets import QApplication

    from mpl_qt_viz.visualizers import PlotNd, DockablePlotWindow

    print("Starting test of mpl_qt_viz")

    data = np.random.random((20, 20, 20))
    app = QApplication([])
    p = PlotNd(data)

    w = DockablePlotWindow("MyWindow")

    fig, ax = w.subplots("Here", 'left')
    fig2, ax2 = w.subplots("There", 'right')

    ax.plot(np.arange(50), np.random.random((50,)))
    ax2.imshow(data.mean(axis=2))

    sys.exit(app.exec())