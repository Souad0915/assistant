from pathlib import Path
import django_heroku
import pymysql
from pathlib import Path
import os
import dj_database_url
# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/5.1/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = os.environ.get('SECRET_KEY')

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = os.environ.get('DEBUG', 'false').lower()=='true'
ALLOWED_HOSTS = os.environ.get('ALLOWED_HOSTS', '').split()

render_hostname = os.environ.get('RENDER_EXTERNAL_HOSTNAME')
if render_hostname:
    ALLOWED_HOSTS.append(render_hostname)


# Ajout manuel pour résoudre l'erreur
ALLOWED_HOSTS.append('assistant-9-ed4n.onrender.com')

# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'monprojetgl.apps.MonprojetConfig',  # Pas juste 'monprojetgl'
    
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'monprojet.urls'


TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [os.path.join(BASE_DIR, 'templates')],  # Assurez-vous que le dossier est correct
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
                'django.template.context_processors.media',
                'monprojetgl.context_processors.notification_context',
            ],
        },
    },
]


WSGI_APPLICATION = 'monprojet.wsgi.application'


# Database
# https://docs.djangoproject.com/en/5.1/ref/settings/#databases

DATABASES = {
    'default': dj_database_url.config(default=os.environ.get('DATABASE_URL'))
}
# Password validation
# https://docs.djangoproject.com/en/5.1/ref/settings/#auth-password-validators

AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
]


# Internationalization
# https://docs.djangoproject.com/en/5.1/topics/i18n/

LANGUAGE_CODE = 'fr'  # Passé à français

TIME_ZONE = 'UTC'

USE_I18N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/5.1/howto/static-files/
STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles')

STATIC_URL = 'static/'

# Emplacement des fichiers statiques à collecter dans le projet
STATICFILES_DIRS = [
    BASE_DIR / 'static',  # Répertoire statique à la racine du projet
]

# Emplacement des fichiers statiques collectés pour la production
STATIC_ROOT = BASE_DIR / 'staticfiles'

STATICFILES_FINDERS = [
    'django.contrib.staticfiles.finders.FileSystemFinder',
    'django.contrib.staticfiles.finders.AppDirectoriesFinder',
]


# Auth Settings
LOGIN_REDIRECT_URL = 'index'  # Redirige vers la page d'accueil après la connexion (nom d'URL)
LOGIN_URL = '/'  # Redirige vers la page de connexion si l'utilisateur n'est pas authentifié

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'


AUTHENTICATION_BACKENDS = [
    'django.contrib.auth.backends.ModelBackend',
]

AUTH_USER_MODEL = 'monprojetgl.Enseignant'  # Doit utiliser le label exact

# Ajoutez ces lignes à la fin de votre settings.py
MEDIA_URL = '/media/'
MEDIA_ROOT = os.path.join(BASE_DIR, 'media')


# Taille maximale des uploads (2MB)
DATA_UPLOAD_MAX_MEMORY_SIZE = 2097152  # 2MB
FILE_UPLOAD_MAX_MEMORY_SIZE = 2097152  # 2MB

# Emplacement par défaut pour les photos de profil
DEFAULT_PROFILE_PICTURE = 'profile_pics/default.jpg'

CSRF_COOKIE_HTTPONLY = True
CSRF_COOKIE_SECURE = False  # Assurez-vous que cela est configuré correctement en fonction de votre environnement (True pour HTTPS).
CSRF_COOKIE_NAME = 'csrftoken'

