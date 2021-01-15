from PyQt5 import QtCore
from PyQt5.QtWidgets import QWidget, QLabel, QSlider, QHBoxLayout


class LabeledSlider(QWidget):
    """A slider with a label that indicates the current value."""
    def __init__(self, Min, Max, Step, Value, parent=None):
        super().__init__(parent)
        self.display = QLabel(self)
        self.slider = QSlider(QtCore.Qt.Horizontal, self)

        self.slider.valueChanged.connect(lambda val: self.display.setText(str(val)))

        self.setMaximum = lambda val: self.slider.setMaximum(val)
        self.setMinimum = lambda val: self.slider.setMinimum(val)
        self.setSingleStep = lambda val: self.slider.setSingleStep(val)
        self.setValue = lambda val: self.slider.setValue(val)
        self.value = lambda: self.slider.value()
        self.valueChanged = self.slider.valueChanged

        l = QHBoxLayout()
        l.setContentsMargins(0, 0, 0, 0)
        l.addWidget(self.slider)
        l.addWidget(self.display)
        l.setStretch(0, 0)
        l.setStretch(1, 1)
        self.setLayout(l)

        self.setMinimum(Min)
        self.setMaximum(Max)
        self.setSingleStep(Step)
        self.setValue(Value)