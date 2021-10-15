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

"""
Useful classes for interacting with Matplotlib plots. Mostly for the purpose of drawing ROIs.

ROI Creators
----------
.. autosummary::
   :toctree: generated/

   EllipseCreator
   LassoCreator
   RegionalPaintCreator
   SquareCreator
   FullImPaintCreator
   WaterShedPaintCreator

Utility
--------
.. autosummary::
   :toctree: generated/

   AdjustableSelector
   PolygonModifier

"""
from ._utilityClasses.adjustableSelector import AdjustableSelector
from ._modifierWidgets.polygonModifier import PolygonModifier
from ._modifierWidgets.movingModifier import MovingModifier
from ._creatorWidgets.ellipse import EllipseCreator
from ._creatorWidgets.lasso import LassoCreator
from ._creatorWidgets.paint import RegionalPaintCreator
from ._creatorWidgets.square import SquareCreator
from ._creatorWidgets.point import PointCreator
from ._creatorWidgets.FullImPaintSelector import FullImPaintCreator
from ._creatorWidgets.WaterShedPaintSelector import WaterShedPaintCreator
from ._creatorWidgets._base import CreatorWidgetBase
from ._coreClasses import InteractiveWidgetBase
from ._modifierWidgets._base import ModifierWidgetBase

__all__ = ['AdjustableSelector', 'EllipseCreator', 'LassoCreator', 'RegionalPaintCreator',
           'SquareCreator', 'FullImPaintCreator', 'WaterShedPaintCreator', 'PolygonModifier',
           'MovingModifier', 'PointCreator', 'CreatorWidgetBase', 'InteractiveWidgetBase', 'ModifierWidgetBase']
