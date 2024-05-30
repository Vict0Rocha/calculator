from main_window import MainWindow
from PySide6.QtGui import QIcon
from PySide6.QtWidgets import (QApplication, QLabel)
import sys
from variables import WINDOW_ICON_PATH_CALCULATOR


if __name__ == '__main__':
    app = QApplication()
    window = MainWindow()

    # Define o ícone
    icon = QIcon(str(WINDOW_ICON_PATH_CALCULATOR))
    window.setWindowIcon(icon)
    app.setWindowIcon(icon)

    '''Verificando se o S.O é windows
    Esse if está configurando o ID do modelo de usuário do aplicativo 
    (AppUserModelID) para um processo no Windows. Esse ID é usado pelo
    Shell do Windows para identificar o processo de recursos como
    agrupamento da barra de tarefas e notificações.
    Em algumas verções do windows, pode ser que o icone não apareça na barra
    de tarefas, esse trecho do codigo ajusta para que o icone apareça. 
    '''
    if sys.platform.startswith('win'):
        import ctypes
        ctypes.windll.shell32.SetCurrentProcessExplicitAppUserModelID(
            u'CompanyName.ProductName.SubProduct.VersionInformation')

    window.show()
    app.exec()
