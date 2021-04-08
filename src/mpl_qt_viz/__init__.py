"""
A Python package providing enhanced data visualization and ROI selection built on top of Matplotlib and PyQt5.

Subpackages
------------
.. autosummary::
   :toctree: generated/

   roiSelection
   visualizers

"""
import logging
try:
    from . import version
    _versionStr = version.version
except ImportError:  # When running from source the version.py file won't have been created by setuptools_scm
    logging.getLogger(__name__).info("Failed to import `version.py`. Trying to import setuptools_scm")
    try:
        import setuptools_scm
        _versionStr = setuptools_scm.get_version(root='../..', relative_to=__file__)
    except ImportError:  # setuptools_scm
        logging.getLogger(__name__).warn("Failed to import setuptools_scm. Using fallback version string.")
        _versionStr = "x.x.x-dev"

__author__ = 'Nick Anthony'
__version__ = _versionStr

__all__ = ['roiSelection', 'visualizers']