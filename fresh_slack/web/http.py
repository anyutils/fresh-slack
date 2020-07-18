'''
Defines stdlib HTTP functionality
'''
from fresh_slack.config import slack_url, slack_token
import fresh_slack.utils.log as log
import json
import time
from typing import Union
import urllib.error
import urllib.request
import urllib.parse


def check_http_status(res: http.client.HTTPResponse) -> None:
    if res.status != 200:
        err = f"Unable to make request to '{res.url}'; response code {res.status} {res.reason}"
        log.error(err)
        raise urllib.error.URLError(err)


def retry_api():
    '''
    Retry in case of API rate limiting
    '''
    # respond to a raw status code 429, with a Retry-After header


def http(http_method: str, endpoint: str, params: str = '') -> Union[dict, str]:
    '''
    Abstraction function for HTTP requests to Slack. Seems like a lot of work,
    and it is, but this avoids needing external HTTP dependencies for
    fresh-slack.

        :http_method: GET or POST
        :endpoint: which Slack API method to call
        :params: optional URL parameters to add to a request. Most useful for
                 pagination.
    '''
    req = urllib.request.Request(
        url = f"{slack_url}/api/{endpoint}?{params}",
        headers = {
            'Authorization': f'Bearer {slack_token}',
            'Accept': 'application/json'
        }
    )

    if http_method == 'GET':
        with urllib.request.urlopen(req) as f:
            check_http_status(f)
            res = f.read().decode('utf-8')
    
    elif http_method == 'POST':
        req.add_header('Content-type', 'application/json')
        # post_data = 
        # post_data = post_data.encode('ascii')
        # with urllib.request.urlopen(req, post_data) as f:
        #     check_http_status(f)
        #     res = f.read().decode('utf-8')

    try:
        res = json.loads(res)
    except json.JSONDecodeError:
        raise Exception(f"URL '{res.url}' did not return a valid JSON response")

    assert res['ok'], log.error("Error in call to Slack API; response not 'ok'")
    
    if has_next_page(res):
        data = urllib.parse.urlencode(res['response_metadata']['next_cursor']).encode('ascii')
        

    return res


def has_next_page(res: dict) -> bool:
    '''
    Helper for Slack API paginated responses
    '''
    if 'response_metadata' in res and res['response_metadata']['next_cursor'] != '':
        return True
    else:
        return False
