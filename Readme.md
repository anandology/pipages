pipages
=======

GitHub pages like system for managing static websites.

It supports multiple engines for generating websites. The currently supported engines are:

* [Jekyll](http://jekyllrb.com)
* [mynt](http://mynt.mirroredwhite.com/)
* [Pelican](http://blog.getpelican.com/)

How to use
==========

To build a website:

    $ pipages -e jekyll src-dir dest-dir

GitHub Hooks
============

The distribution comes with a cgi script that can be configured to receive
GitHub post commit hooks and build the website on every change.

TODO: explain how to configure a github hook
