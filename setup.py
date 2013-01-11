import sys
from setuptools import setup

install_requires = ["PyYAML"]

# argparse is not available as stdlib module for Python<2.7
if sys.version_info < (2, 7):
    install_requires.append("argparse")

setup(
    name="pipages",
    version="0.1.dev",
    description="GitHub pages like system for managing static websites.",
    license='BSD',
    author="Anand Chitipothu",
    author_email="anandology@gmail.com",
    url="http://github.com/anandology/pipages",
    packages=["pipages"],
    platforms=["any"],
    entry_points={
        "console_scripts": [
            "pipages=pipages.pipages:main"
        ]
    },
    install_requires=install_requires
)

