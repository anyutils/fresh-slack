import configparser
import logging
import os

# Reads values from config file into env vars, which ensures default behavior
# (env vars take precedence) but allows them to be set in the file
cfg_file = os.environ.get('SLACK_CFG_FILE', 'fresh-slack.cfg')
cfg_file_section = os.environ.get('SLACK_CFG_FILE_SECTION', 'fresh-slack')

def read_cfg_file(
        cfg_file: str = cfg_file,
        cfg_file_section: str = cfg_file_section,
        env: os._Environ = os.environ) -> dict:
    logging.info(f"fresh-slack configured using file '{cfg_file}' and file section '{cfg_file_section}'")

    fscfgfile = configparser.ConfigParser()
    fscfgfile.read(cfg_file)
    fscfg = dict(fscfgfile[cfg_file_section])
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
warn_days = int(cfg.get('SLACK_WARN_DAYS'))
archive_days = int(cfg.get('SLACK_ARCHIVE_DAYS'))

