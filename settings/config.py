from pathlib import Path


# Директории
def get_project_root() -> Path:
    return Path(__file__).parent.parent


ROOT_DIR: str = str(get_project_root())
TEMPLATES_DIR: str = '/templates/'

BACKGROUNDS_DIR: str = ROOT_DIR + TEMPLATES_DIR + 'backgrounds'
PHRASE_DIR: str = ROOT_DIR + TEMPLATES_DIR + 'phrases'
CALENDAR_DIR: str = ROOT_DIR + TEMPLATES_DIR + 'calendars'


# Координаты для календаря и цитат
coord_phrase_center: tuple = (80, 350)
coord_calendar_center: tuple = (1030, 175)

coord_phrase_left: tuple = (1050, 650)
coord_calendar_left: tuple = (1015, 100)

coord_phrase_right: tuple = (115, 655)
coord_calendar_right: tuple = (90, 95)

# Времена года
winter: tuple = (1, 2, 12)
summer: tuple = (6, 7, 8)

