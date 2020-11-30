from flask import flash, redirect, request, current_app
from flask_login import current_user
from flask_babel import _
from app import db
from models import Task, TaskVersion, BotTask
from util import get_extension

def get_invalid_messages(form):
    messages = ''
    for fieldName, errorMessages in form.errors.items():
        for err in errorMessages:
            if len(messages) == 0:
                messages = _('[%(field)s: %(error)s]'
                                ,error=err
                                , field=form[fieldName].label.text)
            else:
                messages = messages + ', ' + _('[%(field)s: %(error)s]'
                                                ,error=err
                                                , field=form[fieldName].label.text)
    return messages

def upload(task_name, file,bot_id=None):
    if file == '' or file == None:
        flash(_('No selected file, please select a file'))
        return redirect(request.url)
    
    task = Task(name=task_name, user= current_user)
    taskVersion = TaskVersion(task = task)
    file_content = file.read()
    extension = get_extension(file.filename)
    current_app.logger.info("File content %s, and extension %s" % (file_content,extension))
    taskVersion.set_task_body(body=file_content, extension=extension)
    if bot_id is not None:
        bot_task = BotTask(bot_id=bot_id, task=task)
        db.session.add(bot_task)
    db.session.add(taskVersion)
    db.session.commit()
    flash(_("Task '%(task)s' was uploaded successfully",task=task_name))