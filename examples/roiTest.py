from PyQt5.QtWidgets import QWidget, QFrame, QHBoxLayout, QPushButton, QVBoxLayout, QApplication, QButtonGroup, \
    QScrollArea
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg
import matplotlib.pyplot as plt
from mpl_qt_viz.roiSelection import EllipseCreator, LassoCreator, RegionalPaintCreator, SquareCreator,\
    FullImPaintCreator, WaterShedPaintCreator, PointCreator, CreatorWidgetBase
import numpy as np


creatorClasses = [EllipseCreator, LassoCreator, RegionalPaintCreator, SquareCreator,
    FullImPaintCreator, WaterShedPaintCreator, PointCreator]


class TestWidg(QWidget):
    def __init__(self):
        super().__init__()
        fig, ax = plt.subplots()
        self._canvas = FigureCanvasQTAgg(figure=fig)

        X, Y = np.meshgrid(np.linspace(-1, 1, num=1024), np.linspace(-1, 1, num=1024))
        arr = np.sin(5*X) + np.cos(6*Y)
        im = ax.imshow(arr)

        onSelection = lambda coords, coords2: print(coords)

        self._activeSelector: CreatorWidgetBase = None
        creators = [clazz(ax, im, onSelection) for clazz in creatorClasses]

        buttonWidg = QFrame(self)
        buttonWidg.setLayout(QVBoxLayout())
        buttonGrp = QButtonGroup(self)
        for creator in creators:
            creator.set_active(False)
            button = QPushButton(creator.__class__.__name__)
            button.setCheckable(True)
            buttonGrp.addButton(button)
            button.setToolTip(creator.getHelpText())
            button.released.connect(lambda creat=creator: self._changeActive(creat))
            buttonWidg.layout().addWidget(button)

        scroll = QScrollArea(self)
        scroll.setWidget(buttonWidg)

        self.setLayout(QHBoxLayout())
        self.layout().addWidget(self._canvas)
        self.layout().addWidget(scroll)

        # activate an initial selector
        buttonGrp.buttons()[0].setChecked(True)
        self._changeActive(creators[0])

    def _changeActive(self, creator: CreatorWidgetBase):
        if self._activeSelector is not None:
            self._activeSelector.set_active(False)
        self._activeSelector = creator
        self._activeSelector.set_active(True)

if __name__ == '__main__':
    app = QApplication([])
    t = TestWidg()
    t.show()
    app.exec()
