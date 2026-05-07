from pathlib import Path
import environ
BASE_DIR=Path(__file__).resolve().parent.parent
env=environ.Env(DEBUG=(bool, True))
if (BASE_DIR/'.env').exists():
    environ.Env.read_env(BASE_DIR/'.env')
SECRET_KEY=env('SECRET_KEY', default='dev-secret-change-me')
DEBUG=env('DEBUG', default=True)
ALLOWED_HOSTS=[x.strip() for x in env('ALLOWED_HOSTS', default='127.0.0.1,localhost').split(',') if x.strip()]
INSTALLED_APPS=[
 'django.contrib.admin','django.contrib.auth','django.contrib.contenttypes','django.contrib.sessions',
 'django.contrib.messages','django.contrib.staticfiles','storages','takip'
]
MIDDLEWARE=[
 'django.middleware.security.SecurityMiddleware','whitenoise.middleware.WhiteNoiseMiddleware',
 'django.contrib.sessions.middleware.SessionMiddleware','django.middleware.common.CommonMiddleware',
 'django.middleware.csrf.CsrfViewMiddleware','django.contrib.auth.middleware.AuthenticationMiddleware',
 'takip.middleware.ActivityLogMiddleware','django.contrib.messages.middleware.MessageMiddleware',
 'django.middleware.clickjacking.XFrameOptionsMiddleware'
]
ROOT_URLCONF='musteri_web.urls'
TEMPLATES=[{'BACKEND':'django.template.backends.django.DjangoTemplates','DIRS':[BASE_DIR/'templates'],'APP_DIRS':True,
'OPTIONS':{'context_processors':['django.template.context_processors.debug','django.template.context_processors.request','django.contrib.auth.context_processors.auth','django.contrib.messages.context_processors.messages']}}]
WSGI_APPLICATION='musteri_web.wsgi.application'
DATABASE_URL=env('DATABASE_URL', default='')
if DATABASE_URL:
    DATABASES={'default': env.db('DATABASE_URL')}
else:
    DATABASES={'default': {'ENGINE':'django.db.backends.sqlite3','NAME': BASE_DIR/'db.sqlite3'}}
AUTH_PASSWORD_VALIDATORS=[
 {'NAME':'django.contrib.auth.password_validation.UserAttributeSimilarityValidator'},
 {'NAME':'django.contrib.auth.password_validation.MinimumLengthValidator'},
 {'NAME':'django.contrib.auth.password_validation.CommonPasswordValidator'},
 {'NAME':'django.contrib.auth.password_validation.NumericPasswordValidator'},
]
LANGUAGE_CODE='tr-tr'
TIME_ZONE='Europe/Istanbul'
USE_I18N=True
USE_TZ=True
STATIC_URL='static/'
STATIC_ROOT=BASE_DIR/'staticfiles'
MEDIA_URL='media/'
MEDIA_ROOT=BASE_DIR/'media'
DEFAULT_AUTO_FIELD='django.db.models.BigAutoField'
FILE_STORAGE_MODE=env('FILE_STORAGE_MODE', default='local')
if FILE_STORAGE_MODE=='s3':
    DEFAULT_FILE_STORAGE='storages.backends.s3boto3.S3Boto3Storage'
    AWS_ACCESS_KEY_ID=env('AWS_ACCESS_KEY_ID')
    AWS_SECRET_ACCESS_KEY=env('AWS_SECRET_ACCESS_KEY')
    AWS_STORAGE_BUCKET_NAME=env('AWS_STORAGE_BUCKET_NAME')
    AWS_S3_ENDPOINT_URL=env('AWS_S3_ENDPOINT_URL', default=None)
    AWS_S3_REGION_NAME=env('AWS_S3_REGION_NAME', default='eu-central-1')
    AWS_DEFAULT_ACL=None
    AWS_QUERYSTRING_AUTH=True
    AWS_S3_FILE_OVERWRITE=False
LOGIN_URL='/admin/login/'
