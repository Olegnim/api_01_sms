import time
import os

import requests
from twilio.rest import Client

from dotenv import load_dotenv

load_dotenv()


ACCOUNT_SID = os.getenv('TWILIO_ACCOUNT_SID')
AUTH_TOKEN = os.getenv('TWILIO_AUTH_TOKEN')
NUMBER_TO = os.getenv('NUMBER_TO')
NUMBER_FROM = os.getenv('NUMBER_FROM')
USER_ONLINE = 1
TOKEN = os.getenv('ACCESS_TOKEN')
BASE_URL = 'https://api.vk.com/method/'
METHOD_USERS = 'users.get'


def get_status(user_id, url, method):
    UID = user_id
    VK_VER = '5.92'
    params = {
        'user_ids': UID,
        'access_token': TOKEN,
        'v': VK_VER,
        'fields': 'online',
    }
    URL = url+'{}'.format(method)
    try:
        r = requests.post(URL, timeout=5, params=params)
    except requests.exceptions.HTTPError as errh:
        print("Http Error:", errh)
    except requests.exceptions.ConnectionError as errc:
        print("Error Connecting:", errc)
    except requests.exceptions.Timeout as errt:
        print("Timeout Error:", errt)
    except requests.exceptions.RequestException as err:
        print("Что-то пошло не так", err)
    finally:
        status_vk_user = r.json()['response'][0]['online']
    return status_vk_user


def send_sms(sms_text, to_number, from_number=NUMBER_FROM):

    client = Client(ACCOUNT_SID, AUTH_TOKEN)

    message = client.messages.create(
        body=sms_text,
        from_=from_number,
        to=to_number
    )

    return message.sid


if __name__ == '__main__':
    vk_id = input('Введите id ')
    while True:
        if get_status(vk_id, BASE_URL, METHOD_USERS) == USER_ONLINE:
            send_sms(f'{vk_id} сейчас онлайн!', NUMBER_TO)
            break
        time.sleep(5)
