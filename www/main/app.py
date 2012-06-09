'''
Main view
'''
from functools import wraps

from flask import Blueprint
from flask import render_template
from flask import g, request, jsonify, session, url_for, redirect, flash
from flask import make_response

import mjson
import random
from bson import ObjectId
#import rpxtokenurl
import janrain

from datetime import datetime, timedelta

main = Blueprint("main", __name__)

def success(msg):
    doc = {"success" : True,
            "msg": msg}
    return jsonify(doc)

def error(msg):
    doc = {"success" : False,
            "msg" : msg}
    return jsonify(doc)

def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if not ("user_id" in session) :
            return redirect(url_for('main.index'))
        return f(*args, **kwargs)
    return decorated_function

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

def add_doc(collection, doc = None):
    if doc is not None:
        doc_id = g.db[collection].insert(doc)
        print "doc added."
        return g.db[collection].find({"_id": doc_id})


@main.route("/balance", methods = ["GET", "POST"])
#@login_required
def balance():
    if request.method == "POST":
        add_doc("testcoll",
                {
                "datetime": datetime.utcnow(),
                "type": "balance",
                "amount" : request.form['amount']
                })
        return redirect('/transactions')
    else:
        return render_template("balance.html")

@main.route("/transactions", methods = ["GET", "POST"])
def transactions():
    if request.method == "POST":
       
        if len(request.form) <= 0:
            return render_template("transactions.html")
        
        trns = request.form
        
        if trns.has_key("datefield"):
            dt_string = datetime.utcnow()
            dt_string = datetime.strptime(trns["datefield"], "%m/%d/%Y")
        else: 
            dt_string = datetime.utcnow()

        print trns["amount"]
        add_doc("transactions", 
            {
                "datetime" : dt_string,
                "user_id" : 1,
                "amount": float(trns["amount"]),
                "income": float(trns["amount"]) > 0,
                "regular": False, #trns["is_regular"],
                "currency": {
                    "symbol" : "EUR",
                    "value" : 1.0
                },
                "category" : "cat{0}".format(random.randint(1, 10)),
                "added" :  datetime.utcnow()
            })
        return render_template("transactions.html")

    return render_template("transactions.html")

@main.route("/transactions/view", methods = ["GET"])
def trns_view():

    search_params = {}
    if len(request.args) > 0:
        qriteria = {}
        if request.args.has_key("start"):
            qriteria["$gte"] = request.args["start"]
        if request.args.has_key("end"):
            qriteria["$lt"] =  request.args["end"]
        search_params["datetime"] = qriteria

    table_view = {
        "headers" : [],
        "rows" : []
        }
    field_filter = { 
        "user_id": 0 , 
        "added": 0, 
        "currency": 0}
    docs = g.db["transactions"].find(search_params, field_filter)
    first = True
    headers = ["_id", "datetime"]
    for doc in docs:
        vals = [str(doc.pop("_id")), doc.pop("datetime").strftime("%Y-%m-%d")]
        if first == True:
            headers = doc.keys()
            table_view["headers"] = headers
            first = False

        table_view["rows"].append(doc.values())

    return mjson.mongo_dumps(table_view)

@main.route("/data/demo", methods = ["GET"])
def data_demo():
    
    import time
    arr = {
        "time": int(time.time() * 1000), 
        "val":  random.randint(1, 20)}
    return jsonify(arr)

@main.route("/channel", methods = ["GET"])
def channel():
    '''
    servers channel file for FB JS sdk.
    read more: https://developers.facebook.com/docs/reference/javascript/
    '''
    cache_expire = 60 * 60 * 24 * 365
    expiration_date = datetime.utcnow() + timedelta(seconds = cache_expire)
    response = make_response(render_template("channel.html"))
    response.headers["Pragma"] = "public"
    response.headers["Cache-Control"] = "max-age={0}".format(cache_expire)
    response.headers["Expires"] = expiration_date.strftime("%a, %d %m %Y %H:%M:%S")
  
    return response

#login and logout functions

@main.route("/login", methods = ["GET", "POST"])
def login():
    '''handles user login and redirecting to user home page'''
    if request.method == "GET":
        return "I'm ajaxian."

    elif request.method == "POST":
        token = request.form['token']
        user_info = janrain.authenticate(token)
        
        #does this user exists in db,ifnot then adds
        user_id = signup(user_info)
        session["user_id"] = user_id
        #redirect to users homepage
        print "Logged user id: ", user_id
        if user_id:
            flash("You are now logged in.")
            return redirect('/balance')
        else:
            flash("Unsuccessful login. Please try again.")
    else:
        abort(404)


@main.route("/logout", methods = ["GET"])
def logout():
    session.pop("username", None)
    return redirect(url_for("main.index"))

def signup(user_info):
    '''adds new user into db'''
    #does this user exists in db
    user_id = None
    user = g.db.users.find_one({"identifier": user_info["identifier"]})
    #if yes return user id
    if user:
        user_id = user["_id"]
    else:
        user_id = add_new_user(user_info)

    return user_id

def add_new_user(user_info):
    '''creates new user profile into db'''
    
    new_user = g.db.users.insert({
        "first_name": user_info["name"]["givenName"],
        "last_name" : user_info["name"]["familyName"],
        "headline":  u"alpha-user",
        "identifier": user_info["identifier"],
        "email":  user_info.get("verifiedEmail", "")
    })

    return new_user
