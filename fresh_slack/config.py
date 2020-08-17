import configparser
import os

# Reads values from config file into env vars, which ensures default behavior
# (env vars take precedence) but allows them to be set in the file
def read_cfg_file(
    cfg_file: str = 'fresh-slack.cfg',
    cfg_section: str = 'fresh-slack',
    env: os._Environ = os.environ
) -> dict:
    fscfgfile = configparser.ConfigParser()
    fscfgfile.read(cfg_file)
    fscfg = dict(fscfgfile[cfg_section])
    cfg = {}
    for key, value in fscfg.items():
        var = key.upper()
        if 'SLACK' not in var:
            var = f'SLACK_{var}'
        if var in env:
            cfg[var] = env[var]
        else:
            cfg[var] = value
    return cfg

cfg = read_cfg_file()

slack_name = cfg.get('SLACK_NAME')
slack_url = f"https://{cfg.get('SLACK_NAME')}.slack.com"
slack_api_token = cfg.get('SLACK_API_TOKEN')
slack_bot_token = cfg.get('SLACK_BOT_TOKEN')
warn_days = cfg.get('SLACK_WARN_DAYS')
archive_days = cfg.get('SLACK_ARCHIVE_DAYS')
