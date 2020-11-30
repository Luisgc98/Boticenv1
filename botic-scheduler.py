import sys
import schedule
from datetime import date, datetime
import time
import json
from app import create_app, db
from models import BotJob, BotScheduledJob, Bot, TaskVersion, Task, Status, ScheduledJobStatus, BotJobType

app = create_app()
app.app_context().push()

def checkChannelsForNews():
    try:
        message = p.get_message()
        if message and type(message['data']) != int:
            return message['data']
    except:
        app.logger.error("Error retrieving messages", exc_info=sys.exc_info())
    return

def scheduleYearMonth():
    qMonth = app.redis.hgetall("MONTHLY")
    qYear = app.redis.hgetall("YEARLY")

    if qMonth:
        for queue in qMonth:
            processScheduleJob(qMonth[queue],True)
    if qYear:
        for queue in qYear:
            processScheduleJob(qYear[queue],True)
    return

#F

# Función a analizar y donde se va a trabajar.
def processScheduleJob(metadata, flagCtrl=False):
    if metadata:
        #Recuperando parametros de metadatos.
        data = json.loads(metadata)
        identifier = data['identifier']
        #Validando canal del mensaje.
        if data['queueName'] == 'DELETE':
            schedule.clear(identifier)
            app.logger.info(f"Tarea de calendarizado eliminada: {identifier}")
        else:
            message = ""
            periodicity=data['periodicity']
            # Ejemplo de dato a evaluar: x = 'YEARLY;April;20:2021-04-20:2022-04-20/10:00/00:00'
            #Validando tipo de ejecucion
            # Posible formula para separar los tiempos en una lista: time = x[x.find('/')+1:].split('/')
            # Posible formula para seprara las fechas en una lista, las posiciones son 1 y 2: date = x[x.find(';')+1 : x.find('/')].split(':')
            if data['queueName'] == 'MINUTE':
                schedule.every(int(periodicity)).minutes.do(executeTask,data).tag(identifier)
            elif data['queueName'] == 'HOUR':
                schedule.every().hour.at(f":{periodicity}").do(executeTask,data).tag(identifier)
            elif data['queueName'] == 'DAY':
                schedule.every().day.at(periodicity).do(executeTask,data).tag(identifier)
            elif data['queueName'] == 'WEEK':
                splitPeriod = periodicity.lower().split(";")
                days = splitPeriod[0]
                periodicity = splitPeriod[1]
                if("monday" in days):
                    schedule.every().day.monday.at(periodicity).do(executeTask,data).tag(identifier)
                if("tuesday" in days):
                    schedule.every().day.tuesday.at(periodicity).do(executeTask,data).tag(identifier)
                if("wednesday" in days):
                    schedule.every().day.wednesday.at(periodicity).do(executeTask,data).tag(identifier)
                if("thursday" in days):
                    schedule.every().day.thursday.at(periodicity).do(executeTask,data).tag(identifier)
                if("friday" in days):
                    schedule.every().day.friday.at(periodicity).do(executeTask,data).tag(identifier)
                if("saturday" in days):
                    schedule.every().day.saturday.at(periodicity).do(executeTask,data).tag(identifier)
                if("sunday" in days):
                    schedule.every().day.sunday.at(periodicity).do(executeTask,data).tag(identifier)
            elif data['queueName'] == 'MONTHLY':
                splitPeriod = periodicity.lower().split(";")
                day = splitPeriod[0]
                hour = splitPeriod[1]
                currentDate = datetime.now()
                inputDate = datetime.strptime(day + "T" + hour, "%dT%H:%M") 

                if int(day) == currentDate.day and flagCtrl == False:
                    if(datetime.strptime(currentDate.strftime("%dT%H:%M"),"%dT%H:%M") < inputDate):
                        schedule.every().day.at(hour).do(executeTask,data).tag(identifier)
                        message = f"Nueva tarea mensual calendarizada: {identifier} periodo: {hour}"
                    else:
                        message = "La tarea mensual será programada en otro momento."
                elif int(day) == currentDate.day + 1 and flagCtrl == True:
                    schedule.every().day.at(hour).do(executeTask,data).tag(identifier)
                    message = f"Nueva tarea mensual calendarizada: {identifier} periodo: {hour}"
                else:
                    message = "La tarea mensual será programada en otro momento."
            elif data['queueName'] == 'YEARLY':
                splitPeriod = periodicity.lower().split(";")
                day = splitPeriod[0]
                month = splitPeriod[1]
                hour = splitPeriod[2]
                currentDate = datetime.now()
                currentDateFormat = datetime.strptime(currentDate.strftime("%d/%mT%H:%M"),"%d/%mT%H:%M")
                inputDate = datetime.strptime(day + "/" + month + "T" + hour, "%d/%mT%H:%M") 
                if(int(month) == currentDate.month):
                    if int(day) == currentDate.day and flagCtrl == False:
                        if(currentDateFormat < inputDate):
                            schedule.every().day.at(hour).do(executeTask,data).tag(identifier)
                            message = f"Nueva tarea anual calendarizada: {identifier} periodo: {hour}"
                        else:
                            message = "La tarea anual será programada en otro momento."
                    elif int(day) == currentDate.day + 1 and flagCtrl == True:
                        schedule.every().day.at(hour).do(executeTask,data).tag(identifier)
                        message = f"Nueva tarea anual calendarizada: {identifier} periodo: {hour}"
                    else:
                        message = "La tarea anual será programada en otro momento."
                else:
                    message = "La tarea anual será programada en otro momento."
            if message != "":
                app.logger.info(message)
            else:
                app.logger.info(f"Nueva tarea calendarizada:{periodicity} {data}")

    else:
        app.logger.error("La tarea no puede ser programada.", exc_info=sys.exc_info())

def executeTask(data):
    task =data
    if(task['queueName'] == 'MONTHLY'):
        identifier = task['identifier']
        app.logger.info(f"Ejecutando tarea mensual: {data}")
        app.logger.info("Tarea ejecutada.")
        app.logger.info("Limpiando tarea de registro diario")
        schedule.clear(identifier)
        app.logger.info(f"Tarea de calendarizado eliminada: {identifier} con éxito.")
    elif(task['queueName'] == 'YEARLY'):
        identifier = task['identifier']
        app.logger.info(f"Ejecutando tarea anual: {data}")
        app.logger.info("Tarea ejecutada.")
        app.logger.info("Limpiando tarea de registro diario")
        schedule.clear(identifier)
        app.logger.info(f"Tarea de calendarizado eliminada: {identifier} con éxito.")
    else:
        app.logger.info(f"Ejecutando tarea: {data}")

    task_metadata = json.loads(task['metadata'])
    scheduled = BotScheduledJob.query.get(task_metadata['id'])
    try:
        play_task(task_id=scheduled.task_id,
                    bot_id=scheduled.bot_id, 
                    parameters=scheduled.parameters)
        scheduled.status = ScheduledJobStatus.PROCESSING
        db.session.commit()
    except:
        db.session.rollback()
        app.logger.error("Error in get_task_last_rev", exc_info=sys.exc_info())

def getQueuesFromServer():
    qMinute = app.redis.hgetall("MINUTE")
    qHour = app.redis.hgetall("HOUR")
    qDay = app.redis.hgetall("DAY")
    qWeek = app.redis.hgetall("WEEK")
    qMonth = app.redis.hgetall("MONTHLY")
    qYear = app.redis.hgetall("YEARLY")

    if qMinute:
        for queue in qMinute:
            processScheduleJob(qMinute[queue])
    if qHour:
        for queue in qHour:
            processScheduleJob(qHour[queue])
    if qDay:
        for queue in qDay:
            processScheduleJob(qDay[queue])
    if qWeek:
        for queue in qWeek:
            processScheduleJob(qWeek[queue])
    if qMonth:
        for queue in qMonth:
            processScheduleJob(qMonth[queue])
    if qYear:
        for queue in qYear:
            processScheduleJob(qYear[queue])
    return

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
    """
    
    taskVersion = db.session.query(
        TaskVersion.task_id, db.func.max(TaskVersion.id).label('last_version_id')
    ).group_by(TaskVersion.task_id).filter(TaskVersion.task_id == task_id)
    row = taskVersion.first()
    if row != None:
        value = row.last_version_id
        return value

def play_task(task_id, bot_id, parameters):
    """Plays the task with `bot_job_sm.id` in the specified `bot_job_sm.botSecretLists`.

    Parameters
    task_id: int
        the task id to schedule
    bot_id: int
        the bot id that is going to perform the task
    parameters: str
        the additional parameters to execute the task

    Returns
    -------
    """

    task_version_id = get_task_last_rev(task_id)
    botJob = BotJob(bot_id = bot_id, \
                    task_version_id = task_version_id, \
                    parameters = parameters, \
                    status = Status.NOT_PROCESSED, \
                    job_type = BotJobType.SCHEDULED)
    db.session.add(botJob)

if __name__ == "__main__":
    try:
        p = app.redis.pubsub()
        app.logger.info("Recuperación y calendarizado de colas existentes")
        getQueuesFromServer()
        app.logger.info("Subscrito a colas MINUTE, HOUR, DAY, WEEK, MONTHLY y DELETE.")
        p.subscribe('MINUTE','HOUR','DAY','WEEK','MONTHLY','YEARLY',"DELETE")
        while True:
            #Revisando tareas por ejecutar
            schedule.run_pending()
            #Creando subscripcion mensual y anual
            schedule.every().day.at("23:59").do(scheduleYearMonth)
            #Revisando si existe nuevas colas en bus de datos.
            metadata = checkChannelsForNews()
            if metadata:
                processScheduleJob(metadata)
            time.sleep(1)
    except:
        app.logger.error('Unhandled exception',exc_info=sys.exc_info())