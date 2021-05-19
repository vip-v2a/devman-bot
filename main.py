import os
import requests
import telegram
import logging
import time
from bot_logger import MyLogsHandler

DEVMAN_TOKEN = os.environ['DEVMAN_TOKEN']
BOT_TOKEN = os.environ['BOT_TOKEN']
CHAT_ID = os.environ['TELEGRAM_CHAT_ID']
TIMEOUT = 91
SLEEP_PERIOD = 60 * 10

API_URL = 'https://dvmn.org/api/long_polling/'
HEADERS = {
    'Authorization': DEVMAN_TOKEN
}


def main():
    bot = telegram.Bot(token=BOT_TOKEN)
    
    last_timestamp = None
    counter_connection_error = 0

    logger = logging.getLogger("bot logger")
    logger.setLevel(logging.INFO)
    logger.addHandler(MyLogsHandler(bot_token=BOT_TOKEN, chat_id=CHAT_ID))

    logger.info("Бот запущен")
    
    while True:
        try:
            response = requests.get(
                API_URL,
                headers=HEADERS,
                timeout=TIMEOUT,
                params={'timestamp': last_timestamp}
                )
            
            devman_checking = response.json()
            response_status = devman_checking['status']

            if response_status == 'timeout':
                last_timestamp = devman_checking['timestamp_to_request']

            if response_status == 'found':
                last_timestamp = devman_checking['last_attempt_timestamp']
                checking_params, *__ = devman_checking['new_attempts']

                title = checking_params['lesson_title']
                lesson_url = checking_params['lesson_url']
                checking_status_is_negative = checking_params['is_negative']

                lesson_url = f"https://dvmn.org{lesson_url}"
                
                result_text = 'Преподавателю всё понравилось, можно приступать к следующему уроку'
                if checking_status_is_negative:
                    result_text = 'К сожалению, в работе нашлись ошибки'             

                bot.send_message(
                    chat_id=CHAT_ID,
                    text=f"У Вас проверили работу '{title}'\n{lesson_url}\n\n{result_text}"
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
        except Exception as err:
            logger.exception(err)

if __name__ == '__main__':
    main()
