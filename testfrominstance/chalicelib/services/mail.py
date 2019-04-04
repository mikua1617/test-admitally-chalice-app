import json
from chalice import NotFoundError, BadRequestError
import sendgrid
from sendgrid.helpers.mail import *
import os
import random
from chalicelib.aws_secrets_helper import (
    get_secret
)


def send_mail(body):
    sg = sendgrid.SendGridAPIClient(apikey = json.loads(get_secret())["sendgridAPIKey"])
    print(body)
    email = body['email_id']
    dynamic_data = body['data']
    if "cc" in body.keys():
        print("---------------------------------------------------->")
        print("found cc")
        data = {
            "personalizations": [
                {
                    "to": [
                        {
                            "email": email
                        }
                    ],
                    "cc": [{
                        "email": body['cc']
                    }],
                    "dynamic_template_data": dynamic_data
                }
            ],
            "template_id": json.loads(get_secret())[body['template_id']],
            "from": {
                "email":  json.loads(get_secret())["admin_email_id"]
            }
        }

    else:
        data = {
            "personalizations": [
                {
                    "to": [
                        {
                            "email": email
                        }
                    ],
                    "dynamic_template_data": dynamic_data
                }
            ],
            "template_id": json.loads(get_secret())[body['template_id']],
            "from": {
                "email":  json.loads(get_secret())["admin_email_id"]
            }
        }
    response = sg.client.mail.send.post(request_body=data)
    print(response.status_code)
    print(response.body)
    print(response.headers)