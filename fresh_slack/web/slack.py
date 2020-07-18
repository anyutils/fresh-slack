from fresh_slack.web.http import http
import fresh_slack.utils.log as log
import time

now = int(time.time)


def get_channels() -> dict:
    channels = http('GET', 'conversations.list')
    return channels


def join_channel(channel_id: str) -> None:
    """
    Fix for new-type Slack apps where apps need to already be in channels to
    work.
    """
    http('POST', 'conversations.join', 'channel=channel_id')


def get_history(timestamp: int, channel_id: str) -> dict:
    '''
    :timestamp: UNIX integer timestamp
    '''
    history = http(
        'GET',
        'conversations.history',
        params = f'oldest={timestamp}&channel={channel_id}'
    )
    return history


def channel_action(channel_id) -> str:
    '''
    Returns one of 'WARN' or 'ARCHIVE'
    '''
    warn_timestamp = now - (warn_days * 86400)
    archive_timestamp = now - (archive_days * 86400)

    warnable_history = get_history(warn_timestamp)
    archivable_history = get(history)


def slack_main():
    channels = get_channels()
    for channel_id in channels:
        if channel_action(channel) == 'WARN':
            pass
        elif channel_action(channel) == 'ARCHIVE':
            pass
        else:

            raise Exception('Bad channel_action ')
