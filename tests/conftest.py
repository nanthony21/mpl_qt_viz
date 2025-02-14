import pytest
from PyQt6.QtWidgets import QApplication


@pytest.fixture(scope="session")
def qapplication():
    return QApplication([])
