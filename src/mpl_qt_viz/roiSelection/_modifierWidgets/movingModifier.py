# Copyright 2018-2021 Nick Anthony, Backman Biophotonics Lab, Northwestern University
#
# This file is part of mpl_qt_viz.
#
# mpl_qt_viz is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# mpl_qt_viz is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with mpl_qt_viz.  If not, see <https://www.gnu.org/licenses/>.
from __future__ import annotations
import typing
import numpy as np
from matplotlib.axes import Axes
from matplotlib.backend_bases import MouseEvent, KeyEvent
from matplotlib.figure import Figure
from matplotlib.lines import Line2D
from matplotlib.patches import Polygon
from matplotlib.text import Text
from mpl_qt_viz.roiSelection._modifierWidgets._base import ModifierWidgetBase

if typing.TYPE_CHECKING:
    from matplotlib.axes import Axes
    from matplotlib.image import AxesImage


class MovingModifier(ModifierWidgetBase):
    """This iteractive widget allows translating and rotating multiple polygons"""
    def __init__(self, ax: Axes, image: AxesImage = None, onselect: typing.Optional[ModifierWidgetBase.SelectionFunction] = None, onCancelled: typing.Optional[typing.Callable] = None):
        super().__init__(ax, image=image, onselect=onselect)
        self._cancelFunc = onCancelled
        self.initialClickPoint = None  # The coords where a drag was started
        self.indicatorLine = Line2D([0, 0], [0, 0], color='k', linestyle='dashed', animated=True)
        self.angleRefLine = Line2D([0, 0], [0, 0], color='r', animated=True)
        self.angleIndicatorLine = Line2D([0, 0], [0, 0], color='b', animated=True)
        self.transformText = Text(ax.get_xlim()[0], ax.get_ylim()[0], "", animated=True)
        self.addArtist(self.indicatorLine)
        self.addArtist(self.angleRefLine)
        self.addArtist(self.angleIndicatorLine)
        self.addArtist(self.transformText)
        self.setArtistVisible(self.angleIndicatorLine, False)
        self.setArtistVisible(self.angleRefLine, False)
        self.polygonArtists = []

    @staticmethod
    def getHelpText():
        return """Translation/Rotation: Left click and drag to translate the ROI. Shift + left click and drag to rotate. Press 'enter' to accept
        the new location. Press 'esc' to reset."""

    def initialize(self, setOfVerts: typing.Sequence[ModifierWidgetBase.PolygonCoords]):
        [self.removeArtist(artist) for artist in self.polygonArtists]
        self.polygonArtists = []
        self.originalCoords = setOfVerts
        self.affineTransform = np.identity(3)
        self.angle = 0
        self.translation = np.array([0, 0])
        self.initializeRotation = False
        for verts in setOfVerts:
            poly = Polygon(verts, facecolor=(.7, .3, 0, 0.1), linewidth=2, linestyle='dotted', edgecolor=(1, 0, 0, 0.9), animated=True)  # Having animated true here helps with rendering.
            self.addArtist(poly)
            self.polygonArtists.append(poly)

    def _press(self, event: MouseEvent):
        self.initialClickPoint = np.array((event.xdata, event.ydata))
        self.initialTranslation = self.translation

    def _ondrag(self, event: MouseEvent):
        mousePoint = np.array((event.xdata, event.ydata))
        span = np.abs(self.ax.get_xlim()[0] - self.ax.get_xlim()[1])
        self.lineMagnitude = span / 20  # draw over 1/20th of the view span
        if 'shift' in self.state:
            if self.initializeRotation:
                self.initializeRotation = False
                self._setRotationPoint(mousePoint)
            delta = mousePoint - self.rotationPivotPoint
            self._setRotation(np.arctan2(delta[1], delta[0]))
        else:
            delta = mousePoint - self.initialClickPoint  # Difference between current mouse position and initial pos
            self.indicatorLine.set_data([[self.initialClickPoint[0], event.xdata], [self.initialClickPoint[1], event.ydata]])
            self._setTranslation(self.initialTranslation + delta)
            self._setRotationPoint(mousePoint)

        self.transformText.set_text(f"Trans: ({self.translation[0]:.1f}, {self.translation[1]:.1f})\nRot: {np.degrees(self.angle):.1f} deg.")
        self._updatePolygons()

    def _on_key_press(self, event: KeyEvent):
        if event.key == 'escape':
            self.set_active(False)
            if self._cancelFunc is not None: self._cancelFunc()  # Cancel
        elif event.key == 'enter':
            newCoordSet = [poly.get_xy() for poly in self.polygonArtists]
            self.onselect(newCoordSet, newCoordSet)
            self.set_active(False)
        elif event.key == 'shift':  # Begin rotation
            self.initializeRotation = True
            self.setArtistVisible(self.angleRefLine, True)
            self.setArtistVisible(self.angleIndicatorLine, True)

    def _on_key_release(self, event: KeyEvent):
        if event.key == 'shift':  # end rotation
            self.setArtistVisible(self.angleRefLine, False)
            self.setArtistVisible(self.angleIndicatorLine, False)

    def _updatePolygons(self):
        self.affineTransform[0, 2] = self.translation[0]
        self.affineTransform[1, 2] = self.translation[1]
        self.affineTransform[0, 0] = self.affineTransform[1, 1] = np.cos(self.angle)
        self.affineTransform[1, 0] = np.sin(self.angle)
        self.affineTransform[0, 1] = -self.affineTransform[1, 0]
        for coords, poly in zip(self.originalCoords, self.polygonArtists):
            poly: Polygon
            coords = np.array(coords) - (self.rotationPivotPoint - self.translation)  # So that any rotation is centered around our initial click position
            coords = np.hstack([coords, np.ones((len(coords), 1))])
            coords = (self.affineTransform @ coords.T).T
            coords = coords[:, :2] + (self.rotationPivotPoint - self.translation)  # Convert back
            poly.set_xy(coords)
        self.updateAxes()

    def _setRotationPoint(self, point: typing.Tuple[float, float]):
        self.rotationPivotPoint = point
        self.angleRefLine.set_data([point[0], point[0] + self.lineMagnitude], [point[1], point[1]])

    def _setRotation(self, radians: float):
        self.angle = radians
        # self.affineTransform[0, 0] = self.affineTransform[1, 1] = np.cos(self.angle)
        # self.affineTransform[1, 0] = np.sin(self.angle)
        # self.affineTransform[0, 1] = -self.affineTransform[1, 0]
        self.angleIndicatorLine.set_data(
            [self.rotationPivotPoint[0], self.rotationPivotPoint[0] + np.cos(self.angle) * self.lineMagnitude],
            [self.rotationPivotPoint[1], self.rotationPivotPoint[1] + np.sin(self.angle) * self.lineMagnitude])

    def _setTranslation(self, translation: typing.Tuple[float, float]):
        self.translation = translation
        # self.affineTransform[0, 2] = translation[0]
        # self.affineTransform[1, 2] = translation[1]


if __name__ == '__main__':
    import matplotlib.pyplot as plt
    fig, ax = plt.subplots()
    fig: Figure
    ax: Axes
    poly = Polygon([[0, 0], [0, 1], [1, 1], [1, 0]])
    poly2 = Polygon([[1, 1], [1, 1.5], [1.5, 1]])
    ax.add_patch(poly)
    ax.add_patch(poly2)
    ax.set_xlim(-1, 2)
    ax.set_ylim(-1, 2)
    mod = MovingModifier(ax, None, None)
    mod.initialize([poly.get_xy(), poly2.get_xy()])
    mod.set_active(True)
    plt.show()
