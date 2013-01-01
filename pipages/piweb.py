"""webapp to receive hooks.

This is exposed as cgi using pipages.cgi script in the repository.
"""

from __future__ import absolute_import
import os
import yaml
import web

from . import pipages

urls = (
    "/?.*", "build"
)
app = web.application(urls, globals())

config = None

def get_website(name):
    return config.get("websites", {}).get(name)

class build:
    def POST(self):
        i = web.input(name="", _method="GET")
        web.data()

        name = i.name
        d = get_website(name)
        if not d:
            raise web.notfound()

        kwargs = {
            "engine": d['engine'],
            "src": d['repo'],
            "dest": self.get_dest_path(name),
            "repo": "git",
            "tmpdir": self.get_tmpdir()
        }
        pipages.build(**kwargs)
        web.header("content-type", "text/plain")
        return "ok"

    def get_dest_path(self, name):
        root = config['root']
        dir = os.path.join(root, "public", name)
        if not os.path.exists(dir):
            os.makedirs(dir)
        return dir

    def get_tmpdir(self):
        root = config['root']
        dir = os.path.join(root, "tmp")
        if not os.path.exists(dir):
            os.makedirs(dir)
        return dir

def load_config(configfile):
    global config
    config = yaml.safe_load(open(configfile))
    print config

def run(configfile):
    """Runs the app after initializing the configuration.
    """
    load_config(configfile)
    app.run()

