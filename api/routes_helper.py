import sys
from flask_restful import request, Resource, reqparse
from flask import make_response, request, current_app
from flask_babel import gettext
from datetime import datetime, timedelta
import json
from collections import namedtuple
from api import db
from exceptions import InvalidLoginError, BotNotConfiguredError, ParameterNotFoundError
from models import User, Bot, BotHeartbeat, Parameter, BotJob, TaskVersion, BotJobFailureEvidence, BotJobEvidence, Task
from exceptions import InvalidLoginError, BotNotConfiguredError
from util import get_secret_random, json_2_object

class Setup(Resource):
    def post(self):
        parser = reqparse.RequestParser()

        parser.add_argument('name',required=True)
        args = parser.parse_args()
        name = args['name']
        user_secret = getUserSecretHeaderInfo()
        current_app.logger.info("Configuring machine %s as bot" % name)
        try:
            user = db.session.query(User).filter(User.user_secret==user_secret).first()
            if user:
                bot_secret = get_secret_random()
                bot = Bot(name=name, user=user, bot_secret= bot_secret)
                db.session.add(bot)
                db.session.commit()
                return {"bot_secret": bot_secret}, 200
            else:
                return { "message": gettext("Invalid login") }, 404
        except:
            current_app.logger.error("Error setting up a bot", exc_info=sys.exc_info())
            db.session.rollback()
            return { "message": gettext("bot not configured") }, 500

class Alive(Resource):
    def post(self):
        botSecret = getBotSecretHeaderInfo()
        try:
            bot = get_bot(botSecret)
            if(bot is None):
                return { "error": gettext("bot not found") }, 404
            else:
                heartbeat = BotHeartbeat(bot_id=bot.id)
                db.session.add(heartbeat)
                db.session.commit()
                return { "success": gettext("alive received") },200
        except:
            current_app.logger.error("Error registering bot alive", exc_info=sys.exc_info())
            return { "error": gettext("alive not recorded") }, 404

class NextJob(Resource):
    def get(self):
        botSecret = getBotSecretHeaderInfo()
        try:
            bot = get_bot(botSecret)
            if(bot is None):
                current_app.logger.info("Bot not found %s" % botSecret)
                return { "error": gettext("bot not found") }, 404
            else:
                bot_job = db.session.query(
                    BotJob.id,
                    BotJob.parameters,
                    BotJob.task_version_id,
                    TaskVersion.task_id,
                    Task.name).filter(BotJob.bot_id == bot.id, 
                                                BotJob.status == "NOT_PROCESSED") \
                    .join(TaskVersion, TaskVersion.id==BotJob.task_version_id) \
                    .join(Task,Task.id==TaskVersion.task_id) \
                    .order_by(BotJob.id.asc()) \
                    .first()
                current_app.logger.info("Bot job found %s" % (bot_job != None))
                json_data={}
                if bot_job:
                    print(bot_job)
                    json_data= {
                        "job_id": str(bot_job.id),
                        "parameters" : bot_job.parameters,
                        "script_id": str(bot_job.task_id),
                        "script_version_id": str(bot_job.task_version_id),
                        "job_entrypoint":bot_job.name+".ipynb",
                        "job_files":[
                            {
                                "filename":bot_job.name+".ipynb",
                                "url":"/api/script"
                            }
                        ]
                    }
                    db.session.query(BotJob) \
                    .filter(BotJob.id == bot_job.id) \
                    .update({
                        BotJob.status:"PROCESSING",
                        BotJob.updated_date:datetime.utcnow(), 
                        BotJob.ovn: BotJob.ovn +1 
                    })
                    db.session.commit()
                
                return json_data,200
        except:
            current_app.logger.error("Error getting next job ", exc_info=sys.exc_info())
            return { "error": gettext("bot not found") }, 404

class JobScript(Resource):
    def get(self):
        botSecret = getBotSecretHeaderInfo()
        scriptId = getHeader("script_id")
        scriptVersionId = getHeader("script_version_id")
        
        try:
            bot = get_bot(botSecret)
            if(bot is None):
                return { "error": gettext("bot not found") }, 404
            else:
                taskBody = db.session.query(TaskVersion.task_body) \
                            .filter(TaskVersion.id == scriptVersionId
                                    , TaskVersion.task_id == scriptId
                                    , TaskVersion.is_active == models.IsActive.V).first()
                if(taskBody):
                    if (type(taskBody.task_body) == bytes):
                        return json.loads(json_2_object(taskBody.task_body.decode('utf-8'))), 200
                    return json.loads(json_2_object(taskBody.task_body)), 200
                else:
                    return { "error": gettext("script not found") }, 500
        except:
            current_app.logger.error("Error getting job script ", exc_info=sys.exc_info())
            return { "error": gettext("bot not found") }, 404

class JobEvidendeDetails(Resource):
    def post(self):
        bot_secret = getBotSecretHeaderInfo()
        job_id = getHeader('job_id')
        error = getHeader('job_error')
        status = getHeader('job_status')
        try:
            if get_bot(bot_secret):
                if error is not None and error != '':
                    bot_job = BotJob.query.get(job_id)
                    if bot_job:
                        bot_job.status = models.Status.ERRORED
                        bot_job.execution_status = status if status else ''
                        db.session.commit()
                
                result = _get_parameter("jobevidence_resource")
                result = result.replace("__JOB_ID__",job_id).replace("__BASE_URI__",request.url_root[:-1])
                return json.loads(json_2_object(result)), 200
            else:
               return { "error": gettext("bot not found") }, 404
        except ParameterNotFoundError as _:
            return { "error": gettext("no evidence detail") }, 500

class ScreenShotDetails(Resource):
    def post(self):
        bot_secret = getBotSecretHeaderInfo()
        job_id = getHeader('job_id')
        try:
            if get_bot(bot_secret):
                result = _get_parameter("printscreen_resource")
                result = result.replace("__JOB_ID__",job_id).replace("__BASE_URI__",request.url_root[:-1])
                return json.loads(json_2_object(result)), 200
            else:
                return { "error": gettext("bot not found") }, 404
        except ParameterNotFoundError as _:
            return { "error": gettext("no screen shot evidence detail") }, 500

class FailurePrintScreen(Resource):
    def post(self):
        parser = reqparse.RequestParser()
        parser.add_argument('job_id',required=True)
        parser.add_argument('extension',required=True)
        #parser.add_argument('file',required=True)

        if 'file' not in request.files:
            return { "error": gettext("no file provided") }, 500
        else:
            file = request.files['file']
            args = parser.parse_args()
            jobId = args['job_id']
            extension = args['extension']
        
            current_app.logger.info("job_id %s, extension %s" % (jobId,extension))
            if jobId != None and extension != None:
                failureEvidence = BotJobFailureEvidence(bot_job_id = jobId, image = file.read())
                db.session.add(failureEvidence)
                db.session.commit()
                return {"message":gettext("print screen received") }, 200
            else:
                return { "error": gettext("no jobId or extension provided") }, 500

class JobEvidence(Resource):
    def post(self):
        parser = reqparse.RequestParser()
        parser.add_argument('job_id',required=True)
        parser.add_argument('extension',required=True)

        args = parser.parse_args()
        job_id = args['job_id']
        extension = args['extension']
        file = request.files['file']
        
        job_evidence = BotJobEvidence(bot_job_id = job_id, evidence = file.read(),extension = extension)
        db.session.add(job_evidence)
        db.session.commit()
        return {"message": gettext("job evidence received") }, 200

class JobStatus(Resource):
    def post(self):
        parser = reqparse.RequestParser()
        parser.add_argument('job_id',required=True)
        parser.add_argument('job_status',required=True)
        parser.add_argument('bot_secret',required=True)

        args = parser.parse_args()
        print(args)
        if not args['bot_secret'] :
            return { "error": gettext("bot not found") }, 500
        job_id = args['job_id']
        job_status = args['job_status']
        #file = request.files['file']
        #bot_job = db.session.query(BotJob).filter(BotJob.id==job_id)
        db.session.query(BotJob) \
                    .filter(BotJob.id == job_id) \
                    .update({
                        BotJob.status:"PROCESSED",
                        BotJob.execution_status:job_status,
                        BotJob.updated_date:datetime.utcnow(), 
                        BotJob.ovn: BotJob.ovn +1 
                    })
        db.session.commit()
        return {"message": gettext("job evidence received") }, 200

def _get_parameter(key):
    """gets the parameter that matchs with the `key`
    
    Parameters
    ----------

    Returns
    -------
    obj:
        the parameter's value

    Raises
    ------
    ParameterNotFoundError
        the specified parameter with key does not exist

    """
    try:
        
        param = Parameter.query \
                .filter(Parameter.parameter_key == key
                        , Parameter.is_active=='V') \
                .first()
        
        if param:
            value = param.varchar_value if param.param_type=='VARCHAR' else None
            value = param.number_value if param.param_type=='NUMBER' else value
            value = param.date_value if param.param_type=='DATE' else value
            return value
        else:
            raise ParameterNotFoundError("The specified parameter %s, does not exist " % key)
    except:
        current_app.logger.error("Error getting parameter ", exc_info=sys.exc_info())
        raise ParameterNotFoundError("The specified parameter %s, does not exist " % key)

def get_parameter_as_json(key):
    """gets the parameter that matchs with the `key`
    
    Parameters
    ----------

    Returns
    -------
    obj:
        the parameter's value as python object

    Raises
    ------
    ParameterNotFoundError
        the specified parameter with key does not exist

    """
    return json.dumps(_get_parameter(key))

def getEvidenceHeaders():
    botSecret = getBotSecretHeaderInfo()
    jobId = getHeader("job_id")
    jobStatus = getHeader("job_status")
    jobError = getHeader("job_error")
    return botSecret, jobId, jobStatus, jobError

def getHeader(headerName):
    result = None
    try:
        result = request.headers[headerName]
    except KeyError:
        result = ""
    return result

def getUserSecretHeaderInfo():
    userSecret = getHeader('user_secret')
    return userSecret

def getBotSecretHeaderInfo():
    botSecret = getHeader('bot_secret')
    return botSecret

def get_bot(botSecret):
    bot = db.session.query(Bot.id
                            , Bot.name
                            , Bot.bot_secret) \
            .filter(Bot.bot_secret == botSecret,
                    Bot.is_active == models.IsActive.V).first()
    return bot

import models