import os
from dotenv import load_dotenv
from datetime import timedelta
dbdir = os.path.abspath(os.path.dirname(__file__))
load_dotenv(os.path.join(dbdir, '.env'))
try:
    from pathlib import Path
    path = Path(dbdir)
    dbdir = path.parent
except Exception:
    pass

class Config(object):
    SECRET_KEY = os.environ.get('SECRET_KEY') or b'KEUo\x7fu\x9b1t\x07\xfc\x95)l\xa5\xc1\x19\x1c\xaf\x9d@\xf8_\xbaR\xf2K\xc7'
    
    UPLOAD_FOLDER = os.environ.get('UPLOAD_FOLDER') or '/usr/src/app/files'
    WTF_CSRF_TIME_LIMIT = os.environ.get('WTF_CSRF_TIME_LIMIT') or None #the CSRF token is valid for the life of the session.
    PERMANENT_SESSION_LIFETIME = os.environ.get('PERMANENT_SESSION_LIFETIME') or timedelta(days=5) #the life time for session data

    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or \
        'sqlite:///' + os.path.join(dbdir,'botic.db')
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    PORT = os.environ.get('PORT') or 5000

    MAIL_SERVER = os.environ.get('MAIL_SERVER')
    MAIL_PORT = int(os.environ.get('MAIL_PORT') or 25)
    MAIL_USE_TLS = os.environ.get('MAIL_USE_TLS') is not None
    MAIL_USERNAME = os.environ.get('MAIL_USERNAME')
    MAIL_PASSWORD = os.environ.get('MAIL_PASSWORD')
    ADMINS = ['javier.luna@i-condor.com','isai.galindo@i-condor.com']

    TESTING = os.environ.get('TESTING') or False

    LANGUAGES = ['en', 'es']

    ELASTICSEARCH_URL = os.environ.get('ELASTICSEARCH_URL')
    LOG_TO_STDOUT= os.environ.get('LOG_TO_STDOUT')

    API_URL = os.environ.get('API_URL')
    
    TASK_PER_PAGE = 12
    BOTS_PER_PAGE = 15
    SCHEDULED_TASK_PER_PAGE = 3
    TASK_EXEC_DETAILS_PER_PAGE = 5
    
    REDIS_URL = os.environ.get("REDIS_URL") or 'redis://'
