from typing import List, Union
from unittest.mock import Mock

import requests
import telebot
from loguru import logger
from telebot import types, TeleBot

from Core import Env
from Core.Env import environ


def choose_option(options: List[str], row_count: int = 4) -> types.ReplyKeyboardMarkup:
    markup = types.ReplyKeyboardMarkup(row_width=row_count)
    markup.add(*[types.KeyboardButton(option) for option in options])
    return markup


def make_request(method, request_url, params, files, timeout, proxies):
    return telebot.apihelper._get_req_session() \
        .request(method,
                 request_url,
                 params=params,
                 files=files,
                 timeout=timeout,
                 proxies=proxies,
                 verify=False)


class TelegramBot:

    def __init__(self):
        requests.packages.urllib3.disable_warnings()
        self.personal_channel_id = environ('TELEGRAM_BOT_CHAT_ID')
        self.bot_token = environ('TELEGRAM_TOKEN')
        self._bot = None
        telebot.logger = logger
        telebot.apihelper.CUSTOM_REQUEST_SENDER = make_request
        self.__initialize_commands()

    @property
    def valid(self) -> bool:
        if self.bot_token in [Env.BLANK_ENV_VALUE, '']:
            logger.warning('Telegram token not set. Notifications would not be sent.')
            return False
        if self.personal_channel_id in [Env.BLANK_ENV_VALUE, '']:
            logger.warning('Telegram chat id not set. Notifications would not be sent.')
            return False
        return True

    @property
    def bot(self) -> Union['TeleBot', 'Mock']:
        if not self._bot:
            if self.valid:
                self._bot = TeleBot(self.bot_token, parse_mode='Markdown')
            else:
                self._bot = Mock()
        return self._bot

    def __initialize_commands(self) -> None:
        self.bot.set_my_commands([
            telebot.types.BotCommand('/help', 'get list of commands and their description'),
        ], scope=types.BotCommandScopeDefault())

        def __help_message(message: types.Message):
            command_list = self.bot.get_my_commands()
            messages = ['List of commands:'] + [f'/{command.command}  {command.description}' for command in
                                                command_list]
            self.bot.reply_to(message, '\n'.join(messages))

        self.bot.message_handler(commands=['help'])(__help_message)

    def message_me(self, text: str) -> None:
        self.bot.send_message(self.personal_channel_id, text)

    def run(self, timeout: int = 20, long_polling_timeout: int = 20) -> None:
        self.bot.infinity_polling(timeout=timeout, long_polling_timeout=long_polling_timeout)


if __name__ == '__main__':
    TelegramBot().run()
