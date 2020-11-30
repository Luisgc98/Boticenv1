from flask import request
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, FileField, HiddenField, SelectField, RadioField
from wtforms.validators import DataRequired, Email, Length, ValidationError,NumberRange
from flask_babel import lazy_gettext as _l, _
import re
    
class TaskUploadForm(FlaskForm):
    bot_id = HiddenField(_l('Bot'))
    task_name = StringField(_l('Task Name'), validators=[DataRequired(), Length(max=50)])
    task_file = FileField(_l('Task file'), validators=[DataRequired()])
    submit = SubmitField(_l('Upload'))

    def validate_task_file(self, task_file):
        if task_file.data:
            if not re.match(r'^([a-zA-Z_\-\s0-9\.]+)+\.(txt|ipynb|py)$',task_file.data.filename):
                raise ValidationError(_('Please select a valid file type: %(allowed_files)s',allowed_files='.txt, .py, .ipynb'))

class EmptyDelBotForm(FlaskForm):
    bot_delete_btn = SubmitField(_l('Delete'))

class SearchForm(FlaskForm):
    q = StringField(_l('Search'), validators=[DataRequired()])

    def __init__l(self, *args, **kwargs):
        if 'formdata' not in kwargs:
            kwargs['formdata'] = request.args
        if 'csrf_enabled' not in kwargs:
            kwargs['csrf_enabled'] = False
        super(SearchForm,self).__init__l(*args, **kwargs)

month_days = [
    ('1',_l('1st')),
    ('2',_l('2nd')),
    ('3',_l('3rd')),
    ('4',_l('4th')),
    ('5',_l('5th')),
    ('6',_l('6th')),
    ('7',_l('7th')),
    ('8',_l('8th')),
    ('9',_l('9th')),
    ('10',_l('10th')),
    ('11',_l('11th')),
    ('12',_l('12th')),
    ('13',_l('13th')),
    ('14',_l('14th')),
    ('15',_l('15th')),
    ('16',_l('16th')),
    ('17',_l('17th')),
    ('18',_l('18th')),
    ('19',_l('19th')),
    ('20',_l('20th')),
    ('21',_l('21st')),
    ('22',_l('22nd')),
    ('23',_l('23rd')),
    ('24',_l('24th')),
    ('25',_l('25th')),
    ('26',_l('26th')),
    ('27',_l('27th')),
    ('28',_l('28th')),
    ('29',_l('29th')),
    ('30',_l('30th')),
    #('31',_l('31st'))
]
'''days = [
    ('1',_l('01')),
    ('2',_l('02')),
    ('3',_l('03')),
    ('4',_l('04')),
    ('5',_l('05')),
    ('6',_l('06')),
    ('7',_l('07')),
    ('8',_l('08')),
    ('9',_l('09')),
    ('10',_l('10')),
    ('11',_l('11')),
    ('12',_l('12')),
    ('13',_l('13')),
    ('14',_l('14')),
    ('15',_l('15')),
    ('16',_l('16')),
    ('17',_l('17')),
    ('18',_l('18')),
    ('19',_l('19')),
    ('20',_l('20')),
    ('21',_l('21')),
    ('22',_l('22')),
    ('23',_l('23')),
    ('24',_l('24')),
    ('25',_l('25')),
    ('26',_l('26')),
    ('27',_l('27')),
    ('28',_l('28')),
    ('29',_l('29')),
    ('30',_l('30')),
    #('31',_l('31'))
]'''
days = [
    ('1',_l('01')),
    ('2',_l('02')),
    ('3',_l('03')),
    ('4',_l('04')),
    ('5',_l('05')),
    ('6',_l('06')),
]

months = [
    ('1',_l('January')),
    ('2',_l('February')),
    ('3',_l('March')),
    ('4',_l('April')),
    ('5',_l('May')),
    ('6',_l('June')),
    ('7',_l('July')),
    ('8',_l('August')),
    ('9',_l('September')),
    ('10',_l('October')),
    ('11',_l('November')),
    ('12',_l('December'))
]

hours = [
    #('0','00'),
    ('1','01'),
    ('2','02'),
    ('3','03'),
    ('4','04'),
    ('5','05'),
    ('6','06'),
    ('7','07'),
    ('8','08'),
    ('9','09'),
    ('10','10'),
    ('11','11'),
    ('12','12'),
    ('13','13'),
    ('14','14'),
    ('15','15'),
    ('16','16'),
    ('17','17'),
    ('18','18'),
    ('19','19'),
    ('20','20'),
    ('21','21'),
    ('22','22'),
    ('23','23')
]

minutes = [
    #('0','00'),
    ('1','01'),
    ('2','02'),
    ('3','03'),
    ('4','04'),
    ('5','05'),
    ('6','06'),
    ('7','07'),
    ('8','08'),
    ('9','09'),
    ('10','10'),
    ('11','11'),
    ('12','12'),
    ('13','13'),
    ('14','14'),
    ('15','15'),
    ('16','16'),
    ('17','17'),
    ('18','18'),
    ('19','19'),
    ('20','20'),
    ('21','21'),
    ('22','22'),
    ('23','23'),
    ('24','24'),
    ('25','25'),
    ('26','26'),
    ('27','27'),
    ('28','28'),
    ('29','29'),
    ('30','30'),
    ('31','31'),
    ('32','32'),
    ('33','33'),
    ('34','34'),
    ('35','35'),
    ('36','36'),
    ('37','37'),
    ('38','38'),
    ('39','39'),
    ('40','40'),
    ('41','41'),
    ('42','42'),
    ('43','43'),
    ('44','44'),
    ('45','45'),
    ('46','46'),
    ('47','47'),
    ('48','48'),
    ('49','49'),
    ('50','50'),
    ('51','51'),
    ('52','52'),
    ('53','53'),
    ('54','54'),
    ('55','55'),
    ('56','56'),
    ('57','57'),
    ('58','58'),
    ('59','59')
]

weeks = [
    ('1','01'),
    ('2', '02'),
    ('3', '03'),
]

class ScheduleForm(FlaskForm):
    scheduled_task_id = HiddenField(_l('Task'),validators=[DataRequired()])
    bots_comma_list = HiddenField(_l('Bots'))
    periodicity = RadioField(_l('Periodicity'),
                                choices=[
                                    ('MINUTE',_l('Minute')),
                                    ('HOUR',_l('Hour')),
                                    ('DAY',_l('Day')),
                                    ('WEEK',_l('Week')),
                                    ('MONTHLY',_l('Month')),
                                    ('YEARLY',_l('Year'))
                                ], validators=[DataRequired()])
    on_day = SelectField(_l('On the'),choices=days)
    on_month = SelectField(_l('of'), choices=months)
    on_month_day = SelectField(_l('of'), choices=month_days)
    on_month_day2 = SelectField(_l('of'), choices=month_days)
    at_hour = SelectField(_l('at'), choices=hours)
    at_minutes = SelectField('', choices=minutes)
    at_week = SelectField('', choices=weeks)
    submit = SubmitField(_l('Schedule'))
    
    init_date = HiddenField(validators=[DataRequired()])
    end_date = HiddenField()
    init_time = HiddenField(validators=[DataRequired()])
    end_time = HiddenField()
    the_day = HiddenField()

    def __as_minutely(self):
        return "%s;%s:%s:%s/%s/%s" % (self.periodicity.data,self.at_minutes.data \
                                        ,self.init_date.data, self.end_date.data \
                                        ,self.init_time.data, self.end_time.data)

    def __as_hourly(self):
        return "%s;%s:%s:%s/%s/%s" % (self.periodicity.data,self.at_hour.data \
                                        ,self.init_date.data, self.end_date.data \
                                        ,self.init_time.data, self.end_time.data)
        
    def __as_daily(self):
        return "%s;%s:%s:%s/%s/%s" % (self.periodicity.data,self.on_day.data \
                                        ,self.init_date.data, self.end_date.data \
                                        ,self.init_time.data, self.end_time.data)

    '''def __as_daily(self):
        return "%s;%s:%s" % (self.periodicity.data,self.at_hour.data,self.at_minutes.data)'''
        
    def __as_weekly(self):
        return "%s;%s;%s:%s:%s/%s/%s" % (self.periodicity.data,self.the_day.data,self.at_week.data \
                                        ,self.init_date.data, self.end_date.data \
                                        ,self.init_time.data, self.end_time.data)

    def __as_monthly(self):
        return "%s;%s:%s:%s/%s/%s" % (self.periodicity.data,self.on_month_day.data \
                                        ,self.init_date.data, self.end_date.data \
                                        ,self.init_time.data, self.end_time.data)

    def __as_yearly(self):
        return "%s;%s;%s:%s:%s/%s/%s" % (self.periodicity.data,self.on_month.data, self.on_month_day2.data \
                                        ,self.init_date.data, self.end_date.data \
                                        ,self.init_time.data, self.end_time.data)

    PERIODICITY = {
        'MINUTE': __as_minutely,
        'HOUR': __as_hourly,
        'DAY': __as_daily,
        'WEEK': __as_weekly,
        'MONTHLY': __as_monthly,
        'YEARLY': __as_yearly
    }

    def as_scheduled_str(self):
        return self.PERIODICITY.get(self.periodicity.data)(self)