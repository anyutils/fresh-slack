import configparser
import os

# Defaults expected to be env vars, so use those globally
cfg = os.environ

# Reads values from config file into env vars, which ensures default behavior
# but allows them to be set in the file
def read_cfg_file(cfg_file: str = 'fresh-slack.cfg') -> None:
    fscfg = configparser.ConfigParser()
    fscfg.read(cfg_file)
    fscfg = dict(fscfg['fresh-slack'])
    for key, value in fscfg.items():
        cfg[key.upper()] = value

read_cfg_file()

slack_name = cfg.get('SLACK_NAME')
slack_url = f"https://{cfg.get('SLACK_NAME')}.slack.com"
slack_api_token = cfg.get('SLACK_API_TOKEN')
slack_bot_token = cfg.get('SLACK_BOT_TOKEN')
