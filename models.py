from time import time
import jwt
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime, timedelta
from app import db
from flask_login import UserMixin, current_user
from flask import current_app
from util import get_proper_file_content
import enum
import json
from util import encode
from app.search import add_to_index, remove_from_index, query_index
from app.enqueuer import add_element_to_queue, remove_element_from_queue
from flask_sqlalchemy import Pagination

class Status(enum.Enum):
    NOT_PROCESSED = "NOT_PROCESSED"
    PROCESSED = "PROCESSED"
    ERRORED = "ERRORED"
    PROCESSING = "PROCESSING"

class IsActive(enum.Enum):
    V = "V"
    F = "F"

class ScheduledJobStatus(enum.Enum):
    NOT_PROCESSED = 'NOT_PROCESSED'
    COMPLETED = 'COMPLETED'
    N_REPEAT_LEFT = 'N_REPEAT_LEFT'
    PROCESSING = 'PROCESSING'

class BotJobType(enum.Enum):
    IMMEDIATE = 'IMMEDIATE'
    SCHEDULED = 'SCHEDULED'

class SearchableMixin(object):
    @classmethod
    def search(cls, expression, page, per_page, filter=None):
        """search for full text 
        
        Parameters
        ----------
        cls: str
            the class to search
        expression: str
            the search query or search expressions
        """
        ids, total = query_index(cls.__tablename__,expression, page, per_page)
        if total == 0:
            pagination = Pagination(query=None, page=page, per_page=per_page, 
                                total=total, items = cls.query.filter_by(id=0))
            return pagination,0
        when = []
        for i in range(len(ids)):
            when.append((ids[i],i))
        
        if filter:
            results = cls.query.filter(cls.id.in_(ids)
                                        ,cls.id.in_(filter)
                                        ,cls.is_active == IsActive.V if hasattr(cls,'is_active') else 1 == 1) \
                        .order_by(db.case(when,value=cls.id))
        else:
            results = cls.query.filter(cls.id.in_(ids)
                                        ,cls.is_active == IsActive.V if hasattr(cls,'is_active') else 1 == 1
                                    ).order_by(db.case(when,value=cls.id))
        pagination = Pagination(query=None, page=page, per_page=per_page, 
                                total=total, items = results.all())
        return pagination, total

    @classmethod
    def before_commit(cls, session):
        session._changes = {
            'add': list(session.new),
            'update': list(session.dirty),
            'delete': list(session.deleted)
        }

    @classmethod
    def after_commit(cls, session):
        for obj in session._changes['add']:
            if isinstance(obj, SearchableMixin):
                add_to_index(obj.__tablename__, obj)
        for obj in session._changes['update']:
            if isinstance(obj, SearchableMixin):
                if isinstance(obj, BaseIsActiveMixin):
                    if obj.is_active == IsActive.F:
                        remove_from_index(obj.__tablename__, obj)
                    else:
                        add_to_index(obj.__tablename__, obj)
                else:
                    add_to_index(obj.__tablename__, obj)
        for obj in session._changes['delete']:
            if isinstance(obj, SearchableMixin):
                remove_from_index(obj.__tablename__, obj)
        session._changes = None

    @classmethod
    def reindex(cls):
        query = cls.query if not hasattr(cls, 'is_active') else cls.query.filter(cls.is_active==IsActive.V)
        for obj in query:
            add_to_index(cls.__tablename__, obj)

db.event.listen(db.session, 'before_commit', SearchableMixin.before_commit)
db.event.listen(db.session, 'after_commit', SearchableMixin.after_commit)

class BaseMixin(db.Model):
    __abstract__ = True
    creation_date = db.Column(db.DateTime, default=datetime.utcnow)
    created_by = db.Column(db.Integer)
    updated_date = db.Column(db.DateTime, default=datetime.utcnow)
    updated_by = db.Column(db.Integer)
    ovn = db.Column(db.Integer,default=1)

class BaseIsActiveMixin(BaseMixin):
    __abstract__ = True
    is_active = db.Column(db.Enum(IsActive), nullable=False, default=IsActive.V)
    
    def delete(self):
        self.is_active = IsActive.F
        self.updated_date = datetime.utcnow()
        self.updated_by = current_user.id
        self.ovn = 1 if self.ovn is None else self.ovn + 1

class User(UserMixin, BaseIsActiveMixin):
    """defines the `user` table

    Attributes
    ----------
    user_secret: str
        the user secret identifier
    first_name: str
        user first name
    last_name: str
        user last name
    email: str
        user email
    password_hash: str
        password hashed value
    is_active: Enum IsActive (V and F values)

    Methods
    -------
    set_password()

    """

    __table_args__ = (
        db.CheckConstraint("is_active IN ('V','F')", name="user_is_active_ck"),
    )

    id = db.Column(db.Integer, primary_key=True, nullable=False)
    user_secret	= db.Column(db.String(100), index=True, unique=True, nullable=False)
    first_name 	= db.Column(db.String(50) , nullable=False)
    last_name = db.Column(db.String(100) , nullable=False)
    email = db.Column(db.String(50), nullable=False, unique=True)
    password_hash = db.Column(db.String(100) , nullable=False)
    addresses = db.relationship('Address', backref='user', cascade='save-update')
    bots = db.relationship("Bot", backref="user", lazy='dynamic')
    task = db.relationship('Task', backref='user',lazy='dynamic')

    def __repr__(self):
        return '<User first Name: {}, last Name: {}, email: {}, is_active: {}>' \
                .format(self.first_name, self.last_name, self.email, self.is_active)

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def set_user_secret(self, secret):
        self.user_secret = encode(secret)

    def check_password(self,password):
        return check_password_hash(self.password_hash, password)
    
    def get_reset_password_token(self, expires_in=600):
        return jwt.encode(
            {"reset_password": self.id, "exp": time() + expires_in}
            , current_app.config['SECRET_KEY']
            , algorithm='HS256').decode('utf-8')

    @staticmethod
    def verify_reset_password_token(token):
        try:
            id = jwt.decode(token, current_app.config['SECRET_KEY'],
                            algorithms=['HS256'])['reset_password']
        except:
            return
        return User.query.get(id)

    def get_tasks(self, page=1):
        user_tasks = Task.query.filter(Task.user_id == current_user.id, 
                            Task.is_active == 'V') \
        .order_by(Task.id.desc()) \
        .paginate(page=page,per_page=current_app.config['TASK_PER_PAGE'])
        return user_tasks

class Address(BaseIsActiveMixin):

    __table_args__ = (
        db.CheckConstraint("is_active IN ('V','F')", name="address_is_active_ck"),
    )

    id = db.Column(db.Integer, primary_key=True, nullable=False)
    city = db.Column(db.String(100), nullable=False)
    state = db.Column(db.String(100), nullable=False)
    municipality = db.Column(db.String(100), nullable=False)
    street = db.Column(db.String(300), nullable=False)
    postal_code	= db.Column(db.String(5), nullable=False)
    interior_number	= db.Column(db.String(10), nullable=False)
    exterior_number	= db.Column(db.String(10))
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))

    def __repr__(self):
        return "<Adress city: {}, state: {}, municipality: {}, street: {}, postalCode: {}, isActive: {}> " \
            .format(self.city, self.state, self.municipality, self.street, self.postal_code, self.is_active)

class Bot(SearchableMixin, BaseIsActiveMixin):

    __searchable__ = ['name','description','user_id']
    __table_args__ = (
        db.CheckConstraint("is_active IN ('V','F')", name="bot_is_active_ck"),
    )

    id = db.Column(db.Integer, primary_key=True, nullable=False)
    name = db.Column(db.String(80), nullable=False)
    description = db.Column(db.String(300))
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    bot_secret = db.Column(db.String(100), nullable=False)	
    botJob = db.relationship('BotJob', backref='bot',lazy='dynamic')
    task = db.relationship('BotTask', backref='bot', lazy='dynamic')
    scheduled_job = db.relationship('BotScheduledJob', backref='bot', lazy='dynamic')

    def set_bot_secret(self, bot_secret):
        self.bot_secret = encode(bot_secret)

    @property
    def is_connected(self):
        return len(db.session.query(BotHeartbeat.bot_id).filter(
            BotHeartbeat.registered_at >=  datetime.utcnow()+ timedelta(seconds= -31)
            ,BotHeartbeat.bot_id == self.id
        ).all()) > 0

    @property
    def total_of_tasks(self):
        return db.session.query(db.func.count(BotTask.id)) \
                .filter(BotTask.bot_id == self.id 
                        ,BotTask.is_active == IsActive.V).scalar()

    @property
    def total_of_scheduled(self):
        return db.session.query(db.func.count(BotScheduledJob.id)) \
                .filter(BotScheduledJob.bot_id == self.id 
                        ,BotScheduledJob.is_active == IsActive.V).scalar()

    def get_tasks(self, page):
        bot_tasks = BotTask.query.filter(
            BotTask.bot_id == self.id, 
            BotTask.is_active == IsActive.V
        ).subquery()
        tasks = db.session.query(Task).filter(Task.is_active == IsActive.V) \
            .join(bot_tasks, bot_tasks.c.task_id == Task.id)\
            .order_by(Task.id.desc())
        return tasks.paginate(page=page,per_page=current_app.config['TASK_PER_PAGE'])

    def delete(self):
        super().delete()
        jobs = BotScheduledJob.query.filter(BotScheduledJob.bot_id == self.id).all()
        for job in jobs:
            job.delete()

    def __repr__(self):
        return '<Bot name: {}, is_active: {}>'.format(self.name, self.is_active)

class BotHeartbeat(BaseMixin):
    id = db.Column(db.Integer, primary_key=True, nullable=False)
    bot_id = db.Column(db.Integer, db.ForeignKey('bot.id'))
    registered_at = db.Column(db.DateTime, default=datetime.utcnow)

    def __repr__(self):
        return '<BotHeartbeat bot name: {}, registered at: {}>'.format(self.bot.name,self.registered_at)

class Parameter(BaseIsActiveMixin):

    __table_args__ = (
        db.CheckConstraint("param_type IN ('VARCHAR','NUMBER','DATE')", name="parameter_param_type_ck"),
    )

    parameter_key = db.Column(db.String(50), primary_key=True, nullable=False)
    parameter_desc = db.Column(db.String(200), nullable=False)
    param_type = db.Column(db.String(20), nullable=False, default = 'VARCHAR')
    varchar_value = db.Column(db.String(3000), nullable=True, default = 'VARCHAR')	
    number_value = db.Column(db.Float)
    date_value = db.Column(db.DateTime)

    def get_value(self):
        value = None
        if self.param_type == 'VARCHAR':
            value = self.varchar_value
        elif self.param_type == 'NUMBER':
            value = self.number_value
        elif self.param_type == 'DATE':
            value = self.date_value
        return value

    def __repr__(self):
        return "<Parameter parameter key: {}, param_type: {}, param value {}" \
                .format(self.parameter_key, self.param_type, self.get_value())

class Task(SearchableMixin, BaseIsActiveMixin):

    __searchable__ = ['user_id','name']

    __table_args__ = (
        db.CheckConstraint("is_active IN ('V','F')", name="task_is_active_ck"),
    )

    id = db.Column(db.Integer, primary_key=True,nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'),nullable=False)
    name = db.Column(db.String(50),nullable=False)
    taskVersion = db.relationship('TaskVersion', backref='task',lazy='dynamic')
    bot_task = db.relationship('BotTask', backref='task', lazy='dynamic')
    scheduled_job = db.relationship('BotScheduledJob', backref='task', lazy='dynamic')

    def delete(self):
        super().delete()
        jobs = BotScheduledJob.query.filter(BotScheduledJob.task_id == self.id).all()
        for job in jobs:
            job.delete()

    def get_scheduled_tasks(self, page = 1):
        return BotScheduledJob.query.filter(BotScheduledJob.task_id==self.id
                                            ,BotScheduledJob.is_active==IsActive.V) \
                .paginate(page=page, per_page=current_app.config['SCHEDULED_TASK_PER_PAGE'])

    def get_execution_details(self, page = 1):
        task_version = db.session.query(TaskVersion.task_id, TaskVersion.id)\
                        .filter(TaskVersion.task_id == self.id).subquery()
        return BotJob.query.filter(BotJob.task_version_id==task_version.c.id) \
                .order_by(BotJob.creation_date.desc()) \
                .paginate(page=page, per_page=current_app.config['TASK_EXEC_DETAILS_PER_PAGE'])

    @property
    def total_of_scheduled(self):
        return db.session.query(db.func.count(BotScheduledJob.id)) \
                                .filter(BotScheduledJob.task_id == self.id 
                                        ,BotScheduledJob.is_active == IsActive.V).scalar()
    
    def __repr__(self):
        return '<Task name {}, is_active {}, user_id {}>'.format(self.name, self.is_active, self.user_id)

class TaskVersion(SearchableMixin, BaseIsActiveMixin):

    __searchable__ = []
    __json__searchable__ = ['task_body']

    __table_args__ = (
        db.CheckConstraint("is_active IN ('V','F')", name="task_version_is_active_ck"),
    )

    id =  db.Column(db.Integer, primary_key=True, nullable=False)
    task_id = db.Column(db.Integer, db.ForeignKey('task.id'), nullable=False)
    task_body = db.Column(db.Text, nullable=False)

    def __repr__(self):
        return '<TaskVersion task_id {}, task_body {}, is_active {}>' \
                .format(self.task_id, self.task_body, self.is_active)

    def set_task_body(self, body, extension):
        task_body = get_proper_file_content(body, extension)
        self.task_body = task_body

class BotJob(BaseMixin):
    __table_args__ = (
        db.CheckConstraint("status IN ('NOT_PROCESSED','PROCESSED','PROCESSING','ERRORED')", \
                             name="bot_job_status_ck"),
    )

    id =  db.Column(db.Integer, primary_key=True, nullable=False)
    bot_id = db.Column(db.Integer,db.ForeignKey('bot.id'),nullable=False)
    task_version_id = db.Column(db.Integer, db.ForeignKey('task_version.id'), nullable=False)
    parameters = db.Column(db.String(100), nullable=True)
    status = db.Column(db.Enum(Status), nullable=False, default = Status.NOT_PROCESSED)
    execution_status = db.Column(db.String(20), nullable=True)
    job_type = db.Column(db.Enum(BotJobType), default= BotJobType.IMMEDIATE)

    def __repr__(self):
        return '<BotJob bot_id {}, task_version_id {}, parameters {}, status {}>' \
                .format(self.bot_id, self.task_version_id, self.parameters, self.status)

class BotJobFailureEvidence(BaseMixin):
    id =  db.Column(db.Integer, primary_key=True, nullable=False)
    bot_job_id = db.Column(db.Integer,db.ForeignKey('bot_job.id'),nullable=False)
    image = db.Column(db.LargeBinary,nullable=False)

    def __repr__(self):
        return '<BotJobFailureEvidence id{}, bot_job_id {}>'

class BotJobEvidence(BaseMixin):

    id = db.Column(db.Integer, primary_key=True, nullable=False)
    bot_job_id = db.Column(db.Integer, db.ForeignKey('bot_job.id'), nullable=False, index=True)
    evidence = db.Column(db.Text, nullable=False)
    extension = db.Column(db.String(10), nullable=False)

class BotTask(BaseIsActiveMixin):
    __table_args__ = (
        db.CheckConstraint("is_active IN ('V','F')", \
                             name="bot_task_is_active_ck"),
    )

    id = db.Column(db.Integer, primary_key=True, nullable=False)
    bot_id = db.Column(db.Integer, db.ForeignKey('bot.id'), nullable=False)
    task_id = db.Column(db.Integer, db.ForeignKey('task.id'), nullable=False)

    def __repr__(self):
        return '<BotTask id: {}, bot: {}, task: {}>'.format(self.id, self.bot.name, self.task.name)

# Clase a analizar
class BotScheduledJob(BaseIsActiveMixin): # Pendiente a modificar

    __table_args__ = (
        db.CheckConstraint("is_active IN ('V','F')", \
                             name="bot_scheduled_job_is_active_ck"),
        db.CheckConstraint("status IN ('NOT_PROCESSED','COMPLETED','N_REPEAT_LEFT', 'PROCESSING')", \
                             name="bot_scheduled_job_status_ck"),
    )

    id = db.Column(db.Integer, primary_key=True, nullable=False)
    bot_id = db.Column(db.Integer, db.ForeignKey('bot.id'), nullable=False)
    task_id = db.Column(db.Integer, db.ForeignKey('task.id'), nullable=False) # task_version_id
    parameters = db.Column(db.String(100))
    status = db.Column(db.Enum(ScheduledJobStatus),nullable=False, default=ScheduledJobStatus.NOT_PROCESSED)
    # Variable when a modificar
    when = db.Column(db.String(100), nullable=False)
    until = db.Column(db.DateTime, nullable=True)
    repeat = db.Column(db.Integer, nullable=True)
    queue_identifier = db.Column(db.String(100),index=True)

    def enqueue(self):
        queueName, periodicity, metadata, isPublish = self.__to_queue()
        self.queue_identifier = add_element_to_queue(queueName, periodicity, metadata, isPublish)
        
    def delete(self):
        super().delete()
        self.dequeue()

    def dequeue(self):
        if self.queue_identifier:
            remove_element_from_queue(self.__get_queue_name(),self.queue_identifier)

    def __to_queue(self):
        queue_name = self.__get_queue_name()
        periodicity = self.when[self.when.find(";") + 1:] if self.when is not None else '1' # Estas dos variables son el perdiodo de las tareas
        periodicity = periodicity if len(periodicity) > 0 else '1' # Estas dos variables son el perdiodo de las tareas
        metadata = "{" + ('"id":%s' % self.id) + "}" 
        isPublish = True

        return (queue_name, periodicity, metadata, isPublish)

    def __get_queue_name(self): # Lo que retorna es igual a la calendarización ('periodicity').
        return self.when[:self.when.find(";")] if self.when is not None else None
    
    def string_rep(self):
        return self.__to_queue()

    def __repr__(self):
        return '<BotScheduledJob id= {}, bot = {}-{}, task: {}-{}, status: {}, when: {}>'\
            .format(self.id, self.bot_id, self.bot.name if self.bot is not None else ''
                    , self.task_id, self.task.name if self.task is not None else ''
                    , self.status, self.when)