import qdarktheme
import math
from pathlib import Path
from PySide6.QtCore import Qt, Slot
from utils import is_empty, is_num_or_dot, is_valid_number
from PySide6.QtWidgets import (QMainWindow, QWidget, QVBoxLayout, QGridLayout,
                               QLineEdit, QLabel, QPushButton)
# from typing import TYPE_CHECKING

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
PRIMARY_COLOR = '#215fa2'
DARKER_PRIMARY_COLOR = '#4076bb'
DARKEST_PRIMARY_COLOR = '#5e8cd3'

# Sizing
BIG_FONT_SIZE = 37
MEDIUM_FONT_SIZE = 24
SMALL_FONT_SIZE = 15
TEXT_MARGIN = 10
MINIMUM_WITH = 280


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

    def add_widget_to_vlayout(self, widget: QWidget):
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


class Button(QPushButton):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.config_style()

    def config_style(self):
        font = self.font()
        font.setPixelSize(MEDIUM_FONT_SIZE)
        self.setFont(font)
        self.setMinimumSize(60, 65)
        # self.setProperty('cssClass', 'specialButton')


'''Grid de botões 
Tenho uma matriz, para cada elemento dessa matriz,
é criado e adicionada um novo botão na minha grid.
'''


class ButtonsGrid(QGridLayout):
    def __init__(self, display: Display, info: Info, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)

        self._grid_mask = [
            ['C', 'CE', '^', '/'],
            ['7', '8', '9', '*'],
            ['4', '5', '6', '-'],
            ['1', '2', '3', '+'],
            ['',  '0', '.', '='],
        ]
        self.display = display
        self.info = info
        self._equation = ''
        self.equation_initial_value = ''
        self._left = None
        self._right = None
        self._op = None
        self.equation = self.equation_initial_value
        self._make_grid()

    @property
    def equation(self):
        return self._equation

    @equation.setter
    def equation(self, value):
        self._equation = value
        self.info.setText(value)

    def _make_grid(self):
        for i, row_data in enumerate(self._grid_mask):
            for j, button_text in enumerate(row_data):
                button = Button(button_text)
                # Espandindo o meu botão de número 0
                # if button_text == '0':
                #     self.addWidget(button, i, j, 0, 2)
                self.addWidget(button, i, j)

                # if button_text == '':
                #     button.deleteLater()

                # Verificando os botões para estilizar
                if not is_num_or_dot(button_text) and not is_empty(button_text):
                    button.setProperty('cssClass', 'specialButton')

                slot = self._make_slot(
                    self._insert_button_text_to_display, button)
                self._connect_button_clicked(button, slot)
                self._config_sprecial_button(button)

    def _connect_button_clicked(self, button, slot):
        button.clicked.connect(slot)

    def _config_sprecial_button(self, button):
        text = button.text()

        if text == 'C':
            self._connect_button_clicked(button, self._clear)

        if text == 'CE':
            self._connect_button_clicked(button, self.display.backspace)

        if text in '+-/*^':
            self._connect_button_clicked(
                button,
                self._make_slot(self._operator_clicked, button)
            )

        if text in '=':
            self._connect_button_clicked(button, self._eq)

    def _make_slot(self, func, *args, **kwargs):
        @Slot(bool)
        def real_slot():
            func(*args, **kwargs)
        return real_slot

    def _insert_button_text_to_display(self, button):
        button_text = button.text()
        new_display_value = self.display.text() + button_text

        if not is_valid_number(new_display_value):
            return

        self.display.insert(button_text)

    def _clear(self):
        self._left = None
        self._right = None
        self._op = None
        self.equation = self.equation_initial_value
        self.display.clear()

    def _operator_clicked(self, button):
        button_text = button.text()  # Operador +-*/ (etc...)
        display_text = self.display.text()  # Deverá ser meu número _left
        self.display.clear()  # Limpa o display

        # Se o usuario clicar no operador sem configurar qualquer número
        if not is_valid_number(display_text) and self._left is None:
            print('Nada para colocar a esquerda')
            return

        # Se houver algo no número da esquerda, apenas atribuimos o valor
        # E aguardamos o número da direita.
        if self._left is None:
            self._left = float(display_text)

        self._op = button_text
        self.equation = f'{self._left} {self._op}'
        # print(button_text)

    def _eq(self):
        display_text = self.display.text()

        if not is_valid_number(display_text):
            print('Nada para a direita')
            return

        self._right = float(display_text)
        self.equation = f'{self._left} {self._op} {self._right}'
        result = 'erro'

        try:
            if '^' in self.equation and isinstance(self._left, float):
                result = math.pow(self._left, self._right)
            else:
                result = eval(self.equation)
        except ZeroDivisionError:
            print('Zero Division Error')
        except OverflowError:
            print('Número muito grande')

        self.display.clear()
        self.info.setText(f'{self.equation} = {result}')
        self._left = result
        self._right = None

        if result == 'erro':
            self._left = None


# QSS - Estilo do QT for python
# https://pypi.org/project/qt-material
# Dark Theme
# https://pypi.org/project/pyqtdarktheme
# Outra alternativa
# https://doc.qt.io/qtforpython-6/tutorials/basictutorial/widgetstyling.html
qss = f"""
    QPushButton[cssClass="specialButton"] {{
        color: #fff;
        background: {PRIMARY_COLOR};
    }}
    QPushButton[cssClass="specialButton"]:hover {{
        color: #fff;
        background: {DARKER_PRIMARY_COLOR};
    }}
    QPushButton[cssClass="specialButton"]:pressed {{
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
                "primary": "#d2ffff",
            },
            "[light]": {
                "primary": f"{PRIMARY_COLOR}",
            },
        },
        additional_qss=qss
    )
