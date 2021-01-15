
if __name__ == '__main__':
    # Just run a quick test
    import numpy as np
    from PyQt5.QtWidgets import QApplication

    from mpl_qt_viz.visualizers import PlotNd, DockablePlotWindow

    data = np.random.random((20, 20, 20))
    app = QApplication([])
    p = PlotNd(data)

    w = DockablePlotWindow("MyWindow")

    fig, ax = w.subplots("Here", 'left')
    fig2, ax2 = w.subplots("There", 'right')

    ax.plot(np.arange(50), np.random.random((50,)))
    ax2.imshow(data.mean(axis=2))

    app.exec()