# Copyright 2018-2021 Nick Anthony, Backman Biophotonics Lab, Northwestern University
#
# This file is part of MPL-Qt-Visualization.
#
# MPL-Qt-Visualization is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# MPL-Qt-Visualization is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with MPL-Qt-Visualization.  If not, see <https://www.gnu.org/licenses/>.

# -*- coding: utf-8 -*-
"""
This file is used to install the MPL-Qt-Visualization package. for example navigate in your terminal to the directory containing this
file and type `pip install .`. This file is also used by the Conda recipe (buildscripts/conda)
"""
from setuptools import setup, find_packages
import os.path as osp
import os


setup(name='MPL-Qt-Visualization',
      version="1",
      description='A Python library providing enhanced data visualization and ROI selection built on top of Matplotlib and PyQt5.',
      author='Nick Anthony',
      author_email='nickmanthony@hotmail.com',
      url='',
      python_requires='>3.7',
      install_requires=['numpy',
                        'scipy',
                        'matplotlib',
                        'shapely',
                        'PyQt5',
                        'scikit-image'],
      package_dir={'': 'src'},
      package_data={'MPL-Qt-Visualization': []},
      packages=find_packages('src')
	)
