'''
Main view
'''

from flask import Blueprint
from flask import render_template
from flask import g, request, jsonify, session, url_for, redirect
from flask import make_response

import mjson
import random
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
        print "registering new user"
        user = g.db.users.find_one({"id": user_info["id"]});
        if user is None:
            #if we didnt find such user, then signup as new user.
            user_id = g.db.users.insert({
                "_id": user_info["id"],
                "name" : user_info["name"],
                "email" : user_info["email"],
                "registered": datetime.utcnow()
            });
            
        session["user_id"] = str(user_id)

    return success("Accepted. User session initialized.")


@main.route("/logout", methods = ["GET"])
def logout():
    if 'user_id' in session:
        del session["user_id"]
    #return success("User is logged out.");
    return redirect('/')
