from os import environ, path
from split_settings.tools import include
from dotenv import load_dotenv

# Wczytaj zmienne z pliku .env, jeśli istnieje
BASE_DIR = path.dirname(path.dirname(path.abspath(__file__)))
dotenv_path = path.join(BASE_DIR, '.env')

if path.exists(dotenv_path):
    load_dotenv(dotenv_path)

# Ustawienie domyślnej wartości DJANGO_ENV
environ.setdefault('DJANGO_ENV', 'development')
ENV = environ['DJANGO_ENV']

# Lista plików konfiguracyjnych do załadowania
base_settings = [
    'components/apps.py',
    'components/cache.py',
    'components/common.py',
    'components/custom.py',
    'components/database.py',
    'components/mail.py',
    'components/rest.py',
    'components/security.py',
   # 'environments/{0}.py'.format(ENV),
]

# Include settings:
include(*base_settings)
