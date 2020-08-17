from fresh_slack.wrappers import Slack
import fresh_slack.config as cfg
import multiprocessing as mp
from typing import Any

def main():
    client = Slack(
        cfg.slack_name,
        cfg.slack_api_token,
        cfg.slack_bot_token,
        cfg.warn_days,
        cfg.archive_days
    )

    # with mp.Pool() as p:
    client.warn_stale_channels()
    client.archive_stale_channels()
    raise Exception

def lambda_handler(event: Any, context: Any) -> str:
    raise Exception
