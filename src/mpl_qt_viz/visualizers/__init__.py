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
Qt Widgets for interactive data visualization.

Classes
----------
.. autosummary::
   :toctree: generated/

   MultiPlot
   PlotNd
   PlotNdCanvas
   DockablePlotWindow

"""

from ._multiPlot import MultiPlot
from ._PlotNd import PlotNd, PlotNdCanvas
from ._dockPlot import DockablePlotWindow

__all__ = ['MultiPlot', 'PlotNd', 'PlotNdCanvas', 'DockablePlotWindow']