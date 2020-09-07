import datetime
from fresh_slack.messages import warning_message, archive_message
from slack import WebClient
from slack.errors import SlackApiError, SlackClientError
import logging
import multiprocessing
import time
from typing import Any


class Slack:
    def __init__(
            self,
            slack_name: str,
            slack_api_token: str,
            slack_bot_token: str,
            warn_days: int,
            archive_days: int):
        self.slack_name = slack_name
        self.slack_api_token = slack_api_token
        self.slack_bot_token = slack_bot_token
        
        now = datetime.datetime.today().timestamp()
        self.warn_days = warn_days
        self.warn_cutoff = now - (warn_days * 60*60*24)
        self.archive_days = archive_days
        self.archive_cutoff = now - (archive_days * 60*60*24)


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

        The naming conventions end up being a bit confusing because
        check_pagination is the also wraps `check_rate_limit`, but I'm sure I'll
        clean this up some day.
        '''
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
                    logging.error
                    raise err
        return response


    def check_pagination(self, client_method, data_key = 'ok', *args, **kwargs):
        '''
        client_method: method callable to have *this* method call

        data_key: key in response.data that you want. Defaults to 'ok', which is
        a dummy value to skip things that will never have pagination (like
        posting messages).

        *args, **kwargs: passed to client_method callable
        '''
        response = self.check_rate_limit(client_method, *args, **kwargs)
        response_data = response.data[data_key]
        # Continue collecting any paginated results
        if 'response_metadata' in response.data:
            response.__iter__()
            while response.data['response_metadata']['next_cursor'] != '':
                logging.info(f'`{client_method.__name__}` returned paginated results; getting more...')
                self.check_rate_limit(response.__next__)
                response_data += response.data[data_key]
            logging.info("Done collecting paginated results.")
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


    def get_message_history(self, channel_id) -> dict:
        # Can potentially limit response size to a single message, which at the
        # time of this writing is the latest message in the channel. However,
        # I'm not confident in being the arbiter of channel archival based on
        # such limited history, so *shrug*
        try:
            history = self.try_call(
                self.client.conversations_history,
                data_key = 'messages',
                channel = channel_id)
        except SlackApiError as err:
            if err.response['error'] == 'not_in_channel':
                logging.info(f'Bot not in channel `{self.channels_by_id[channel_id]}`; auto-joining')
                self.client.conversations_join(channel = channel_id)
                history = self.try_call(
                    self.client.conversations_history,
                    data_key = 'messages',
                    channel = channel_id)
            else:
                logging.error(str(err).replace('\n', ' '))
                raise err
        return history


    def get_latest_message(self, history: dict) -> dict:
        # If a message has a subtype, then it's not an actual message (like a
        # channel join/leave, topic set, etc.)
        msgs = [msg for msg in history if 'subtype' not in msg.keys()]
        if len(msgs) > 0:
            return msgs[0]
        else:
            # Dummy a super-old timestamp
            return {'ts': '1000000000'}


    def warn_stale_channels(self) -> None:
        for channel_id, channel_name in self.channels_by_id.items():
            logging.info(f"Checking if warning `{channel_name}` is needed; using value of {self.warn_days} days...")
            latest_msg = self.get_latest_message(self.get_message_history(channel_id), )
            if float(latest_msg['ts']) < self.warn_cutoff:
                self.try_call(
                    self.client.chat_postMessage,
                    data_key = 'ok',
                    channel = channel_id,
                    text = warning_message.format(warn_days = self.warn_days))
                logging.info(f"Warned `{channel_name}` that it's stale")
    

    def archive_stale_channels(self) -> None:
        for channel_id, channel_name in self.channels_by_id.items():
            logging.info(f"Checking if archiving `{channel_name}` is needed; using value of {self.archive_days} days...")
            latest_msg = self.get_latest_message(self.get_message_history(channel_id))
            if float(latest_msg['ts']) < self.archive_cutoff:
                if 'control code: stale-channel-warned' in latest_msg['text']:
                    self.try_call(
                        self.client.chat_postMessage,
                        channel = channel_id,
                        text = archive_message.format(archive_days = self.archive_days))
                    try:
                        self.try_call(
                            self.client.conversations_archive,
                            channel = channel_id)
                        logging.info(f"Archived stale channel `{channel_name}`")
                    except SlackApiError as err:
                        logging.error(str(err).replace('\n', ' '))
                        logging.error("Cloudn't archive channel `{channel_name}`; are you allowed to do that? (above error message should have more detail)")
