import sys
from models import TaskVersion, Task, BotJob, Bot, Status, BotHeartbeat, BotTask, BotScheduledJob
from datetime import datetime, timedelta
from app.util.static_models import BotJobSM
from exceptions import ScriptNotFoundError
from flask_login import current_user
from flask import current_app
from flask_babel import _
from app import db
import logging

def get_bots(page=1):
    """gets user's bots.

    Parameters
    ----------
    

    Returns
    -------
    flask_sqlalchemy.Pagination
    """
    bots = Bot.query.filter(
            Bot.user_id == current_user.id, 
            Bot.is_active == 'V') \
        .order_by(Bot.id.desc()) \
        .paginate(page=page, per_page=current_app.config['BOTS_PER_PAGE'])
    
    return bots

def play_task(bot_job_sm: BotJobSM):
    """Plays the task with `bot_job_sm.id` in the specified `bot_job_sm.botSecretLists`.

    Parameters
    bot_job_sm: BotJobSM
        the complex structure used to create 

    Returns
    -------
    str:
        the execution status (ERROR, COMPLETED)
    """

    try:
        for b in bot_job_sm.botSecretLists:
            if bot_job_sm.taskVersionId == None:
                bot_job_sm.taskVersionId = get_task_last_rev(bot_job_sm.taskId)
            botJob = BotJob(bot = Bot.query.filter(Bot.bot_secret == b).first(), \
                            task_version_id = bot_job_sm.taskVersionId, \
                            parameters = bot_job_sm.parameters, \
                            status = Status.NOT_PROCESSED)
            db.session.add(botJob)
        
        db.session.commit()
    except:
        current_app.logger.error("Error saving bot job", exc_info=sys.exc_info())
        db.session.rollback()
        return _("There was an error and the execution was not launch")

    return _("The task was configured to launch")

def get_task_body(taskId):
    """gets user's scripts.

    Parameters
    ----------

    Returns
    -------
    list
        {
            "script_id":"the script id",
            "name":"the script name"
        }
    """
    task = db.session.query(
        Task.id, Task.user_id, Task.name
    ).filter(Task.user_id == current_user.id).subquery()
    query = TaskVersion.query.join(task, TaskVersion.task_id == task.c.id)
    result = []
    for t in query.filter(Task.is_active == 'V').all():
        result.append({"script_id":t.id, "name":t.task.name})
    return result

def get_task_last_rev(task_id):
        """gets the task last revision that match with `task_id`.

        Parameters
        ----------
        task_id: int
            the task id
        
        Returns
        -------
        int
            the task last revision

        Raises
        ------
        ScriptNotFoundError
            the script does not exist with id and version combination
        """
        try:
            taskVersion = db.session.query(
                TaskVersion.task_id, db.func.max(TaskVersion.id).label('last_version_id')
            ).group_by(TaskVersion.task_id).filter(TaskVersion.task_id == task_id)
            row = taskVersion.first()
            if row != None:
                value = row.last_version_id
                return value
            
            raise ScriptNotFoundError("The task with id %s does not exist" % (task_id))
        except:
            current_app.logger.error("Error in get_task_last_rev", exc_info=sys.exc_info())
        raise ScriptNotFoundError("The task with id %s does not exist" % (task_id))

def delete_task(id):
        """deletes the task `id`

        Parameters
        ----------
        id: int
            the task id
        
        Returns
        -------
        str: 
            a message indicating that the task was deleted

        """
        task = Task.query.get(id)
        task.delete()
        db.session.commit()
        return _('The task was deleted')
        

def delete_bot_task(bot_id, bot_task_id):
        """deletes the task `bot_task_id` that belongs to `bot_id`

        Parameters
        ----------
        bot_id: int
            the bot id
        bot_task_id: int
            the task id that belongs to bot
        
        Returns
        -------
        str: 
            a message indicating that the task was deleted

        """
        task = BotTask.query.filter(BotTask.bot_id==bot_id, BotTask.task_id==bot_task_id).first_or_404()
        task.delete()
        db.session.commit()
        return _('The task was deleted')

# Función a analizar.
def schedule_job_on_bot(task_id, bot_id, as_scheduled_str):
    bot_sch_job = None
    try:
        bot_sch_job = BotScheduledJob(bot_id = bot_id,
                                        task_id = task_id,
                                        parameters = "",
                                        when=as_scheduled_str)
        db.session.add(bot_sch_job)
        db.session.commit()
        bot_sch_job.enqueue() #updates queue_identifier and use BotScheduledJob.id, could be improve, surely
        db.session.commit() #this is needed for enqueue updates
        return _('The task was scheduled')
    except:
        current_app.logger.error("Error in schedule_job_on_bot", exc_info=sys.exc_info())
        db.session.rollback()
        if bot_sch_job:
            try:
                bot_sch_job.dequeue()
            except:
                current_app.logger.error("Error in schedule_job_on_bot dequeu", exc_info=sys.exc_info())

    return _('There was an error and the task was not scheduled')

# Función a analizar.
def schedule_job_on_bots(task_id, bots, as_scheduled_str):
    bot_sch_job = None
    bot_list = bots.split(',')
    try:
        for idx in range(len(bot_list)):
            bot = Bot.query.filter(Bot.bot_secret == bot_list[idx]).first()
            if bot:
                # class BotScheduledJob // models.py -> línea 417
                bot_sch_job = BotScheduledJob(bot_id = bot.id,
                                                task_id = task_id,
                                                parameters = "",
                                                when=as_scheduled_str)
                db.session.add(bot_sch_job)
                db.session.commit()
                bot_sch_job.enqueue() #updates queue_identifier and use BotScheduledJob.id, could be improve, surely
                db.session.commit() #this is needed for enqueue updates
        return _('The task was scheduled')
    except:
        current_app.logger.error("Error in schedule_job_on_bot", exc_info=sys.exc_info())
        db.session.rollback()
        if bot_sch_job:
            try:
                bot_sch_job.dequeue()
            except:
                current_app.logger.error("Error in schedule_job_on_bot dequeu", exc_info=sys.exc_info())

    return _('There was an error and the task was not scheduled')