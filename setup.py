#!/usr/bin/env python
# coding: utf-8

import os
import sys
from setuptools import setup, find_packages

if sys.argv[-1] == 'publish':
    os.system('python setup.py sdist upload')
    sys.exit()

requirements = """
decorator
Flask-Script
Flask==0.10.1
Flask-WTF==0.10.2
gnureadline
ipython
itsdangerous
Jinja2
MarkupSafe
pip
psycopg2
py
pyparsing
pytest==2.6.4
pytest-flask==0.5.0
setuptools
six
SQLAlchemy==0.9.8
SQLAlchemy-Searchable
SQLAlchemy-Utils
validators
Werkzeug
wsgiref
WTForms
"""


setup(
    name='monkeysApp',
    version='0.1.0',

    description='Keep track of monkeys and his friends',
    long_description='Recruitment exercise for Fast Monkeys',
    author='Jani Nieminen',
    author_email='jpkniem@gmail.com',
    url='https://github.com/jpknie/monkeysApp',

    packages=find_packages(),
    package_dir={'monkeysApp': 'monkeysApp'},
    include_package_data=True,
    install_requires=requirements,

    license="MIT",
    zip_safe=False,
    keywords='monkey',
    classifiers=[
        'Development Status :: 2 - Pre-Alpha',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Natural Language :: English',
        "Programming Language :: Python :: 2",
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.3',
        'PyPI :: NoUpload',
    ],
#    tests_require=['pytest'],
#    cmdclass={
#        'test': PyTest
#    },
)

