import sys
from PySide6.QtGui import QIcon
from PySide6.QtWidgets import QApplication
from main_window import (MainWindow, Display, Info, setup_theme,
                         WINDOW_ICON_PATH_CALCULATOR)


if __name__ == '__main__':
    # Cria a aplicação
    app = QApplication()
    setup_theme()
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

    # Info
    info = Info('2 + 5')
    window.add_to_vlayout(info)

    # Display
    display = Display()
    display.setPlaceholderText('0')
    window.add_to_vlayout(display)

    # Fixando o tamanha da janela
    window.adjust_fixed_size()

    # Executando tudo
    window.show()
    app.exec()
