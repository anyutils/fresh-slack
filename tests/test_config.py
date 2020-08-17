from fresh_slack.config import read_cfg_file
import os

def test_read_cfg_file():
    # Reads from file section
    cfg = read_cfg_file(cfg_section = 'test-unit')
    for key in ['SLACK_NAME', 'SLACK_API_TOKEN', 'SLACK_BOT_TOKEN', 'SLACK_WARN_DAYS', 'SLACK_ARCHIVE_DAYS']:
        assert key in cfg

    # Defaults to taking OS env vars, but still takes ones from the cfg file
    os.environ['SLACK_NAME'] = 'abc'
    cfg = read_cfg_file(cfg_section = 'test-unit')
    assert cfg['SLACK_NAME'] == 'abc'
    assert cfg['SLACK_API_TOKEN'] == 'xoxb-lol'
