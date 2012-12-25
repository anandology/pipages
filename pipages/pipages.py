import sys
import optparse
import tempfile
import os
import logging
import atexit
import shutil

logger = logging.getLogger("pipages")
logging.basicConfig(level=logging.INFO, format="%(asctime)s [%(name)s] [%(levelname)s] %(message)s")

commands = {
    "jekyll": "jekyll --safe %(src)s %(dest)s",
    "mynt": "mynt gen %(src)s %(dest)s",
    "pelican": "pelican %(src)s -o %(dest)s",
}

clone_commands = {
    "git": "git clone %(src)s %(dest)s",
    "hg": "hg clone %(src)s %(dest)s"
}

def clone_repo(type, source_url, dest_dir):
    cmd = clone_commands[type] % dict(src=source_url, dest=dest_dir)

    logger.info(cmd)
    status = os.system(cmd)
    if status == 0:
        print "fetched the repo successfully to", dest_dir
    else:
        print >> sys.stderr, "failed to fetch the repository"
        sys.exit(1)

def generate(engine, source, dest):
    cmd = commands[engine] % dict(src=source, dest=dest)
    logger.info(cmd)
    status = os.system(cmd)
    if status == 0:
        print "build successful", dest    
    else:
        print >> sys.stderr, "build failed"
        sys.exit(2)

def parse_options():
    p = optparse.OptionParser(usage="%prog -e [jekyll|mynt|pelican] source-dir dest-dir")
    p.add_option("-e", "--engine", choices=["jekyll", "mynt", "pelican"], help="Website generation engine to use")
    p.add_option("--repo", choices=["git", "hg"], help="Repository type when the source is a repository")
    p.add_option("--tmpdir", help="tmp directory to store temporary folders.")
    options, args = p.parse_args()
    if options.engine is None:
        p.error("Please provide an engine")
    if len(args) != 2:
        p.error("please provide souce-dir and dest-dir arguments")
    return options, args

def remote_dir(dir):
    logger.info("deleting temporary directory %s", dir)
    shutil.rmtree(dir, ignore_errors=True)

def mkdtemp(root, suffix=""):
    dir = tempfile.mkdtemp(prefix="pipages-", suffix=suffix, dir=root)
    atexit.register(remote_dir, dir)
    return dir

def build(engine, src, dest, repo=None, tmpdir=None):
    if repo:
        tmp = mkdtemp(tmpdir)
        clone_repo(repo, src, tmp)
        src = tmp

    generate(engine, src, dest)

def main():
    options, args = parse_options()
    build(options.engine, args[0], args[1], repo=options.repo, tmpdir=options.tmpdir)

if __name__ == "__main__":
    main()
