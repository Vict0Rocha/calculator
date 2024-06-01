import qdarktheme
from variables import PRIMARY_COLOR, DARKEST_PRIMARY_COLOR, DARKER_PRIMARY_COLOR

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
