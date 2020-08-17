from slack import WebClient
from slack.errors import SlackApiError, SlackClientError
import logging
import time
from typing import Any


class Slack:
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
            # Unwrap error to fit on one log line
            logging.error(str(err).replace('\n', ' '))
            raise err
        logging.info(f'Authenticated to {self.slack_name}!')
        logging.info(f'Running initial data fetch...')

        self.get_channel_metadata()
        self.get_channels_by_key()


    def try_call(self, client_method, *args, **kwargs) -> Any:
        '''
        This is used to wrap the Slack client calls, to catch pagination,
        rate-limiting errors, and perform general API error handling.
        '''
        self.check_rate_limit(client_method, *args, **kwargs)
        response = self.check_pagination(client_method, *args, **kwargs)
        return response
    

    def check_rate_limit(self, client_method, *args, **kwargs):
        retries = 0
        while True:
            if retries >= 5:
                logging.error(f'Calling `{client_method.__name__}` retried too many times; aborting')

            # Retry from rate limiting
            try:
                response = client_method(*args, **kwargs)
                break
            except SlackApiError as err:
                retries += 1
                if err.response['error'] == 'ratelimited':
                    # The `Retry-After` header will tell you how long to wait
                    # before retrying; also buffer with an additional second
                    delay = int(err.response.headers['Retry-After']) + 1
                    logging.info(f'Rate-limited when calling `{client_method.__name__}`; retrying in {delay} seconds')
                    time.sleep(delay)
                    continue
                else:
                    raise err
        # Returned response only needed for some other method calls
        return response
    
    def check_pagination(self, client_method, data_key, *args, **kwargs):
        '''
        client_method: method callable to have *this* method call
        data_key: key in response.data that you want
        *args, **kwargs: passed to client_method
        '''
        response = self.check_rate_limit(client_method, *args, **kwargs)
        # Continue collecting any paginated results
        response_data = response.data[data_key]
        if 'response_metadata' in response.data:
            response.__iter__()
            while response.data['response_metadata']['next_cursor'] != '':
                logging.info(f'`{client_method.__name__}` returned paginated results; getting more...')
                self.check_rate_limit(response.__next__)
                response_data += response.data[data_key]
        return response_data

    def get_channel_metadata(self) -> None:
        channel_data = self.try_call(
            self.client.conversations_list,
            data_key = 'channels',
            exclude_archived = True)
        self.channel_data = channel_data
    
    def get_channels_by_key(self) -> None:
        self.channels_by_id = {x['id']: x['name'] for x in self.channel_data}
        self.channels_by_name = {x['name']: x['id'] for x in self.channel_data}


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
