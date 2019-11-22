import os
BASE_DIR = os.path.dirname(os.path.dirname(__file__))

def get_secret(secret_name):
    try:
        with open('/run/secrets/{0}'.format(secret_name), 'r') as secret_file:
            return secret_file.read()
    except IOError:
        return None

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = '@9e1s9zexj93d%n^^2)vxi0p4lwmz2tn0y67%*65#$nn5g64q1'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True


ALLOWED_HOSTS = ['glossarios.libras.ufsc.br', 'glossario.libras.ufsc.br', 'localhost', '200.135.84.253']

INSTALLED_APPS = (
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'glossario',

)

MIDDLEWARE_CLASSES = (
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.auth.middleware.SessionAuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
)

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'glossariolibras.urls'

WSGI_APPLICATION = 'glossariolibras.wsgi.application'

MEDIA_ROOT = os.path.join(BASE_DIR, 'media')
MEDIA_URL = '/media/'

if get_secret('glossario_name_db'):

    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.mysql',
            'NAME': get_secret('glossario_name_db'),
            'USER': get_secret('glossario_user_db'),
            'PASSWORD': get_secret('glossario_password_db'),
            'HOST': 'mysql.sites.ufsc.br',
            'PORT': '3306',
            'OPTIONS': {'charset': 'latin1',}, # o banco tá em utf8, mas se não colocar latin1 aqui da erro...
        }
    }
# else:
#     DATABASES = {
#         'default': {
#             'ENGINE': 'django.db.backends.mysql',
#             'NAME': 'glossario',
#             'USER': 'root',
#             'PASSWORD': 'glossario',
#             'HOST': 'db_gll',
#             'PORT': '3306',
#             'OPTIONS': {'charset': 'utf8'},
#         }
# }

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
    }
}


LANGUAGE_CODE = 'pt-br'

TIME_ZONE = 'America/Sao_Paulo'

USE_I18N = True

USE_L10N = True

USE_TZ = True

STATIC_URL = '/static/'
PROJECT_ROOT = os.path.dirname(os.path.dirname(__file__))
STATIC_ROOT = os.path.join(PROJECT_ROOT, 'glossario/static')

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [os.path.join(BASE_DIR, 'templates')],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
            'debug': DEBUG,
        },
    },
]

SESSION_EXPIRE_AT_BROWSER_CLOSE = True

AUTH_USER_MODEL = 'glossario.UserGlossario'

LOGIN_REDIRECT_URL = 'index'

LOGIN_URL = 'login'

EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'

EMAIL_HOST = "smtp.sistemas.ufsc.br"
EMAIL_PORT = 587
EMAIL_HOST_USER = get_secret('email_libras_user')
EMAIL_HOST_PASSWORD = get_secret('email_libras_password')
EMAIL_USE_SSL = True