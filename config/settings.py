import os
from pathlib import Path
BASE_DIR=Path(__file__).resolve().parent.parent
SECRET_KEY=os.environ.get('SECRET_KEY','test-only-do-not-deploy')
DEBUG=False
ALLOWED_HOSTS=os.environ.get('ALLOWED_HOSTS','localhost,127.0.0.1,testserver,web').split(',')
CSRF_TRUSTED_ORIGINS=os.environ.get('CSRF_TRUSTED_ORIGINS','http://localhost:8080,http://127.0.0.1:8080').split(',')
INSTALLED_APPS=['django.contrib.admin','django.contrib.auth','django.contrib.contenttypes','django.contrib.sessions','django.contrib.messages','django.contrib.staticfiles','booking']
MIDDLEWARE=['django.middleware.security.SecurityMiddleware','django.contrib.sessions.middleware.SessionMiddleware','django.middleware.common.CommonMiddleware','django.middleware.csrf.CsrfViewMiddleware','django.contrib.auth.middleware.AuthenticationMiddleware','django.contrib.messages.middleware.MessageMiddleware','django.middleware.clickjacking.XFrameOptionsMiddleware']
ROOT_URLCONF='config.urls'
TEMPLATES=[{'BACKEND':'django.template.backends.django.DjangoTemplates','DIRS':[BASE_DIR/'templates'],'APP_DIRS':True,'OPTIONS':{'context_processors':['django.template.context_processors.request','django.contrib.auth.context_processors.auth','django.contrib.messages.context_processors.messages']}}]
DATABASES={'default':{'ENGINE':'django.db.backends.postgresql','NAME':'hotel','USER':os.environ.get('DB_USER','hotel_owner'),'PASSWORD':os.environ.get('DB_PASSWORD',''),'HOST':os.environ.get('DB_HOST','db'),'PORT':'5432'}}
if os.environ.get('TEST_SQLITE')=='1': DATABASES={'default':{'ENGINE':'django.db.backends.sqlite3','NAME':BASE_DIR/'test.sqlite3'}}
LANGUAGE_CODE='vi'; TIME_ZONE='Asia/Ho_Chi_Minh'; USE_TZ=True
STATIC_URL='/static/'; STATIC_ROOT=BASE_DIR/'staticfiles'
DEFAULT_AUTO_FIELD='django.db.models.BigAutoField'
LOGIN_REDIRECT_URL='/'; LOGOUT_REDIRECT_URL='/'
SECURE_CONTENT_TYPE_NOSNIFF=True
SESSION_COOKIE_HTTPONLY=True; SESSION_COOKIE_SAMESITE='Lax'
AUTH_PASSWORD_VALIDATORS=[{'NAME':'django.contrib.auth.password_validation.MinimumLengthValidator'},{'NAME':'django.contrib.auth.password_validation.CommonPasswordValidator'}]

if os.environ.get('APP_LOG'):
    LOGGING={'version':1,'disable_existing_loggers':False,'handlers':{'file':{'class':'logging.FileHandler','filename':os.environ['APP_LOG']},'console':{'class':'logging.StreamHandler'}},'loggers':{'hotel':{'handlers':['file','console'],'level':'INFO','propagate':False}}}
