from PySide6.QtWidgets import (QMainWindow, QWidget,
                               QVBoxLayout)

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
