from chalicelib.services.smsTemplates import Templates
from chalicelib.util import get_session
from chalicelib.services.mail import send_mail
from chalicelib.services.sms import send_sms
from chalicelib.aws_secrets_helper import get_secret


def notify_helper(user_id, template_id, data, role, sms_data):
    with get_session() as session:
        if role == "mentee":
            details = session.execute('SELECT * FROM mentee WHERE id = :id', {"id": user_id}).fetchall()
        else:
            details = session.execute('SELECT * FROM mentor WHERE id = :id', {"id": user_id}).fetchall()

        isSMS = False
        message = Templates(template_id, sms_data)
        for details in details:
            if details.phone_number != '' and details.isSMSEnabled and message != '':
                isSMS = True
        

        body = {"number": details.phone_number, 
                "email_id": details.email, 
                "message": message, 
                "data": data, 
                "template_id": template_id}

        # data = json.dumps({
        #     "isSMS": isSMS,
        #     "isMAil": True,
        #     "credentials": [
        #         {
        #             "number": details.phone_number,
        #             "email-id": details.email,
        #             "message": message
        #         }
        #     ]
        # })
        print('notify')
        print(body)
        
        send_mail(body)

        if(isSMS):
            send_sms(body)
