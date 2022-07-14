"""
Send event to telegram via bot
"""
import sys

import requests
from dotenv import load_dotenv
from os import environ

load_dotenv()


def log(event):
    """
    Send message to Channel
    :param event:
    :return:
    """
    bot = environ.get('BOT_API_KEY')
    chat_ids = environ.get('BOT_USER_ID').split(',')
    for chat_id in chat_ids:
        url = f'https://api.telegram.org/bot{bot}/sendMessage?chat_id={chat_id}&text={event}'
        requests.get(url)


if __name__ == '__main__':
    log(sys.argv[1])
