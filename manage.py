#!/usr/bin/env python

import os
import sys
import subprocess

from flask import url_for
from flask.ext.script import Manager, Server

from monkeysApp.app import create_app
from monkeysApp.models import Base
from monkeysApp.settings import DevelopmentConfig, ProductionConfig

if os.environ.get('MONKEYAPP_ENV') == 'production':
    app = create_app(__name__, ProductionConfig)
else:
    app = create_app(__name__, DevelopmentConfig)

manager = Manager(app)

@manager.command
def test():
    status = subprocess.call("py.test", shell=True)
    sys.exit(status)

@manager.command
def list_routes():
    import urllib
    output = []
    for rule in app.url_map.iter_rules():

        options = {}
        for arg in rule.arguments:
            options[arg] = "[{0}]".format(arg)

        methods = ','.join(rule.methods)
        url = url_for(rule.endpoint, **options)
        line = urllib.unquote("{:50s} {:20s} {}".format(rule.endpoint, methods, url))
        output.append(line)

    for line in sorted(output):
        print line

@manager.command
def createdb():
    Base.metadata.create_all(bind=app.engine)


manager.add_command("run", Server())

if __name__ == '__main__':
    manager.run()


