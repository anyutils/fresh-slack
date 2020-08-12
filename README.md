`fresh-slack` -- to keep your Slack workspace fresh!
====================================================

Like [`destalinator`](), but less prone to annoying you. `fresh-slack` relies
*only* on Slack's own maintained `slackclient` package, so the risk of breakage
should fall entirely on the Slack API and not other clever dependencies.

Install
-------

`fresh-slack` can be installed as any other Python package:

    pip3 install fresh-slack
    
    # Or, if cloned locally:
    pip3 install .

To install the development packages for `fresh-slack`:

    pip3 install --user 'fresh-slack[dev]'

Slack App setup
---------------

OAuth app, token needs the following permissions:

- `abc`
- `123`

`fresh-slack` Configuration
---------------------------

config file is standard INI, looks like this:

    [fresh-slack]
    slack_name = { name of your Slack workspace }
    slack_api_token = { your Slack OAuth token }
    slack_bot_token = { your Slackbot token }

