'''
Django Settings File
'''
import os
import localcreds

<<<<<<< HEAD

=======
>>>>>>> f6036cac74dbf01fa553dbfbab4de4ce89e2533e
# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
PROJECT_ROOT = os.path.dirname(os.path.abspath(__file__))

<<<<<<< HEAD
=======
#DEPLOYMENT MODE : toggle LOCAL or REMOTE
DEPLOY = 'REMOTE'

>>>>>>> f6036cac74dbf01fa553dbfbab4de4ce89e2533e
#Secret keys for heroku and firebase (deploy must be LOCAL or REMOTE)
def SECRET_KEYS(deploy):
    if (deploy == 'LOCAL'):
        return (localcreds.get_credentials(), localcreds.get_credentials(firebase=True))
    elif (deploy == 'REMOTE'):
        return (os.environ.get('SECRET_KEY'), os.environ.get('FIREBASE_KEY'))
    else:
        print ('BAD DEPLOMENT CONDITION!')
        assert(False)

<<<<<<< HEAD
#Toggle 'LOCAL' if you're developing locally via $ heroku local
#Be sure to run localcreds.py in the project directory before
#developing locally! (instructions in localcreds.py source code) 
(SECRET_KEY, FIREBASE_KEY) = SECRET_KEYS('LOCAL')

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True
=======
(SECRET_KEY, FIREBASE_KEY) = SECRET_KEYS(DEPLOY)

# SECURITY WARNING: don't run with debug turned on in production!
if (DEPLOY == 'LOCAL'):
    DEBUG = True
else:
    DEBUG = False
>>>>>>> f6036cac74dbf01fa553dbfbab4de4ce89e2533e

# Application definition
INSTALLED_APPS = (
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'assigncal',
<<<<<<< HEAD
     'cas'
=======
>>>>>>> f6036cac74dbf01fa553dbfbab4de4ce89e2533e
)

MIDDLEWARE_CLASSES = (
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.auth.middleware.SessionAuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'django.middleware.security.SecurityMiddleware',
<<<<<<< HEAD
    'cas.middleware.CASMiddleware',
    'django.contrib.auth.middleware.RemoteUserMiddleware',
=======
>>>>>>> f6036cac74dbf01fa553dbfbab4de4ce89e2533e
)

ROOT_URLCONF = 'project.urls'

TEMPLATES = (
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': ['project/templates'],
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
)

WSGI_APPLICATION = 'project.wsgi.application'


# Database
# https://docs.djangoproject.com/en/1.9/ref/settings/#databases
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
    }
}

AUTH_PASSWORD_VALIDATORS = (
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
)

<<<<<<< HEAD
#CAS_SERVER_URL
CAS_SERVER_URL = "https://fed.princeton.edu/cas/login"
CAS_LOGOUT_COMPLETELY = True
CAS_PROVIDE_URL_TO_LOGOUT = True
#CAS_RETRY_LOGIN = True

#where our site is on the web
SITE_URLS = { 
'DEV': 'assign-cals-cos333.herokuapp.com', 
'LIVE': 'NEED A LEGIT NAME' 
} 

#where our firebase is on the web
FIREBASE_URLS = { 
'DEV': 'https://assign-cals-cos333.firebaseio.com/', 
'LIVE': 'NEED A LEGIT NAME' 
} 

SITE_URL = SITE_URLS['DEV'] 
FIREBASE_URL = FIREBASE_URLS['DEV']
=======
#where our site is on the web
SITE_URLS = { 
'LOCAL': 'http://localhost:8000/',
'REMOTE': 'http://assign-cals-cos333.herokuapp.com/', 
'LIVE': 'NEED A LEGIT NAME' 
} 

SITE_URL = SITE_URLS[DEPLOY] 

#where our firebase is on the web
FIREBASE_URLS = { 
'LOCAL' : 'https://assign-cals-cos333.firebaseio.com/',
'REMOTE': 'https://assign-cals-cos333.firebaseio.com/', 
'LIVE': 'NEED A LEGIT NAME' 
} 

FIREBASE_URL = FIREBASE_URLS[DEPLOY]
>>>>>>> f6036cac74dbf01fa553dbfbab4de4ce89e2533e

# Internationalization
# https://docs.djangoproject.com/en/1.9/topics/i18n/

LANGUAGE_CODE = 'en-us'
TIME_ZONE = 'UTC'
USE_I18N = True
USE_L10N = True
USE_TZ = True

# Honor the 'X-Forwarded-Proto' header for request.is_secure()
SECURE_PROXY_SSL_HEADER = ('HTTP_X_FORWARDED_PROTO', 'https')

# Allow all host headers
ALLOWED_HOSTS = ['*']

# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/1.9/howto/static-files/

STATIC_ROOT = os.path.join(PROJECT_ROOT, 'staticfiles')
STATIC_URL = '/static/'

# Extra places for collectstatic to find static files.
STATICFILES_DIRS = [
    os.path.join(PROJECT_ROOT, 'static'),
]

# Simplified static file serving.
# https://warehouse.python.org/project/whitenoise/
STATICFILES_STORAGE = 'whitenoise.django.GzipManifestStaticFilesStorage'
