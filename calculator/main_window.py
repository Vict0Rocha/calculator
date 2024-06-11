import math
from PySide6.QtGui import QKeyEvent
import qdarktheme
from pathlib import Path
from PySide6.QtGui import QKeyEvent
from PySide6.QtCore import Qt, Slot, Signal
from utils import is_empty, is_num_or_dot, is_valid_number
from PySide6.QtWidgets import (QMainWindow, QWidget, QVBoxLayout, QGridLayout,
                               QLineEdit, QLabel, QPushButton, QMessageBox)
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

    def make_msg_box(self):
        return QMessageBox(self)


class Display(QLineEdit):
    eq_pressed = Signal()
    del_pressed = Signal()
    clear_pressed = Signal()

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

    def keyPressEvent(self, event: QKeyEvent) -> None:
        # Pegando o texto da tecla digitada sem espaços
        text = event.text().strip()
        key = event.key()  # Pegando minha tecla
        KEYS = Qt.Key  # Valores para as teclas
        is_enter = key in [KEYS.Key_Enter, KEYS.Key_Return]
        is_delete = key in [KEYS.Key_Backspace, KEYS.Key_Delete]
        is_esc = key in [KEYS.Key_Escape]

        if is_enter or text == '=':
            print('ENTER - SINAL DE', type(self).__name__)
            self.eq_pressed.emit()  # Mandando a solicitadação para minha grid
            return event.ignore()

        if is_delete or text.lower() == 'd':
            print('DELETE - SINAL DE', type(self).__name__)
            self.del_pressed.emit()
            return event.ignore()

        if is_esc or text.lower() == 'c':
            print('ESC - SINAL DE', type(self).__name__)
            self.clear_pressed.emit()
            return event.ignore()

        # Não passar daqui, se não tiver texto
        if is_empty(text):
            return event.ignore()

        print('teste', text)
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
    def __init__(self, display: Display, info: Info, window: MainWindow, * args, **kwargs) -> None:
        super().__init__(*args, **kwargs)

        self._grid_mask = [
            ['CE', 'C', '^', '/'],
            ['7', '8', '9', '*'],
            ['4', '5', '6', '-'],
            ['1', '2', '3', '+'],
            ['',  '0', '.', '='],
        ]
        self.display = display
        self.info = info
        self.window = window
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
        self.display.eq_pressed.connect(lambda: print(123))
        self.display.del_pressed.connect(self.display.backspace)
        self.display.clear_pressed.connect(lambda: print(123))

        for i, row_data in enumerate(self._grid_mask):
            for j, button_text in enumerate(row_data):
                button = Button(button_text)
                self.addWidget(button, i, j)

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
            self._show_error('Formato inválido, você não digitou nada.')
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
            self._show_error(
                'Formato inválido, digite o operador da direitra.'
            )
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
            self._show_error('Não é possivél dividir por 0.')
        except OverflowError:
            self._show_error(
                'Estourou, não é possivel realizar essa conta.'
            )

        self.display.clear()
        self.info.setText(f'{self.equation} = {result}')
        self._left = result
        self._right = None

        if result == 'erro':
            self._left = None

    def _make_dialog(self, text):
        msg_box = self.window.make_msg_box()
        msg_box.setText(text)
        return msg_box

    def _show_error(self, text):
        msgBox = self._make_dialog(text)
        msgBox.setIcon(msgBox.Icon.NoIcon)
        msgBox.exec()

    def _show_info(self, text):
        msgBox = self._make_dialog(text)
        msgBox.setIcon(msgBox.Icon.Information)
        msgBox.exec()


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
