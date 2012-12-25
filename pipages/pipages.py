import sys
import optparse
import tempfile

commands = {
    "jekyll": "jekyll --safe %(src)s %(dest)s",
    "mynt": "mynt gen %(src)s %(dest)s",
    "pelican": "pelican %(src)s -o %(dest)s",
}

def generate(engine, source, dest):
    #tmpdir = tempfile.mkdtemp("pipages")
    cmd = commands[engine] % dict(src=source, dest=dest)
    status = os.system(cmd)
    if status == 0:
        print "build successful", dest    
    else:
        print >> sys.stderr, "build failed"
        sys.exit(1)

def parse_options():
    p = optparse.OptionParser(usage="%prog -e [jekyll|mynt|pelican] source-dir dest-dir")
    p.add_option("-e", "--engine", choices=["jekyll", "mynt", "pelican"], help="Website generation engine to use")
    options, args = p.parse_args()
    if options.engine is None:
        p.error("Please provide an engine")
    if len(args) != 2:
        p.error("please provide souce-dir and dest-dir arguments")
    return options, args

def main():
    options, args = parse_options()
    generation(options.engine, args[0], args[1])

if __name__ == "__main__":
    main()
