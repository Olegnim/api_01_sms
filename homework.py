import time
import os

import requests
from twilio.rest import Client

from dotenv import load_dotenv

load_dotenv()


def get_status(user_id):
    UID = user_id
    token = os.getenv('ACCESS_TOKEN')
    URL = 'https://api.vk.com/method/users.get'
    params = {
        'user_ids': UID,
        'access_token': token,
        'v': '5.92',
        'fields': 'online',
    }
    r = requests.post(URL, params=params)
    status_vk_user = r.json()['response'][0]['online']
    return status_vk_user


def send_sms(sms_text):
    account_sid = os.getenv('TWILIO_ACCOUNT_SID')
    auth_token = os.getenv('TWILIO_AUTH_TOKEN')
    my_tel_num = os.getenv('NUMBER_TO')
    tw_tel_num = os.getenv('NUMBER_FROM')
    client = Client(account_sid, auth_token)

    message = client.messages \
        .create(
            body=sms_text,
            from_=tw_tel_num,
            to=my_tel_num
        )

    return message.sid


if __name__ == '__main__':
    vk_id = input('Введите id ')
    while True:
        if get_status(vk_id) == 1:
            send_sms(f'{vk_id} сейчас онлайн!')
            break
        time.sleep(5)
