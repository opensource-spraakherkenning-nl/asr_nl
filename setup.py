#! /usr/bin/env python3
# -*- coding: utf8 -*-

from __future__ import print_function

import os
from setuptools import setup


def read(fname):
    return open(os.path.join(os.path.dirname(__file__), fname), 'r', encoding='utf-8').read()

setup(
    name = "asr_nl",
    version = "0.5.3", #also adapt in asr_nl.py and codemeta.json
    author = "Emre Yilmaz, Maarten van Gompel, Louis ten Bosch",
    author_email = "",
    description = ("Automatic Speech Recognition for Dutch - Webservice"),
    license = "AGPL-3.0-only",
    keywords = "clam webservice rest nlp computational_linguistics rest",
    url = "https://github.com/opensource-spraakherkenning-nl/asr_nl",
    packages=['asr_nl'],
    long_description=read('README.md'),
    classifiers=[
        "Development Status :: 5 - Production/Stable",
        "Topic :: Internet :: WWW/HTTP :: WSGI :: Application",
        "Topic :: Text Processing :: Linguistic",
        "Programming Language :: Python :: 3"
        "Operating System :: POSIX",
        "Intended Audience :: Developers",
        "Intended Audience :: Science/Research",
        "License :: OSI Approved :: GNU General Public License v3 (GPLv3)",
    ],
    package_data = {'asr_nl':['*.sh','*.wsgi','*.yml'] },
    include_package_data=True,
    install_requires=['CLAM >= 3.1.4']
)
