from flask import url_for, request, current_app
from flask_babel import _

class _botic(object):

    @staticmethod
    def is_current_route(route):
        try:
            return url_for(request.endpoint) == route
        except:
            return False
    
    @staticmethod
    def translate(key):
        WHEN = {
            "MINUTE": _('Minutes'),
            "HOUR": _('Hour'),
            "DAY": _('Day'),
            "WEEK": _('Week'),
            "MONTHLY": _('Montly'),
            "YEARLY": _('Yearly'),
        }
        return WHEN.get(key)
    
    @staticmethod
    def status_desc(status):
        STATUS = {
            models.Status.NOT_PROCESSED: _('Not processed'),
            models.Status.PROCESSED: _('Processed'),
            models.Status.ERRORED: _('Errored'),
            models.Status.PROCESSING: _('Processing')
        }
        return STATUS.get(status, _('Not processed'))

    @staticmethod
    def status_css_class(status):
        CSS_CLASS = {
            models.Status.NOT_PROCESSED: 'b__pending',
            models.Status.PROCESSED: 'b__processed',
            models.Status.ERRORED: 'b__errored',
            models.Status.PROCESSING: 'b__processing'
        }
        return CSS_CLASS.get(status, 'b__unknown')
    
    @staticmethod
    def bot_jobtype_desc(bot_job_type):
        BOT_JOB_TYPE_DESC = {
            models.BotJobType.IMMEDIATE: _('Immediate'),
            models.BotJobType.SCHEDULED: ('Scheduled')
        }
        return BOT_JOB_TYPE_DESC.get(bot_job_type, _('Immediate'))

class Botic(object):
    
    def __init__(self, app=None):
        if app is not None:
            self.init_app(app)

    def init_app(self, app):
        if not hasattr(app, 'extensions'):
            app.extensions = {}
        app.extensions['botic'] = _botic
        app.context_processor(self.context_processor)

    @staticmethod
    def context_processor():
        return {
            'botic': current_app.extensions['botic']
        }

    def create(self):
        return current_app.extensions['botic']

import models