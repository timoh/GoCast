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
    return render_template("main.html")

@main.route("/home", methods = ["GET"])
def home():
    return render_template("home.html")

@main.route("/team", methods = ["GET"])
def team():
    return render_template("team.html")

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

def update_metrics(dt, values):
    '''updates metrics in usermetrics collection '''
    day_key = dt.strftime("%Y-%m-%d")
    g.db.usermetrics.update({"_id": day_key}, 
        {"$inc": {
            "daily_balance": values["balance"],
            "daily_income": values["income"],
            "daily_expense": values["expense"]}}, True)

@main.route("/transactions", methods = ["GET", "POST"])
def transactions():
    if request.method == "POST":
       
        if len(request.form) <= 0:
            return render_template("transactions.html")
        
        trns = request.form
        
        if trns.has_key("datefield"):   
            dt_string = datetime.strptime(trns["datefield"], "%m/%d/%Y")
        else: 
            dt_string = datetime.utcnow()

        print session
        if(session.has_key("user")):
            user_id = session["user"]["user_id"]
        else:
            user_id = 1

        print request.form 
        if request.form.has_key("recurring"):
            recurrence = {
                "recurring" : True,
                "freq": trns["recurrence-freq"],
                "unit" : trns["recurrence-unit"],
                "amount" : trns["recurrence-amount"] 
            }
        else:
            recurrence = {
                "recurring" : False,
                "freq": -1,
                "unit" : -1,
                "amount" : -1 
            }
        doc = {
                "datetime" : dt_string,
                "user_id" : user_id,
                "amount": float(trns["amount"]),
                "income": float(trns["amount"]) > 0,
                #"regular": trns["is_regular"],
                "currency": {
                    "symbol" : "EUR",
                    "value" : 1.0
                },
                "recurrence": recurrence,
                "category" : "cat{0}".format(random.randint(1, 10)),
                "added" :  datetime.utcnow()
            }
        add_doc("transactions", doc)

        values = {
            "balance": doc["amount"],
            "income": doc["amount"] if doc["income"] == True else 0.0,
            "outcome": doc["amount"] if doc["income"] == True else 0.0
        }
        update_metrics(doc["datetime"], values)
        
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

#login and logout functions
#TODO: clean namespaces and imports

@main.route("/login", methods = ["GET", "POST"])
def login():
    import janrain
    '''handles user login and redirecting to user home page'''
    if request.method == "GET":
        return "I'm ajaxian."

    elif request.method == "POST":
        token = request.form['token']
        user_info = janrain.authenticate(token)
        
        #does this user exists in db,ifnot then adds
        user_id = signup(user_info)
        
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
    session.pop("user", None)
    return redirect(url_for("main.index"))

def signup(user_info):
    '''adds new user into db'''
    #does this user exists in db
    user_id = None
    user = g.db.users.find_one({"identifier": user_info["identifier"]})
    #set
    #if yes return user id
    if user is None:
        user_id = add_new_user(user_info)
        user = g.db.users.find_one({"_id": user_id})

    #set global & session values
    session["user"] = {
        "is_session_active": True,
        "user_id": user["_id"],
        "name": "{0} {1}".format(user["first_name"], user["last_name"]),
        "headline" : user["headline"]
        }
    
    return user["_id"]

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
