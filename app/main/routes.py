# Import the microframework to create web apps
from flask import render_template, flash, redirect, url_for, request, Response, current_app, g
from flask_login import current_user, login_required
from flask_babel import _, get_locale
from app import db
from app.main import bp
from app.db_helper import play_task, delete_task, get_bots, delete_bot_task, schedule_job_on_bot, schedule_job_on_bots
from app.main.forms import TaskUploadForm, SearchForm, ScheduleForm, days, EmptyDelBotForm
from app.util.static_models import BotJobSM
from app.main.util import get_invalid_messages, upload
from models import User, Task, TaskVersion, Bot, BotTask, BotScheduledJob
import os
import sys
from datetime import datetime

@bp.before_app_request
def before_request():
    if current_user.is_authenticated:
        g.search_form = SearchForm()
        g.task_upload_form = TaskUploadForm()
        g.schedule_form = ScheduleForm()
        #g.schedule_form.periodicity.data = 'MINUTE'
        #g.schedule_form.at_minutes.data = '1'
    g.locale = str(get_locale())

@bp.route('/', methods=['POST','GET'])
@bp.route('/index', methods=['POST','GET'])
@login_required
def index():
    form = g.task_upload_form
    schedule_form = g.schedule_form
    if request.method == 'POST':
        if schedule_form.periodicity.data != None:
            task_id = schedule_form.scheduled_task_id.data
            bots = schedule_form.bots_comma_list.data
            schedule_form.init_date.data = request.form['date1']
            schedule_form.end_date.data = request.form['date2']
            schedule_form.init_time.data = request.form['time1']
            schedule_form.end_time.data = request.form['time2']
            as_scheduled_str = schedule_form.as_scheduled_str()
            # Pendiente a modificar para su ejecución. // db_helper.py -> línea 181
            #message = schedule_job_on_bots(task_id=task_id, bots=bots, as_scheduled_str=as_scheduled_str)
            
            if schedule_form.periodicity.data == 'MINUTE':
                minutes = schedule_form.at_minutes.data
                as_scheduled_str = schedule_form.as_scheduled_str()
                print(as_scheduled_str)
                
            elif schedule_form.periodicity.data == 'HOUR':
                schedule_form.at_minutes.data = schedule_form.at_hour.data
                as_scheduled_str = schedule_form.as_scheduled_str()
                print(as_scheduled_str)
                
            elif schedule_form.periodicity.data == 'DAY':
                days = schedule_form.on_day.data
                as_scheduled_str = schedule_form.as_scheduled_str()
                print(as_scheduled_str)
                
            elif schedule_form.periodicity.data == 'WEEK':
                weeks = schedule_form.at_week.data
                day_week = request.form['day']
                if day_week == 'Dom':
                    schedule_form.the_day.data = 'sunday'
                elif day_week == 'Lun':
                    schedule_form.the_day.data = 'monday'
                elif day_week == 'Mar':
                    schedule_form.the_day.data = 'tuesday'
                elif day_week == 'Mier':
                    schedule_form.the_day.data = 'wednesday'
                elif day_week == 'Jue':
                    schedule_form.the_day.data = 'thursday'
                elif day_week == 'Vie':
                    schedule_form.the_day.data = 'friday'
                elif day_week == 'Sab':
                    schedule_form.the_day.data = 'saturday'
                    
                as_scheduled_str = schedule_form.as_scheduled_str()
                print(as_scheduled_str)
                
            elif schedule_form.periodicity.data == 'MONTHLY':
                months = schedule_form.on_month_day.data
                as_scheduled_str = schedule_form.as_scheduled_str()
                print(as_scheduled_str)
                
            elif schedule_form.periodicity.data == 'YEARLY':
                years = schedule_form.on_month_day2.data
                month_year = request.form['year']
                if month_year == 'Ene':
                    schedule_form.on_month.data = 'January'
                elif month_year == 'Feb':
                    schedule_form.on_month.data = 'February'
                elif month_year == 'Mar':
                    schedule_form.on_month.data = 'March'
                elif month_year == 'Abr':
                    schedule_form.on_month.data = 'April'
                elif month_year == 'May':
                    schedule_form.on_month.data = 'May'
                elif month_year == 'Jun':
                    schedule_form.on_month.data = 'June'
                elif month_year == 'Jul':
                    schedule_form.on_month.data = 'July'
                elif month_year == 'Ago':
                    schedule_form.on_month.data = 'August'
                elif month_year == 'Sep':
                    schedule_form.on_month.data = 'September'
                elif month_year == 'Oct':
                    schedule_form.on_month.data = 'October'
                elif month_year == 'Nov':
                    schedule_form.on_month.data = 'November'
                elif month_year == 'Dic':
                    schedule_form.on_month.data = 'December'
                    
                as_scheduled_str = schedule_form.as_scheduled_str()
                print(as_scheduled_str)
                
        else:
            schedule_form.init_date.data = request.form['uniq_init_date']
            schedule_form.init_time.data = request.form['uniq_init_time']
            init = schedule_form.init_date.data
            time = schedule_form.init_time.data
            print(init)
            print(time)
            
        return redirect(url_for('auth.login'))
            
    tasks = current_user.get_tasks()
    bots= get_bots(1)
    current_date = datetime.now()
    current_time = str(current_date.time())
    dates = {
        'tasks': tasks,
        'bots': bots,
        'current_date': current_date,
        'current_time': current_time,
    }
    return render_template('index.html', **dates)

@bp.route("/tasks/<page>", methods = ["GET"])
@login_required
def tasks(page=1):
    q = request.args.get('q','', type=str)
    page = int(page)
    if q:
        tasks, _ = Task.search(f'(user_id:{current_user.id}) AND {q}*'
                                ,page=page
                                ,per_page=current_app.config['TASK_PER_PAGE'])
    else:
        tasks = current_user.get_tasks(page)
    return render_template("fragments/tasks.html", tasks=tasks)

@bp.route("/tasks/<id>/executions/<page>", methods = ["GET"])
@login_required
def task_exec_details(id, page=1):
    q = request.args.get('q','', type=str)
    page = int(page)
    id = int(id)
    if q:
        tasks, _ = Task.search(f'(user_id:{current_user.id}) AND {q}*'
                                ,page=page
                                ,per_page=current_app.config['TASK_PER_PAGE'])
    else:
        task = Task.query.get(id)
        exec_details = task.get_execution_details(page)
    return render_template("fragments/task-execution-details.html", exec_details=exec_details)

@bp.route("/bot/<id>/tasks/<page>", methods = ["GET"])
@login_required
def bot_tasks(id, page=1):
    g.task_upload_form.bot_id = id
    q = request.args.get('q','', type=str)
    page = int(page)
    if q:
        tasks, _ = Task.search(
            expression= q + '*'
            ,page=page
            ,per_page=current_app.config['TASK_PER_PAGE']
            ,filter=db.session.query(BotTask.task_id).filter(BotTask.bot_id==id, BotTask.is_active == 'V')
        )
    else:
        tasks = Bot.query.get(id).get_tasks(page)
    return render_template("fragments/tasks.html", tasks=tasks)

@bp.route("/task/<id>", methods = ["POST","PATCH", "GET"])
@login_required
def playTask(id):
    status = None
    if request.method == 'POST':
        json = request.get_json()
        botSecretList = json["bots"]
        job = BotJobSM(id, None, botSecretList)
        status = play_task(job)
    elif request.method == 'PATCH':
        status = delete_task(id)
    elif request.method == 'GET':
        task = Task.query.get(id)
        return render_template('fragments/task-details-dialog.html',task_det=task)
    return render_template("fragments/message.html",message=status)

@bp.route("/bot/<id>/task/<task>", methods = ["POST","PATCH"])
@login_required
def manageBotTasks(id, task):
    status = None
    if request.method == 'POST':
        json = request.get_json()
        botSecretList = json["bots"]
        job = BotJobSM(id, None, botSecretList)
        status = play_task(job)
    elif request.method == 'PATCH':
        status = delete_bot_task(id,task)
    return render_template("fragments/message.html",message=status)

@bp.route("/profile", methods = ["GET"])
@login_required
def profile():
    user = User.query.get(current_user.id)
    return render_template("profile.html", user=user)

@bp.route("/download-bot-script/<platform>", methods = ["GET"])
@login_required
def downloadBotScript(platform):
    if not platform:
        flash(_("Please provide a platform to download the bot configurer"))
        return redirect(url_for('main.profile'))
    else:
        content = None
        extension = '.bat' if platform == 'windows' else '.sh'
        fileName = "/app/util/%s_configure_portal%s" % (platform, extension)
        with open(os.path.dirname(current_app.root_path) + fileName, 'r') as doc:
            # Reads the file's content
            content = doc.read()
            url = current_app.config['API_URL'] or request.url_root[:-1] # to remove the last / in URL
            content = content.replace("__PORTAL__",url)
            content = content.replace("__USER_SECRET__",current_user.user_secret)
        return Response(content
                        , mimetype= "application/bat"
                        , headers={
                            f"Content-Disposition":"attachment;filename=%s" % fileName[5:]
                            }
                        )

@bp.route("/download-fix-connection/<platform>", methods = ["GET"])
@login_required
def downloadScriptFixConn(platform):
    if not platform:
        flash(_("Please provide a platform to download the bot configurer"))
        return redirect(url_for('main.profile'))
    else:
        content = None
        fileName = "/app/util/%s_restart_python_as_bot.bat" % platform
        with open(os.path.dirname(current_app.root_path) + fileName, 'r') as doc:
            # Reads the file's content
            content = doc.read()
        return Response(content
                        , mimetype= "application/bat"
                        , headers={
                            f"Content-Disposition":"attachment;filename=%s" % fileName[5:]
                            }
                        )

@bp.route("/bots", methods = ["GET"])
@login_required
def bots_page():
    bots = get_bots(1)
    return render_template("bots.html", bots=bots)

@bp.route("/bots/<page>", methods = ["GET"])
@login_required
def bots(page):
    q = request.args.get('q','', type=str)
    page = 1 if page is None else int(page)
    if q:
        bots, total = Bot.search(f'(user_id:{current_user.id}) AND {q}*'
                                , page
                                , current_app.config['BOTS_PER_PAGE']
                                )
        bots.total = total
    else:
        bots = get_bots(page)
    return render_template("fragments/bots.html", bots=bots)

@bp.route('/bot/<id>', methods=['POST','GET'])
@login_required
def bot(id):
    form = g.task_upload_form
    schedule_form = g.schedule_form
    if form.validate_on_submit() or form.validate():
        file = request.files[form.task_file.name]
        upload(task_name=form.task_name.data,file=file,bot_id=id)
        return redirect(url_for('main.bot',id=id))
    if 'schedule-btn' in request.form and \
        schedule_form.validate_on_submit() or schedule_form.validate():
        task_id = schedule_form.scheduled_task_id.data
        schedule_form.periodicity.data = request.form['periodicity'] #for some reason flask form holds original value and request.form the submited valur
        schedule_form.on_day.data = request.form['on_day']
        schedule_form.on_month.data = request.form['on_month']
        schedule_form.at_hour.data = request.form['at_hour']
        schedule_form.at_minutes.data = request.form['at_minutes']
        as_scheduled_str = schedule_form.as_scheduled_str()
        message = schedule_job_on_bot(task_id=task_id, bot_id=id, as_scheduled_str=as_scheduled_str)
        flash(message)
        return redirect(url_for('main.bot',id=id))
    if (schedule_form.submit.data and request.method == 'POST' \
        and schedule_form.validate_on_submit() == False):
        messages = get_invalid_messages(schedule_form)
        flash(_("Schedule not configured, please verify: %(messages)s",messages=messages))
        return redirect(url_for('main.bot',id=id))
    if request.method == 'POST' and 'bot_delete_btn' in request.form:
        bot = Bot.query.get(id)
        if bot:
            try:
                bot.delete()
                db.session.commit()
                flash(_('Bot %(bot)s deleted successfully',bot=bot.name))
                return redirect(url_for('main.index'))
            except:
                flash(_('An error occurs while deleting bot %(bot)s',bot=bot.name))
                return redirect(url_for('main.bot',id=id))
    form.bot_id = id
    bot = Bot.query.get(id)
    del_form=EmptyDelBotForm()
    return render_template("bot.html", bot=bot, del_form=del_form)

@bp.route('/task/<id>/schedules/<page>')
@login_required
def get_tasks_schedules(id, page):
    sch_tasks = Task.query.get(id).get_scheduled_tasks(page=int(page))
    return render_template('fragments/scheduled-tasks.html',sch_tasks=sch_tasks,task_id=id)

@bp.route('/schedules/<id>', methods=['PATCH'])
@login_required
def handle_schedule(id):
    if request.method == 'PATCH':
        bot_job = BotScheduledJob.query.get(id)
        if bot_job:
            bot_name = bot_job.bot.name if bot_job.bot else ''
            job_desc = current_app.extensions['botic'].translate(bot_job.string_rep()[0])
            message = _('Job %(job)s deleted successfully from bot %(bot)s'
                        ,job=job_desc,bot=bot_name)
            try:
                bot_job.delete()
                db.session.commit()
            except:
                message = _('Job %(job)s was not deleted from bot %(bot)s due to an error'
                            ,job=job_desc,bot=bot_name)
                current_app.logger.error("Error deleting scheduled job", exc_info=sys.exc_info())
        return render_template("fragments/message.html",message=message)