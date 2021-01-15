# Copyright 2018-2020 Nick Anthony, Backman Biophotonics Lab, Northwestern University
#
# This file is part of PWSpy.
#
# PWSpy is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# PWSpy is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with PWSpy.  If not, see <https://www.gnu.org/licenses/>.

"""
Useful classes for interacting with Matplotlib plots. Mostly for the purpose of drawing ROIs.

Selectors
----------
.. autosummary::
   :toctree: generated/

   EllipseSelector
   LassoSelector
   RegionalPaintSelector
   PointSelector
   FullImPaintSelector
   WaterShedPaintSelector

Utility
--------
.. autosummary::
   :toctree: generated/

   AdjustableSelector
   PolygonInteractor
   AxManager

"""
from ._utilityClasses.adjustableSelector import AdjustableSelector
from ._modifierWidgets.polygonModifier import PolygonModifier
from ._modifierWidgets.movingModifier import MovingModifier
from ._creatorWidgets.ellipse import EllipseCreator
from ._creatorWidgets.lasso import LassoCreator
from ._creatorWidgets.paint import RegionalPaintCreator
from ._creatorWidgets.point import PointCreator
from ._creatorWidgets.FullImPaintSelector import FullImPaintCreator
from ._creatorWidgets.WaterShedPaintSelector import WaterShedPaintCreator
from .coreClasses import AxManager

__all__ = ['AdjustableSelector', 'EllipseCreator', 'LassoCreator', 'RegionalPaintCreator',
           'PointCreator', 'AxManager', 'FullImPaintCreator', 'WaterShedPaintCreator', 'PolygonModifier',
           'MovingModifier']
