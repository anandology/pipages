import sys
import argparse
import os
import logging
import commands
import string

from . import _config
from .path import File

__VERSION__ = "0.1"
__AUTHOR__ = "Anand Chitipothu <anandology@gmail.com>"

class Repository:
    """Interface to work with repository.

    Supports cloning a repository or updating an existing copy.

    NOTE: Only git is suppoted as of now.
    """
    def __init__(self, repo_url, type="git", config=None):
        if config is None:
            config = _config.default_config['repos']
        self.cmd_clone = config[type]['clone']
        self.cmd_update = config[type]['update']
        self.repo_url = repo_url

    def sync(self, working_dir):
        """Synchronizes the repository to the specified working copy.

        If the specified directory is already present, it'll be updated. If 
        not, a fresh copy will be checked out.
        """
        d = working_dir
        if d.exists():
            self.update(d)
        else:
            self.clone(d)

    def clone(self, dir):
        with dir.parent().chdir():
            system(self.cmd_clone, repo_url=self.repo_url, src=dir.path)

    def update(self, dir):
        with dir.chdir():
            system(self.cmd_update, repo_url=self.repo_url, src=dir.path)

def system(cmd, **params):
    cmd = string.Template(cmd).safe_substitute(**params)
    logger.info("system %r", cmd)

    status, output = commands.getstatusoutput(cmd)
    if status == 0:
        logger.info(output)
    else:
        logger.error(output)
        logger.error("command failed with status %d", status)
        sys.exit(status)

logger = logging.getLogger("pipages")
logging.basicConfig(level=logging.INFO, format="%(asctime)s [%(name)s] [%(levelname)s] %(message)s")

def parse_args(args=None):
    description = "pipages is a tool for building static websites."
    epilog = "For additional information, see http://pipages.anandology.com/"

    p = argparse.ArgumentParser(description=description, epilog=epilog)

    p.add_argument("project", help="name of the project to build")

    p.add_argument("-c", "--config", help="path to pipages config file")
    p.add_argument("-e", "--engine", help="Website generation engine to use")
    p.add_argument("--repo", help="Repository URL to fetch the sources")
    p.add_argument("--srcdir", help="path to the directory inside the repostory containing sources")
    p.add_argument("--root", help="Root directory to keep sources and builds. (default: current directory)")

    p.add_argument("--build-root", help="Directory to keep the builds. (default: $root/build)")
    p.add_argument("--src-root", help="Directory to keep the sources. (default: $root/src)")
    return p.parse_args(args)


def get_project_vars(config, args):
    """Combines config and args and return the vars relevant for the project
    specified in the args.
    """
    root = config.get("root", "")
    if args.root:
        root = args.root
    root = File(root).abspath().normpath()

    build_root = File(args.build_root or 
                      config.get("build_root") or
                      root.join("build").path).abspath()
    src_root = File(args.src_root or 
                    config.get("src_root") or 
                    root.join("src").path).abspath()

    name = args.project
    d = config.get("projects", {}).get(name, {})
    d.setdefault("name", name)

    d['srcdir'] = args.srcdir or config.get("srcdir") or ""

    # using d['name'] because config can specify a different name
    d['src'] = src_root.join(d['name']).normpath()

    d['dest'] = build_root.join(d['name']).normpath()

    if args.repo: # or use the default from config
        d['repo'] = args.repo

    if args.engine: # or use the default from config
        d['engine'] = args.engine

    if 'engine' not in d:
        raise Exception("engine not specified")

    if 'repo' not in d:
        raise Exception("repository url not specified")

    engines = config.get("engines")
    if d['engine'] not in engines:
        raise Exception("Unknown engine: %r" % d['engine'])
    d['build_command'] = engines[d['engine']]
    return d

def build(args):
    if args.config:
        config = _config.load_config(args.config)
    else:
        config = _config.autoload_config()

    d = get_project_vars(config, args)

    d['src'].parent().makedirs()
    d['dest'].parent().makedirs()

    logger.info("syncing the repository...")
    repo = Repository(d['repo'])
    repo.sync(d['src'])

    logger.info("building...")

    # ugly to change src like this.
    # TODO: need to find different names for repo-dir and src-dir.
    d['src'] = d['src'].join(d['srcdir']).normpath()

    with d['src'].chdir():
        system(d['build_command'], **d)
    logger.info("done")


def main():
    args = parse_args()
    build(args)

if __name__ == "__main__":
    main()
