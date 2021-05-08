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

url = 'https://dvmn.org/api/long_polling/'
headers = {
    'Authorization': TOKEN_DEVMAN
}

bot = telegram.Bot(token=TOKEN_BOT)


def main():
    last_timestamp = None
    counter_connection_error = 0

    while True:
        try:
            response = requests.get(
                url,
                headers=headers,
                timeout=TIMEOUT,
                params={'timestamp': last_timestamp}
                )

            devman_checking = response.json()
            current_status = devman_checking['status']

            if current_status == 'timeout':
                last_timestamp = devman_checking['timestamp_to_request']

            if current_status == 'found':
                title = devman_checking['new_attempts'][0]['lesson_title']
                lesson_url = f"https://dvmn.org{devman_checking['new_attempts'][0]['lesson_url']}"
                last_timestamp = devman_checking['last_attempt_timestamp']
                text_result = 'К сожалению, в работе нашлись ошибки'

                if not devman_checking['new_attempts'][0]['is_negative']:
                    text_result = 'Преподавателю всё понравилось, можно приступать к следующему уроку'
                bot.send_message(
                    chat_id=CHAT_ID,
                    text=f"У Вас проверили работу '{title}'\n{lesson_url}\n\n{text_result}"
                    )

        except requests.exceptions.ReadTimeout:
            logger.info('Нет ответа за TIMEOUT')
        except requests.exceptions.ConnectionError:
            # В случае многократных неудачных попыток установить соединение
            # с сервером скрипт замедлит свою работу — возьмёт небольшую паузу.
            counter_connection_error += 1
            if counter_connection_error > 2:
                logger.info('Несколько неудачных подключений подряд. Ждем 10 минут')
                time.sleep(SLEEP_PERIOD)
                counter_connection_error = 0

if __name__ == '__main__':
    main()