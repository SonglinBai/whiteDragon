from typing import Union, List, Optional
from PyQt5.QtWidgets import QFrame, QLabel


class testFrame(QFrame):
    def __init__(self, name):
        super().__init__()
        self.label = QLabel(name, self)
