import os
import requests
import telegram

token_devman = os.environ['TOKEN_DEVMAN']
token_bot = os.environ['TOKEN_BOT']
chat_id = os.environ['CHAT_ID_TELEGRAM']
last_timestamp = 0
TIMEOUT = 95

url = 'https://dvmn.org/api/long_polling/'
headers = {
    'Authorization': token_devman
}

bot = telegram.Bot(token=token_bot)

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
            last_timestamp = int(data['timestamp_to_request'])

        if current_status == 'found':
            title = data['new_attempts'][0]['lesson_title']
            lesson_url = 'https://dvmn.org' + data['new_attempts'][0]['lesson_url']
            text_result = 'К сожалению, в работе нашлись ошибки'

            if not data['new_attempts'][0]['is_negative']:
                text_result = 'Преподавателю всё понравилось, можно приступать к следующему уроку'
                
            bot.send_message(
                chat_id=chat_id,
                text=f"У Вас проверили работу '{title}'\n{lesson_url}\n\n{text_result}"
                )
        print(data)
    except requests.exceptions.ReadTimeout as error_time:
        print(error_time)
    except requests.exceptions.ConnectionError as error_connect:
        print(error_connect)
