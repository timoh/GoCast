'''
Main app
'''

import os
from flask import Flask, g
import simplejson as json
import mongokit
#import models

#BLUEPRINTS
from main.app import main


PROD_CONFIG = "./www/config_prod.json"
DEV_CONFIG = "./www/config_dev.json"
APP_NAME = "gocast"

application = Flask(__name__)
application.g = g

def init_settings():
    ''' '''
    settings = None
    if os.environ.has_key(APP_NAME) and os.environ[APP_NAME] == "production":
        data = json.load(open(PROD_CONFIG, 'r'))
        settings = data["settings"]

    else:
        data = json.load(open(DEV_CONFIG, 'r'))
        print("NB! Database runs with local settings.\n")
        settings = data["settings"]

    #filter out None values
    map(settings.pop, [key for key,val in settings.iteritems() if val is None])

    if settings:
        application.config.update(settings)

def connect_db():
    '''connects to db and inits db connection'''
    db = None
    if application.config.has_key("DATABASE"):
        dbconf = application.config["DATABASE"]
        conn = mongokit.Connection(dbconf['host'], dbconf['port'])
        db = conn[dbconf['db']]
        if dbconf.has_key('user'):
            db.authenticate(dbconf['user'], dbconf['password'])

        #models.register(conn)
    return db #, models

@application.before_request
def before_request():
    #g.db, g.models= connect_db()
    g.db = connect_db()

def teardown_request(exception):
    if hasattr(application.g, 'db'):
        g.db.connection.disconnect()

init_settings()

application.register_blueprint(main)
