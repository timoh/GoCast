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

def add_doc(collection, doc = None):
    if doc is not None:
        doc_id = g.db[collection].insert(doc)
        print "doc added."
        return g.db[collection].find({"_id": doc_id})

@main.route("/balance", methods = ["GET", "POST"])
def balance():
    if request.method == "POST":
        add_doc("testcoll",
                {
                "datetime": datetime.utcnow(),
                "type": "balance",
                "amount" : request.form['amount']
                })
        return redirect('/salary')
    else:
        return render_template("balance.html")

@main.route("/salary", methods = ["GET", "POST"])
def salary():
    if request.method == "POST":
        add_doc("testcoll",
            {"datetime": datetime.utcnow(),
            "type":  "salary"
            }.update(request.form))
        return redirect('/transactions')

    return render_template("salary.html")

@main.route("/transactions", methods = ["GET", "POST"])
def transactions():
    if request.method == "POST":
       
        if len(request.form) <= 0:
            return render_template("transactions.html")

        trns = {}
        trns.update(request.form)
        
        if trns.has_key("datefield"):
            dt_string = datetime.utcnow()
            dt_string = datetime.strptime(trns["datefield"].pop(), "%d/%m/%Y")
        else: 
            dt_string = datetime.utcnow()

        add_doc("transactions", 
            {
                "datetime" : dt_string,
                "user_id" : 1,
                "amount": float(trns.get("amount", 0.0)),
                "income": (trns.get("amount", 0.0)  >= 0.0),
                "regular": trns.get("is_regular", False),
                "currency": {
                    "symbol" : "EUR",
                    "value" : 1.0
                },
                "category" : {"test" : True},
                "added" :  datetime.utcnow()
            })
        return redirect('/home')

    return render_template("transactions.html")

@main.route("/data/demo", methods = ["GET"])
def data_demo():
    import random
    import time
    arr = {
        "time": int(time.time() * 1000), 
        "val":  random.randint(1, 20)}
    return jsonify(arr)


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
