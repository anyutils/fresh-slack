`fresh-slack` -- to keep your Slack workspace fresh!
====================================================

Like [`destalinator`](), but less prone to annoying you. `fresh-slack` is
completely free from external dependencies, 

Install
-------

There are no installation steps for `fresh-slack`. Its only dependency is Python
3.6+.

To install the development packages for `fresh-slack`, install from the
`requirements-dev.txt` file:

    pip3 install -U 'fresh-slack[dev]'

Slack App setup
---------------

OAuth app, token needs the following permissions:

- `abc`
- `123`

`fresh-slack` Configuration
---------------------------

config file is INI, looks like this:

    [fresh-slack]
    slack_name = { name of your Slack workspace }
    slack_token = { your Slack OAuth token }
    

abc.
