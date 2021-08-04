#!/usr/bin/env/python

from setuptools import setup, find_packages
import codecs
import os

here = os.path.abspath(os.path.dirname(__file__))

with codecs.open(os.path.join(here, "README.md"), encoding="utf-8") as fh:
    long_description = "\n" + fh.read()

VERSION = '1.0.0'
DESCRIPTION = 'AUDL API'
LONG_DESCRIPTION = 'Unofficial AUDL API'

setup(
    name="audl",
    version=VERSION,
    author="yukikongju",
    author_email="temp@gmail.com",
    description=DESCRIPTION,
    long_description_content_type="text/markdown",
    long_description=LONG_DESCRIPTION,
    packages=find_packages(),
    install_requires=['lxml', 'html5lib', 'pandas'],
    url="https://github.com/yukikongju/audl",
    include_package_data=True,
    keywords=['audl'],
    classifiers=[
        "Development Status :: 1 - Planning",
        "Programming Language :: Python :: 3",
    ]
)
