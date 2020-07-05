from .http import http


def get_channels() -> dict:
    channels = http('GET', 'conversations.list')


def check_history() -> dict:
    res = http('GET')