import qdarktheme
from pathlib import Path
from PySide6.QtCore import Qt
from PySide6.QtWidgets import (QMainWindow, QWidget, QVBoxLayout, QLineEdit,
                               QLabel)

# VARIAVEIS CONSTANTES

# Pegando o caminho absoluto do diretório do meu projeto
ROOT_DIR = Path(__file__).parent
# Caminho da pasta do meus icones
FILE_DIR = ROOT_DIR / 'icons'
# Caminho do arquvio em si
WINDOW_ICON_PATH_OM = FILE_DIR / 'icon.png'
WINDOW_ICON_PATH_CALCULATOR = FILE_DIR / 'calculator_icon.png'
WINDOW_ICON_PATH_GOOGLE = FILE_DIR / 'calculate_icon_google.png'

# Colors
PRIMARY_COLOR = '#1e81b0'
DARKER_PRIMARY_COLOR = '#16658a'
DARKEST_PRIMARY_COLOR = '#115270'

# Sizing
BIG_FONT_SIZE = 37
MEDIUM_FONT_SIZE = 24
SMALL_FONT_SIZE = 14
TEXT_MARGIN = 15
MINIMUM_WITH = 300


# Parent é uma janela pai, que vem antes dela.
# Nosso projetos não tera, mas colocamos somente para manter um padrão.

# Janela principal
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

# O label(Infor) que fica em cima do display - é tipo um cache ou flashcards


class Info(QLabel):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.config_style()

    def config_style(self):
        self.setStyleSheet(f'font-size: {SMALL_FONT_SIZE}px;')
        self.setAlignment(Qt.AlignmentFlag.AlignRight)


# QSS - Estilo do QT for python
# https://pypi.org/project/qt-material
# Dark Theme
# https://pypi.org/project/pyqtdarktheme
# Outra alternativa
# https://doc.qt.io/qtforpython-6/tutorials/basictutorial/widgetstyling.html

qss = f"""
    PushButton[cssClass="specialButton"] {{
        color: #fff;
        background: {PRIMARY_COLOR};
    }}
    PushButton[cssClass="specialButton"]:hover {{
        color: #fff;
        background: {DARKER_PRIMARY_COLOR};
    }}
    PushButton[cssClass="specialButton"]:pressed {{
        color: #fff;
        background: {DARKEST_PRIMARY_COLOR};
    }}
"""

# Tema da calculadora


def setup_theme():
    qdarktheme.setup_theme(
        theme='dark',
        corner_shape='rounded',
        custom_colors={
            "[dark]": {
                "primary": f"{PRIMARY_COLOR}",
            },
            "[light]": {
                "primary": f"{PRIMARY_COLOR}",
            },
        },
        additional_qss=qss
    )
