from pathlib import Path


# Директории
def get_project_root() -> Path:
    return Path(__file__).parent.parent


ROOT_DIR = str(get_project_root())
TEMPLATES_DIR = '/templates/'

BACKGROUNDS_DIR = ROOT_DIR + TEMPLATES_DIR + 'backgrounds'
PHRASE_DIR = ROOT_DIR + TEMPLATES_DIR + 'phrases'
CALENDAR_DIR = ROOT_DIR + TEMPLATES_DIR + 'calendars'
