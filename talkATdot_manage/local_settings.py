import os
from pathlib import Path
#settings.pyからそのままコピー
BASE_DIR = Path(__file__).resolve().parent.parent

SECRET_KEY = 'django-insecure-&+fd6gh(m^@t*1*%+0x_0=^qb)_7+s5b$kub&-10)l&$nkc7d7'

#settings.pyからそのままコピー
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}

#ローカルでDebugできるようになる
DEBUG = True