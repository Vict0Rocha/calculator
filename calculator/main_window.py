from PySide6.QtCore import Qt
import qdarktheme
from variables import (BIG_FONT_SIZE, TEXT_MARGIN, MINIMUM_WITH,
                       SMALL_FONT_SIZE)
from PySide6.QtWidgets import (QMainWindow, QWidget, QVBoxLayout, QLineEdit,
                               QLabel)

# Parent é uma janela pai, que vem antes dela.
# Nosso projetos não tera, mas colocamos somente para manter um padrão.


class MainWindow(QMainWindow):
    def __init__(self, parent: QWidget | None = None, *args, **kwargs) -> None:
        super().__init__(parent, *args, **kwargs)

        # Configurando o layout básico
        self.cw = QWidget()
        self.v_layout = QVBoxLayout()
        self.cw.setLayout(self.v_layout)
        self.setCentralWidget(self.cw)

        # Titulo da janela
        self.setWindowTitle('Calculator')

    # Para fixar o tamanho da minha janela de forma que ela abrir.
    def adjust_fixed_size(self):
        # últimas coisas a serem feitas
        self.adjustSize()  # Ajustando o tamanho dos elementos na minha janela.
        # Fixando o tamanho da janela, pelo tamanho que ela abrir.
        self.setFixedSize(self.width(), self.height())

    def add_to_vlayout(self, widget: QWidget):
        self.v_layout.addWidget(widget)


class Display(QLineEdit):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.config_style()

    def config_style(self):
        # Fonte do display
        self.setStyleSheet(f'font-size: {BIG_FONT_SIZE}px;')
        # Tamanho do display em altura
        self.setMinimumHeight(BIG_FONT_SIZE * 2)
        # Largura em comprimento
        self.setMinimumWidth(MINIMUM_WITH)
        # Alinhando o texto a direita
        self.setAlignment(Qt.AlignmentFlag.AlignRight)
        # Margem
        margin = [TEXT_MARGIN for _ in range(4)]
        self.setTextMargins(*margin)

# O label que fica em cima do display - é tipo um cache ou flashcards


class Info(QLabel):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.config_style()

    def config_style(self):
        self.setStyleSheet(f'font-size: {SMALL_FONT_SIZE}px;')
        self.setAlignment(Qt.AlignmentFlag.AlignRight)


def setup_theme():
    qdarktheme.setup_theme()
