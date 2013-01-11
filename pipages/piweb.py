"""webapp to receive hooks.

This is exposed as cgi using pipages.cgi script in the repository.
"""

from __future__ import absolute_import
import os
import yaml
import web

from . import pipages, _config

urls = (
    "/?.*", "build"
)
app = web.application(urls, globals())

config = None
configpath = None

def get_project(name):
    return config.get("projects", {}).get(name)

class build:
    def POST(self):
        i = web.input(name="", _method="GET")
        web.data()

        name = i.name
        d = get_project(name)
        if not d:
            raise web.notfound()

        args = pipages.parse_args([name, "-c", configpath])
        pipages.build(args)
        web.header("content-type", "text/plain")
        return "ok\n"

def load_config(configfile):
    global config, configpath
    config = _config.load_config(configfile)
    configpath = configfile
    print config

def run():
    """Runs the app.
    """
    app.run()
