import os
from google.oauth2 import service_account


BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


SECRET_KEY = 'ydvy5k($y@@7(m-qu-(c5wccyj06=1@d0bi384-5*pngl$2toz'

DEBUG = True

ALLOWED_HOSTS = []

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'storages',
    'style.apps.StyleConfig',
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
 
ROOT_URLCONF = 'fashion.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

WSGI_APPLICATION = 'fashion.wsgi.application'



DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
    }
}


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



LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_L10N = True

USE_TZ = True

# Define the URL prefix for static files
STATIC_URL = '/static/'

# Define the directory where static files will be collected
STATICFILES_DIRS = [os.path.join(BASE_DIR, "static")]

# Define the URL prefix for media files served from the local filesystem
MEDIA_URL_LOCAL = '/images/'

# Import the service_account module from the google.oauth2 package
from google.oauth2 import service_account

# Define the settings for Google Cloud Storage
GOOGLE_APPLICATION_CREDENTIALS = os.path.join(BASE_DIR, 'credentials.json')
GOOGLE_CLOUD_PROJECT_ID = 'burnished-case-381319'
GOOGLE_CLOUD_STORAGE_BUCKET = 'django-bucket-kb'

# Define the default file storage backend to use
DEFAULT_FILE_STORAGE = 'storages.backends.gcloud.GoogleCloudStorage'

# Set the Google Cloud Storage credentials
GS_CREDENTIALS = service_account.Credentials.from_service_account_file(GOOGLE_APPLICATION_CREDENTIALS)
GS_PROJECT_ID = GOOGLE_CLOUD_PROJECT_ID
GS_BUCKET_NAME = GOOGLE_CLOUD_STORAGE_BUCKET

# Define the URL prefix for media files served from Google Cloud Storage
MEDIA_URL = 'https://storage.googleapis.com/{}/images/'.format(GS_BUCKET_NAME)

