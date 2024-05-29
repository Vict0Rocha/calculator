from main_window import MainWindow
from PySide6.QtWidgets import (QApplication, QWidget,
                               QVBoxLayout, QLabel)


if __name__ == '__main__':
    app = QApplication()
    window = MainWindow()

    label = QLabel('Meu texto')
    label.setStyleSheet('font-size: 80px')
    window.v_layout.addWidget(label)
    window.adjust_fixed_size()

    window.show()
    app.exec()
