'''
Defines stdlib HTTP functionality
'''

from fresh_slack.config import slack_url, slack_token
import json
from typing import Union
import urllib.request
import urllib.parse


def http(http_method: str, endpoint: str, params: str = '') -> Union[dict, str]:
    '''
    Abstraction function for HTTP requests. Seems like a lot of work, and it is,
    but this avoids needing external HTTP dependencies for fresh-slack.

        :http_method: GET or POST
        :endpoint: which Slack API method to call
        :params: optional URL parameters to add to a request. Most useful for
                 pagination.
    '''
    req = urllib.request.Request(
        url = slack_url,
        headers = {
            'Authorization': f'Bearer {slack_token}',
            'Accept': 'application/json'
        }
    )
    return

    if http_method == 'GET':
        with urllib.request.urlopen(req) as f:
            res = f.read().decode('utf-8')
    
    elif http_method == 'POST':
        req.add_header('Content-type', 'application/json')
        post_data = 
        post_data = data.encode('ascii')
        with urllib.request.urlopen(req, data) as f:
            res = f.read().decode('utf-8')
    # end if

    try:
        res = json.loads(res)
    except json.JSONDecodeError:
        raise Exception(f"URL '{url}' did not return a valid JSON response")
    
    if has_next_page(res):
        data = urllib.parse.urlencode(res['response_metadata']['next_cursor']).encode('ascii')

    return res
# end http


def has_next_page(res: dict) -> bool:
    '''
    Helper for Slack API paginated responses
    '''
    if 'response_metadata' in res and res['response_metadata']['next_cursor'] != '':
        return True
    else:
        return False
# end has_next_page
