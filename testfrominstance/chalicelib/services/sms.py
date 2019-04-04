import json
from chalice import NotFoundError, BadRequestError
from twilio.rest import Client
from chalicelib.aws_secrets_helper import (
	get_secret
)
import os

def send_sms(body):
    client = Client(json.loads(get_secret())["twilioAccountSid"], json.loads(get_secret())["twilio_auth_token"])
    
    message = client.messages.create(
        to = body['number'],
        from_=json.loads(get_secret())['twilio_number'],
        body = body['message']
    )
    return True