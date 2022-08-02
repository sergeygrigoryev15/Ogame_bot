from typing import List

import telebot
import urllib3
from loguru import logger
from telebot import types

from Bot.Channels import TelegramChannels
from Core.Env import environ

urllib3.disable_warnings()


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


bot = telebot.TeleBot(environ('TELEGRAM_TOKEN'), parse_mode='Markdown')

telebot.logger = logger

telebot.apihelper.CUSTOM_REQUEST_SENDER = make_request

bot.set_my_commands([
    telebot.types.BotCommand("/help", "get list of commands and their description"),
    telebot.types.BotCommand("/saving_start", "start fleet saving process"),
    telebot.types.BotCommand("/saving_stop", "stop fleet saving process"),
], scope=types.BotCommandScopeDefault())


@bot.message_handler(commands=['saving_start'])
def start_saving() -> None:
    """
    Start test to save fleet if planet is under attack.
    """
    pass


@bot.message_handler(commands=['saving_stop'])
def stop_saving() -> None:
    """
    Stop saving fleet test if it is in progress.
    """
    pass


@bot.message_handler(commands=['help'])
def help_message(message: types.Message) -> None:
    """
    When get command /help, sent list of commands

    :param message: the letter to which the response is sent
    """
    command_list = bot.get_my_commands()
    messages = ['List of commands:'] + [f'/{command.command}  {command.description}' for command in command_list]
    bot.reply_to(message, '\n'.join(messages))


class TelegramBot:

    @staticmethod
    def message_me(text: str) -> types.Message:
        return bot.send_message(TelegramChannels.PERSONAL_CHANNEL.value, text)

    @staticmethod
    def send_message(text: str):
        return TelegramBot.message_me(text)

    @staticmethod
    def alert(text: str):
        return TelegramBot.message_me(text)

    @staticmethod
    def run(timeout=20, long_polling_timeout=20):
        bot.infinity_polling(**locals())


if __name__ == '__main__':
    TelegramBot.run()
