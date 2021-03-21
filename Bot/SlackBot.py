import os
import time
import re
from collections import deque
from loguru import logger

from slack import WebClient
from slack.errors import SlackApiError

from Bot.SlackChannels import SlackChannels

global slackCommands
slackCommands = deque()


class SlackBot(object):
    EXAMPLE_COMMAND = "do"
    MENTION_REGEX = "^<@(|[WU].+?)>(.*)"

    def __init__(self):
        self.client = WebClient(os.environ.get('SLACK_BOT_TOKEN'))
        self.connect()
        self.user_id = self.client.api_call("auth.test")["user_id"]

    def connect(self):
        if res := self.client.rtm_connect(with_team_state=False):
            logger.info('Bot is connected and running')
        else:
            logger.error('Connection failed. Exception traceback printed above.')
        return res

    def send_message(self, message, channel: SlackChannels = SlackChannels.OGBOT):
        try:
            logger.debug(f'Sending message "{message}" to "{channel}" channel.')
            self.client.chat_postMessage(channel=channel.value, text=message)
        except SlackApiError as e:
            logger.error(f'Error while sending message "{e.response["error"]}"')

    def parse_bot_commands(self, slack_events):
        for event in slack_events:
            if event["type"] == "message" and "subtype" not in event:
                user_id, message = self.parse_direct_mention(event["text"])
                if user_id == self.user_id:
                    return message, event["channel"]
        return None, None

    def parse_direct_mention(self, message_text):
        matches = re.search(self.MENTION_REGEX, message_text)
        return (matches.group(1), matches.group(2).strip()) if matches else (None, None)

    def handle_command(self, command, channel):
        global slackCommands
        default_response = f'Not sure what you mean. Try *{self.EXAMPLE_COMMAND}*.'
        response = None
        if command.startswith(self.EXAMPLE_COMMAND):
            instr = command[len(self.EXAMPLE_COMMAND):].strip()
            slackCommands.append(instr)
            response = f'Command "{instr}" added to queue'
        elif command == 'print queue':
            response = f'Queue = {slackCommands}'
        self.send_message(response if response else default_response, channel)


bot = SlackBot()

if __name__ == "__main__":
    RTM_READ_DELAY = 1
    slack = SlackBot()
    while True:
        # command, channel = slack.parse_bot_commands(slack.client.rtm_read())
        # if command:
        #     slack.handle_command(command, channel)
        slack.send_message('ping')
        time.sleep(RTM_READ_DELAY)
