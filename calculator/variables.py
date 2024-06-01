from pathlib import Path

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
