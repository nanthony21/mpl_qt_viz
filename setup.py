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

# -*- coding: utf-8 -*-
"""
This file is used to install the mpl_qt_viz package. for example navigate in your terminal to the directory containing this
file and type `pip install .`. This file is also used by the Conda recipe (buildscripts/conda)
"""
from setuptools import setup, find_packages
import os.path as osp
import os

setup(name='mpl_qt_viz',
      version="1",
      description='A Python library providing enhanced data visualization and ROI selection built on top of Matplotlib and PyQt5.',
      author='Nick Anthony',
      author_email='nickmanthony@hotmail.com',
      url='https://github.com/nanthony21/mpl_qt_viz',
      python_requires='>3.7',
      install_requires=['numpy',
                        'scipy',
                        'matplotlib',
                        'shapely',
                        'PyQt5',
                        'scikit-image',
                        'opencv-python'],
      package_dir={'': 'src'},
      package_data={'mpl_qt_viz': []},
      packages=find_packages('src')
      )
