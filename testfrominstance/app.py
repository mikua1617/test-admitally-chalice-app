import json
import os
import random

import requests
from chalice import Chalice, ChaliceViewError, CORSConfig, Rate

from chalicelib.aws_secrets_helper import get_secret
from chalicelib.services.mail import send_mail
from chalicelib.services.notify_meetings import notify_helper
from chalicelib.services.reminder import *
from chalicelib.services.sms import send_sms
from chalicelib.services.smsTemplates import Templates
from chalicelib.util import get_session

app = Chalice(app_name = 'communication')
app.debug = True


communication_host = json.loads(get_secret())["communicationHost"]

cors_config = CORSConfig(
    allow_origin = '*',
    allow_headers = ['X-Special-Header'],
    max_age = 600,
    expose_headers = ['X-Special-Header']
)

def get_token_auth_header():
    """Obtains the Access Token from the Authorization Header
    """
    auth = app.current_request.headers.get("Authorization", None)
    parts = auth.split()

    token = parts[1]
    return token

from chalicelib.auth_helper import (requires_auth, requires_auth_mentee,requires_auth_mentor)


# structure of credentials should be
# credentials = [
#                   {
#                        number: ''(empty)/'+11234567891'(number for the sms support),
#                        email_id: ''(empty)/'xyz@harvard.edu' (email id for the mail support),
#                        data: 'data for the template',
#                        template_id: "id of the tempate",
#                        from: "sender email id",
#                        message: "message to be sent via sms"
#                   }
#               ]
#
# * All fields are mandatory

@app.route('/notifyEvents', methods = ['GET', 'POST'], cors = cors_config)
def notifyEvents1():
    request = app.current_request
    if request.method == 'POST':
        sms = request.json_body['isSMS']        # This is a boolean field. True if notified via SMS
        mail = request.json_body['isMail']      # This is a boolean field. True if notified via e-mail
        body = request.json_body['credentials']
        send_mail(body)

        if(sms):
            send_sms(body)

        return("Sent successfully")
            
    return("Welcome")

@app.route('/notifyMentee', methods= ['POST'], cors = cors_config)
def notifyMentee():
    request = app.current_request
    if request.method == 'POST':
        menteeId = request.json_body['menteeId']
        template_id = request.json_body['template_id']
        data = request.json_body['data']
        sms_data = request.json_body['sms_data']

        notify_helper(menteeId, template_id, data, "mentee", sms_data)

        return ("Mentee Notified")
        
    return {'hello': 'world'}

@app.route('/notifyMentor', methods= ['POST'], cors = cors_config)
def notifyMentor():
    request = app.current_request
    if request.method == 'POST':
        mentorId = request.json_body['mentorId']
        template_id = request.json_body['template_id']
        data = request.json_body['data']
        sms_data = request.json_body['sms_data']

        notify_helper(mentorId, template_id, data, "mentor", sms_data)

        return("Mentor Notified")
        
    return {'notify Mentor'}

@app.route('/contact', methods = ['POST'], cors = cors_config)
def contact():
    request = app.current_request
    if request.method == 'POST':
        firstName = request.json_body["firstName"]
        email = request.json_body["email"]
        phoneNumber = request.json_body["phoneNumber"]
        message = request.json_body["message"]

        email_data = {
            "isSMS": False,
            "isMail": True,
            "credentials": {
                "number": " ",
                "email_id": json.loads(get_secret())["admin_email_id"],
                "cc": email,
                "data": {
                    "sender_first_name": firstName,
                    "sender_message": message
                },
                "template_id": "ADMIN_CONTACT",
                "from": json.loads(get_secret())["admin_email_id"],
                "message": " "
            }
        }

        requests.post(communication_host + "notifyEvents", json=email_data)

        print("data sent to admin successfully")

@app.route('/sendSMS', methods = ['POST'], cors = cors_config)
def run_send_sms():
    request = app.current_request
    if request.method == 'POST':
        to = request.json_body['to']
        template_id = request.json_body['template_id']
        sms_data = request.json_body['sms_data']
        print("sms_data: " + str(sms_data))
        message = Templates(template_id, sms_data)

        body = {
            "number": to,
            "message": message
        }

        return send_sms(body)

@app.route('/reminders',methods = ['POST'], cors = cors_config)
def new_reminder():
    try:
        request = app.current_request
        if request.method == 'POST':
            add_reminder(request.json_body)
	
    except Exception as e:
        print(e)
        raise ChaliceViewError(e)

@app.schedule("cron(0/15 * * * ? *)")
def run_reminder(event):
    try:
        execute_reminders()
	
    except Exception as e:
        print(e)
        raise ChaliceViewError(e)

@app.route('/declineReminders/{appointment_id}',methods = ['POST'], cors = cors_config)
def decline_reminders(appointment_id):
    try:
        decline_reminder(appointment_id)

    except Exception as e:
        print(e)
        raise ChaliceViewError(e)
