import json
import os
from chalicelib.services.EmailTemplates import *
from chalice import NotFoundError, BadRequestError
from chalicelib.aws_secrets_helper import (
    get_secret
)

def getTemplate(template, arguementsArr):
    try:
        smsTemplate = json.loads(get_secret())["SMS_" + template]
        for i in arguementsArr:
            print("------------------------------->")
            print(i)
            message = smsTemplate.replace("{}", i, 1)
            smsTemplate = message
            print(message)

        return message

    except Exception as e:
        print(e)
        BadRequestError(e)
    return ""

def Templates(template_id, arguementsArr):
    return getTemplate(template_id, arguementsArr)
