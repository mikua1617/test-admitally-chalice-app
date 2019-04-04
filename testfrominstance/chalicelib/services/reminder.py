import datetime

import pytz
import requests
from chalice import BadRequestError, ChaliceViewError, NotFoundError, Response
from chalicelib.aws_secrets_helper import get_secret
from chalicelib.models.reminder import Reminder
from chalicelib.models.reminder_status import *
from chalicelib.services.notify_meetings import notify_helper
from chalicelib.util import get_session
from sqlalchemy import func


def add_reminder(reminder):
    
    with get_session() as session:
        new_reminder = Reminder(
                            user_id = reminder['user_id'],
                            appointment_id = reminder['appointment_id'],
                            execution_time = reminder['execution_time'],
                            status = PENDING,
                            role = reminder['role'],
                            template_key = reminder['template_key'],
                            mail_data = reminder['mail_data'],
                            sms_data = reminder['sms_data']
                        )
        session.add(new_reminder)
        session.flush()

def execute_reminders():
    date = pytz.utc.localize(datetime.datetime.utcnow())    
    with get_session() as session:
        reminders = session.query(Reminder).filter(Reminder.execution_time <= date,Reminder.status==PENDING).all()
        for reminder in reminders:
            try:
                notify_helper(reminder.user_id,reminder.template_key,reminder.mail_data,reminder.role,reminder.sms_data)
                reminder.status = PROCESSED
                session.commit()
            except Exception as e:
                print(e)
                reminder.status = FAILED
                session.commit()

def decline_reminder(appointment_id):
    with get_session() as session:
        reminders = session.query(Reminder).filter_by(appointment_id=appointment_id,status=PENDING).all()
        for reminder in reminders:
            reminder.status = DECLINED
            session.commit()