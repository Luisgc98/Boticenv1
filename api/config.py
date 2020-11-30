import os
from datetime import timedelta
dbdir = os.path.abspath(os.path.dirname(__file__))
try:
    from pathlib import Path
    path = Path(dbdir)
    dbdir = path.parent
except Exception:
    pass

class Config(object):
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or \
        'sqlite:///' + os.path.join(dbdir,'botic.db')
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    PORT = os.environ.get('PORT') or 5000

    API_PREFIX = os.environ.get("API_PREFIX") or '/api'

    MAIL_SERVER = os.environ.get('MAIL_SERVER')
    MAIL_PORT = int(os.environ.get('MAIL_PORT') or 25)
    MAIL_USE_TLS = os.environ.get('MAIL_USE_TLS') is not None
    MAIL_USERNAME = os.environ.get('MAIL_USERNAME')
    MAIL_PASSWORD = os.environ.get('MAIL_PASSWORD')
    ADMINS = ['javier.luna@i-condor.com','isai.galindo@i-condor.com']
    
    BABEL_TRANSLATION_DIRECTORIES="i18n/translations"
    BABEL_DEFAULT_LOCATE='en'

    LOG_TO_STDOUT= os.environ.get('LOG_TO_STDOUT')

    PORTAL_URL = os.environ.get('PORTAL_URL') or 'http://localhost:5000'
