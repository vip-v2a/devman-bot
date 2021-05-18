import logging
import telegram

STRFMT = '[%(asctime)s] [%(name)s] [%(levelname)s] > %(message)s'
DATEFFMT = '%Y-%m-%d %H:%M:%S'


class MyLogsHandler(logging.Handler):
    

    def __init__(self, logging_level=logging.DEBUG, bot_token=None, chat_id=None, fmt=STRFMT, datefmt=DATEFFMT):
        super().__init__(logging_level)
        self.bot = telegram.Bot(token=bot_token)
        self.chat_id = chat_id
        formatter = logging.Formatter(fmt, datefmt)
        self.setFormatter(formatter)
        self.setLevel(logging_level)

    
    def emit(self, record):
        log_entry = self.format(record)
        self.bot.send_message(
                    chat_id=self.chat_id,
                    text=log_entry
                    )  
        