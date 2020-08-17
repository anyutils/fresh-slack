from slack import WebClient
from slack.errors import SlackApiError, SlackClientError
import logging
# from typing import


class Slack():
    def __init__(self,
                 slack_name: str,
                 slack_api_token: str,
                 slack_bot_token: str,
                 warn_days: int,
                 archive_days: int):
        self.slack_name = slack_name
        self.slack_api_token = slack_api_token
        self.slack_bot_token = slack_bot_token
        self.client = WebClient(token = self.slack_api_token)
        
        try:
            self.client.api_test()
        except SlackApiError as err:
            logging.error(str(err).replace('\n', ' '))
            raise err
        logging.info(f'Authenticated to {self.slack_name}!')

        self.get_channel_info()
        self.get_channels_by_key()



    def get_channel_info(self) -> None:
        self.info = self.client.conversations_list(exclude_archived = True).data
    
    def get_channels_by_key(self) -> None:
        self.channels_by_id = {x['id']: x['name'] for x in self.info['channels']}
        self.channels_by_name = {x['name']: x['id'] for x in self.info['channels']}


# # Retry from rate limiting
#   try:
#     response = send_slack_message(channel, message)
#   except SlackApiError as e:
#     if e.response["error"] == "ratelimited":
#       # The `Retry-After` header will tell you how long to wait before retrying
#       delay = int(e.response.headers['Retry-After'])
#       print(f"Rate limited. Retrying in {delay} seconds")
#       time.sleep(delay)
#       response = send_slack_message(channel, message)
#     else:
#       # other errors
#       raise e
