'''
Main app
'''
import os
from flask import Flask, g, request, redirect, url_for

import simplejson as json
import mongokit
#import models

#BLUEPRINTS
from main.app import main
from api.app import api

PROD_CONFIG = "config_prod.json"
DEV_CONFIG = "config_dev.json"
APP_NAME = "gocast"


application = Flask(__name__)
application.g = g

def init_settings():
    ''' '''
    settings = None
    abs_path = os.path.abspath(os.path.curdir)
    
    if abs_path.find("www") <= 8:
        abs_path += "/www/"

    if os.environ.has_key(APP_NAME) and os.environ[APP_NAME] == "production":
        abs_path += PROD_CONFIG
    else:
        print("NB! Database runs with local settings.\n")
        abs_path += DEV_CONFIG

    data = json.load(open(abs_path, 'r'))    
    settings = data["settings"]

    #filter out None values
    map(settings.pop, [key for key,val in settings.iteritems() if val is None])
    return settings

def make_db_url():
    '''builds db connction string  based configuration file'''
    settings = init_settings()["DATABASE"]

    conn_string = "{0}://{1}:{2}@{3}:{4}/{5}".format(
        settings["protocol"],
        settings["user"],
        settings["password"],
        settings["host"],
        settings["port"],
        settings["db"]
        )
    return conn_string

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

settings = init_settings()
if settings is not None:
    application.config.update(settings)

application.register_blueprint(main)
application.register_blueprint(api)
