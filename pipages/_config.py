import os
import yaml
import logging

class Config(dict):
	def get_project_vars(self, name):
		d = self.get("projects")

default_config = {
	"root": "",

	"projects": {
	},

	"repos": {
		"git": {
			"clone": "git clone $repo_url $src && cd $src && git submodule init && git submodule update",
			"update": "git pull && git submodule init && git submodule update"
		},
		"hg": {
			"clone": "git clone $repo_url $src",
			"update": "hg pull && hg update"
		}
	},

	"engines": {
		"copy": "cp -r $src $dest",
	    "jekyll": "jekyll --safe $src $dest",
	    "mynt": "mynt gen -f $src $dest",
	    "pelican": "pelican -s $src/pelicanconf.py $src/content -o $dest",
	    "sphinx": "sphinx-build -b html -d $src/_build/doctrees $src $dest"
	}
}

def load_config(path):
	logger = logging.getLogger("pipages")
	logger.info("loading config from %s", path)
	return yaml.safe_load(open(path))

#AUTOLOAD_PATHS = ["pipages.yml", "/etc/pipages.yml"]
AUTOLOAD_PATHS = []

def autoload_config():
    for p in AUTOLOAD_PATHS:
        if os.path.exists(p):
            return load_config(p)
    return default_config


