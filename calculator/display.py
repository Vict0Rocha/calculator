from variables import BIG_FONT_SIZE, TEXT_MARGIN, MINIMUM_WITH
from PySide6.QtWidgets import QLineEdit
from PySide6.QtCore import Qt


class Display(QLineEdit):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.config_style()

    def config_style(self):
        # Fonte do display
        self.setStyleSheet(f'font-size: {BIG_FONT_SIZE}px;')
        # Tamanho do display
        self.setMinimumHeight(BIG_FONT_SIZE * 2)
        # Largura
        self.setMinimumWidth(MINIMUM_WITH)
        # Alinhando o texto a direita
        self.setAlignment(Qt.AlignmentFlag.AlignRight)
        # Margem
        margin = [TEXT_MARGIN for _ in range(4)]
        self.setTextMargins(*margin)
