"""
Django settings for srvup project.

For more information on this file, see
https://docs.djangoproject.com/en/1.7/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/1.7/ref/settings/
"""
# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
import os
BASE_DIR = os.path.dirname(os.path.dirname(__file__))
import datetime

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/1.7/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = '6j6^%gd-su1^j7qmp&4g-gm$_nvs2hx(og&ovlj#1)+@09@p87'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

TEMPLATE_DEBUG = True

ALLOWED_HOSTS = []
FULL_DOMAIN_NAME = 'http://www.codingforentrepreneurs.com'

LOGIN_URL = "/login/"

AUTH_USER_MODEL = 'accounts.MyUser'
RECENT_COMMENT_NUMBER = 10
# Application definition

INSTALLED_APPS = (
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    "crispy_forms",
    "rest_framework",
    'accounts',
    "analytics",
    "billing",
    'comments',
    'notifications',
    'videos',
    )

CRISPY_TEMPLATE_PACK = "bootstrap3"

MIDDLEWARE_CLASSES = (
    'django.contrib.sessions.middleware.SessionMiddleware',
    'corsheaders.middleware.CorsMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.auth.middleware.SessionAuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
)
# CORS_URLS_REGEX=r'^/api/.*'
# CORS_URLS_REGEX=r'^/api2/.*'

CORS_ORIGIN_ALLOW_ALL=True
CORS_ORIGIN_WHITELIST = (
        "video-api-climberwb.c9users.io"
    )

TEMPLATE_CONTEXT_PROCESSORS =(
    "django.contrib.auth.context_processors.auth",
    "django.core.context_processors.debug",
    "django.core.context_processors.i18n",
    "django.core.context_processors.media",
    "django.core.context_processors.request",
    "django.core.context_processors.static",
    "django.core.context_processors.tz",
    "django.contrib.messages.context_processors.messages"
)

ROOT_URLCONF = 'srvup.urls'

WSGI_APPLICATION = 'srvup.wsgi.application'


# Database
# https://docs.djangoproject.com/en/1.7/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': os.path.join(BASE_DIR, 'db_git.sqlite3'),
    }
}

# Internationalization
# https://docs.djangoproject.com/en/1.7/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_L10N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/1.7/howto/static-files/

STATIC_URL = '/static/'

STATICFILES_DIRS = (
    os.path.join(os.path.dirname(BASE_DIR), "static", "static_dirs"),
    #'/Users/jmitch/Desktop/srvup/static/static_dirs/', #on mac
    #'\Users\jmitch\Desktop\srvup\static\static_dirs\', somethingl ike this on windows
    #'/var/www/static/',
)

STATIC_ROOT = os.path.join(os.path.dirname(BASE_DIR), "static", "static_root")

TEMPLATE_DIRS = (
    os.path.join(BASE_DIR, "templates"),
)


MEDIA_URL = '/media/'
MEDIA_ROOT = os.path.join(os.path.dirname(BASE_DIR), "static", "media")



#braintree info
BRAINTREE_MERCHANT_ID ="3j27nwdw8mbvk68y"
BRAINTREE_PUBLIC_KEY = "64zrsxstnhykn4v2"
BRAINTREE_PRIVATE_KEY = "5507587264ea632357cad014f69ed78f"




REST_FRAMEWORK = {
    'DEFAULT_PERMISSION_CLASSES': (
        'rest_framework.permissions.IsAuthenticated',
    ),
    'DEFAULT_AUTHENTICATION_CLASSES': (
        'rest_framework.authentication.SessionAuthentication',
        'rest_framework.authentication.BasicAuthentication',
        'rest_framework_jwt.authentication.JSONWebTokenAuthentication',
    ),
     'DEFAULT_PAGINATION_CLASS': 'rest_framework.pagination.PageNumberPagination'
}

JWT_AUTH = {
    
    'JWT_EXPIRATION_DELTA': datetime.timedelta(seconds=30000),
    'JWT_RESPONSE_PAYLOAD_HANDLER':'srvup.utils.jwt_response_payload_handler',
    # 'JWT_REFRESH_EXPIRATION_DELTA': datetime.timedelta(days=5),
}



'''
curl -H "Authorization: JWT eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ1c2VybmFtZSI6ImNsaW1iZXJ3YiIsInVzZXJfaWQiOjE3LCJlbWFpbCI6IndhcnJlbi5rdXNobmVyQGdtYWlsLmNvbSIsImV4cCI6MTQ2MzU4NzE4MH0.Tx_2Al_UL1MVU0KKeAoGzmRdXUiSZDo1wBKB5SpW0lY" http://video-api-climberwb.c9users.io/api/videos/
curl -X POST -d "username=climberwb&password=videoapi" http://video-api-climberwb.c9users.io/api/auth/token/

curl -X POST -d "username=climberwb&password=videoapi" http://video-api-climberwb.c9use(workspace) climberwb:~/workspace/srvup-membership/src (master) $                  text='SomeText'&user=17"  http://video-api-climberwb.c9users.io/api/comments.json -H "Authorization: JWT eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ1c2VybmFtZSI6ImNsaW1iZXJ3YiIsInVzZXJfaWQiOjE3LCJlbWFpbCI6IndhcnJlbi5rdXNobmVyQGdtYWlsLmNvbSIsImV4cCI6MTQ2MzYzMzY1NX0.Ywlgo679XUdQ9IhryU6EFtlZZjAy5P4e0ZIKsL4dzDQ"

'''
