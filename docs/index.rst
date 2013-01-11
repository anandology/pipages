.. pipages documentation master file, created by
   sphinx-quickstart on Fri Dec 28 20:46:29 2012.
   You can adapt this file completely to your liking, but it should at least
   contain the root `toctree` directive.

PiPages
========

PiPages is a tool to simplify building static websites.

There are lot of engines to generate static websites. Each engine 
has its own way of building the website. PiPages provides a uniform
way to build static websites with any engine and provides an optional
web interface to trigger builds via web and on git commit.

Installation
------------

PiPages can be installed using ``pip``. ::

    $ pip install pipages

Command Line Usage
------------------

When ``pipages`` package is installed, it installs a commandline script with the same name.

It can be used to build a website from a git repository.

The following example, builds ``anandology.com`` website using ``jekyll``. ::

    $ pipages anandology.com --repo git://github.org/anandology/anandology.com.git -e jekyll 

The sources will be checked out into ``src/anandology.com`` and the build output
will be placed in ``build/anandology.com``. The ``--root`` option can be used to
specify some other directory as root.

By default pipages uses root of the repository as source directory. The ``--srcdir``
option can be used to specify a subdirectory in the repository as source directory. ::
    
    $ pipages pipages-docs --repo git://github.org/anandology/pipages.git -e sphinx --srcdir docs

For more options, see::

    $ pipages --help

Configuration
-------------

We can write a config file with list of projects and their settings 
and use it with ``pipages`` command. Pipages uses `YAML`_ format for
specifying configuration.

Here is a sample config file. ::

    # pipages config file

    # root directory to keep sources and build output. 
    root: /var/www/pipages

    # list all projects that you may want to use
    projects:
        # project name and all the settings of the project
        anandology.com:
            repo: git://github.com/anandology/anandology.com.git
            engine: jekyll

        anandology.com-pipages:
            repo: git://github.com/anandology/pipages.git
            engine: sphinx
            srcdir: docs

    # you can add your custom engine here
    engines:
        mynt: "mynt gen -f $src $dest": 

    # set this to false to allow only the engines listed in
    # the configuration
    include_default_engines: false

The ``pipages`` script accepts a config file as argument and takes all the
settings from the project with specified name.

For example, the following builds ``anandology.com`` project with settings
specified in ``/etc/pipages.yml`` file. ::

    $ pipages anandology.com -c /etc/pipages.yml

Web Interface
-------------

Pipages comes with a web application, that can be setup as a cgi script to
trigger builds via web interface. 

First create a cgi script ``pipages.cgi`` with the following code::

    #! /usr/bin/env python
    from pipages import piweb

    if __name__ == "__main__":
        # set your config file
        CONFIG_FILE = "/etc/pipages.yml"
        piweb.load_config(CONFIG_FILE)

        piweb.run()

And make sure the script is executable. ::

    $ chmod +x pipages.cgi

And configure you webserver to run this as a cgi script. The following snippet 
configures Apache to expose the cgi script at `/pipages`.

::

    ScriptAlias /pipages/ /path/to/pipages.cgi/

Once the webserver is setup, you can trigger builds via web. All we need to do
is send a ``POST`` request. For example, the following triggers build of
``anandology.com``. ::

    $ curl -X POST http://mydomain.com/pipages/anandology.com

This looks at the project settings for ``anandology.com`` project in the config
file and triggeres the build.

Triggering builds via web can potentially be dangerous. It can triggered by
anyone and prone to `DDOS attack`_.

To prevent misuse, pipages web interface allows only the projects listed in the
config file to be built. One easier way to secure your server is by picking a 
project name that is not easily guessable. Alternatively, you can add a random
suffix to the project name.

However, the best way is to `setup http authentication`_ in the webserver.  

GitHub Hook
-----------

To build the website on every github commit, setup a 
`github post-receive hook <https://help.github.com/articles/post-receive-hooks>`_ 
with the URL to post.


.. _YAML: https://en.wikipedia.org/wiki/YAML
.. _setup http authentication: http://library.linode.com/web-servers/apache/configuration/http-authentication
.. _DDOS attack: https://en.wikipedia.org/wiki/DDOS#Distributed_attack
