'''
Main view
'''

from flask import Blueprint
from flask import render_template
from flask import g, request, jsonify, session, url_for, redirect
from flask import make_response

import mjson
from bson import ObjectId

from datetime import datetime

main = Blueprint("main", __name__)

def success(msg):
    doc = {"success" : True,
            "msg": msg}
    return jsonify(doc)

def error(msg):
    doc = {"success" : False,
            "msg" : msg}
    return jsonify(doc)

def remove_redundant_keys(d, keys):
    [d.pop(key) for key in d.keys() if key not in keys]
    return d

@main.route("/", methods = ["GET"])
def index():
    print session.get("user_id")
    return render_template("main.html", is_logged = session.has_key("user_id"))

@main.route("/home", methods = ["GET"])
def home():
    return render_template("home.html", is_logged = session.has_key("user_id"))

@main.route("/balance", methods = ["GET"])
def home():
    return render_template("balance.html", is_logged = session.has_key("user_id"))

@main.route("/salary", methods = ["GET"])
def home():
    return render_template("salary.html", is_logged = session.has_key("user_id"))

@main.route("/expenses", methods = ["GET"])
def home():
    return render_template("expenses.html", is_logged = session.has_key("user_id"))

@main.route("/channel", methods = ["GET"])
def channel():
    '''
    servers channel file for FB JS sdk.
    read more: https://developers.facebook.com/docs/reference/javascript/
    '''
    cache_expire = 60 * 60 * 24 * 365
    expiration_date = datetime.utcnow() + timedelta(seconds = cache_expire)
    response = make_response(render_template("channel.html"))
    response.headers.update({
        "Pragma" : "public",
        "Cache-Control" : "max-age={0}".format(cache_expire),
        "Expires" : expiration_date.strptime("%a, %d %m %Y %H:%M:%S")
    })
    return response

@main.route("/login", methods = ["POST"])
def login():
    ''' 
    NB! request.data expects that Content-Type is not application/encoded-form-*, 
    Use application/json instead.
    '''
    user_info = mjson.loads(request.data)
    print user_info
    if 'user_id' not in session:
        user = g.db.users.User.find_one({"social.id": user_info["id"]});

        if user is None:
            #if we didnt find such user, then signup as new user.
            user = g.db.users.User()
            user.update({
                "name" : user_info["name"],
                "email" : user_info["email"],
                "social" : {
                    "link" : user_info["link"],
                    "id" : user_info["id"],
                }
            });
            user.save()
            register_action({
                "activator" : user["_id"],
                "action" : u"signup",
                "subject" : user["_id"]
            })


        session["user_id"] = str(user["_id"])

    return success("Accepted. User session initialized.")


@main.route("/logout", methods = ["GET"])
def logout():
    if 'user_id' in session:
        del session["user_id"]

    return success("User is logged out.");


def register_action(action):
    #register new actions 
    #TODO: use signals and specific singleton for that
    new_action = g.db.actions.Action()
    new_action.update(action)
    new_action.save()