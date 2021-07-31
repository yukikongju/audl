#!/usr/bin/env/python

from setuptools import setup, find_packages
import codecs
import os

here = os.path.abspath(os.path.dirname(__file__))

with codecs.open(os.path.join(here, "README.md"), encoding="utf-8") as fh:
    long_description = "\n" + fh.read()

VERSION = '0.0.1'
DESCRIPTION = 'AUDL data downloader'
LONG_DESCRIPTION = 'A package that downloads AUDL players and team statistics'

setup(
    name="audl",
    version=VERSION,
    author="yukikongju",
    author_email="temp@gmail.com",
    description=DESCRIPTION,
    long_description_content_type="text/markdown",
    long_description=LONG_DESCRIPTION,
    packages=find_packages(),
    install_requires=['matplotlib', 'pandas'],
    #  url=
    keywords=['audl'],
    classifiers=[
        "Development Status :: 1 - Planning",
        "Programming Language :: Python :: 3",
    ]
)
