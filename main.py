import os
import requests
import telegram
import time
from bot_logger import logger

TOKEN_DEVMAN = os.environ['TOKEN_DEVMAN']
TOKEN_BOT = os.environ['TOKEN_BOT']
CHAT_ID = os.environ['CHAT_ID_TELEGRAM']
TIMEOUT = 91
SLEEP_PERIOD = 60 * 10

counter_connection_error = 0
last_timestamp = None
url = 'https://dvmn.org/api/long_polling/'
headers = {
    'Authorization': TOKEN_DEVMAN
}

bot = telegram.Bot(token=TOKEN_BOT)

while True:
    try:
        if not last_timestamp:
            response = requests.get(
                url,
                headers=headers,
                timeout=TIMEOUT
                )
        else:
            response = requests.get(
                url,
                headers=headers,
                timeout=TIMEOUT,
                params={'timestamp': last_timestamp}
                )

        data = response.json()
        current_status = data['status']

        if current_status == 'timeout':
            last_timestamp = data['timestamp_to_request']

        if current_status == 'found':
            title = data['new_attempts'][0]['lesson_title']
            lesson_url = 'https://dvmn.org' + data['new_attempts'][0]['lesson_url']
            last_timestamp = data['last_attempt_timestamp']
            text_result = 'К сожалению, в работе нашлись ошибки'

            if not data['new_attempts'][0]['is_negative']:
                text_result = 'Преподавателю всё понравилось, можно приступать к следующему уроку'
            bot.send_message(
                chat_id=CHAT_ID,
                text=f"У Вас проверили работу '{title}'\n{lesson_url}\n\n{text_result}"
                )
        print(data)
    except requests.exceptions.ReadTimeout:
        logger.debug('нет ответа')
    except requests.exceptions.ConnectionError:
        # В случае многократных неудачных попыток установить соединение
        # с сервером скрипт замедлит свою работу — возьмёт небольшую паузу.
        counter_connection_error += 1
        if counter_connection_error > 2:
            logger.info('Несколько неудачных подключений подряд. Ждем 10 минут')
            time.sleep(SLEEP_PERIOD)
            counter_connection_error = 0
