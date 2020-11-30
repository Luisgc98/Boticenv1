import logging
from logging.handlers import SMTPHandler, RotatingFileHandler
import os
# Import the microframework to create web apps
from flask import Flask
from api.config import Config
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_babel import Babel
from flask_mail import Mail

app = Flask(__name__)
app.config.from_object(Config)
db = SQLAlchemy(app)
if db.engine.url.drivername == 'sqlite':
    migrate = Migrate(app, db)
    migrate.init_app(app, db, render_as_batch=True)
else:
    migrate = Migrate(app, db)

from api.errors import bp as errors_bp
app.register_blueprint(errors_bp)

#Creación de instancia para internacionalización en/es
babel = Babel(app)
mail = Mail(app)

if not app.debug and not app.testing:
    if app.config['MAIL_SERVER']:
        auth = None
        if app.config['MAIL_USERNAME'] or app.config['MAIL_PASSWORD']:
            auth = (app.config['MAIL_USERNAME'], app.config['MAIL_PASSWORD'])
        secure = None
        if app.config['MAIL_USE_TLS']:
            secure= ()
        mail_handler = SMTPHandler(
            mailhost= (app.config['MAIL_SERVER'],app.config['MAIL_PORT']),
            fromaddr= 'no-reply@' + app.config['MAIL_SERVER'],
            toaddrs=app.config['ADMINS'], subject= 'Botic Failure',
            credentials= auth, secure = secure
        )
        mail_handler.setLevel(logging.ERROR)
        app.logger.addHandler(mail_handler)

    if app.config['LOG_TO_STDOUT']:
        stream_handler = logging.StreamHandler()
        stream_handler.setLevel(logging.INFO)
        app.logger.addHandler(stream_handler)
    else:
        if not os.path.exists('logs'):
            os.mkdir('logs')
        file_handler = RotatingFileHandler('logs/botic.log',
                                        maxBytes=10240, backupCount=10)
        file_handler.setFormatter(logging.Formatter(
            '%(asctime)s %(levelname)s: %(message)s '
            '[in %(pathname)s:%(lineno)d]'))
        file_handler.setLevel(logging.INFO)
        app.logger.addHandler(file_handler)

    app.logger.setLevel(logging.INFO)
    app.logger.info('Botic api startup')

from api import routes
import models