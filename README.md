`fresh-slack` -- to keep your Slack workspace fresh!
====================================================

Like [`destalinator`](github.com/randsleadershipslack/destalinator), but less
prone to annoying you.

`fresh-slack` relies *only* on Slack's own maintained `slackclient` package, so
the risk of breakage should fall entirely on the Slack API and not other clever
dependencies. The [author of `fresh-slack`](https://github.com/ryapric) usually
tries his very best to limit dependencies in code, but the `slackclient` package
is too good (and too official) of an abstraction to not use. Plus, its next
major release (as of Sep 2020) will remove its own external dependencies, as
well.

Install
-------

`fresh-slack` can be installed as any other Python package:

    pip3 install fresh-slack
    
    # Or, if cloned locally:
    pip3 install .

To install the development packages for `fresh-slack`:

    pip3 install --user 'fresh-slack[dev]'

Note that you may need to pass in the `--user` flag to `pip3` if not running as
root.

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

