
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

api = Blueprint("api", __name__)

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

@api.route("/api/transactions", methods = ["GET", "POST"])
@api.route("/api/transactions/<string:tid>", methods = ["GET", "POST", "PUT", "DELETE"])
def index(tid = None):
    if request.method == "GET":
        contraints = {}
        data = []
        if tid is not None:
                contraints = {"_id": ObjectId(tid)}
        rows = g.db.transactions.find(contraints)
        for row in rows:
            data.append(row)
        return mjson.mongo_dumps(data)

    elif request.method == "POST":
        form = request.form
        tid = g.db.transactions.insert({
            "user_id" : form["user_id"],
            "amount": form["amount"],
            "datetime":  form["datetime"] or datetime.utcnow()})

        if tid is None:
            return error("Cant saved this data into DB: {0}".format(
                str(request.form)))
        data = g.db.transactions.find_one({"_id": tid})
        return mjson.mongo_dumps(data)
    
    elif request.method == "PUT":
        tid = g.db.update({"_id": request.form["_id"]}, 
            request.form, true)
        if tid is None:
            error("Update was unsuccessful")
        data = g.db.find_one({"_id": tid})
        return msjson.mongo_dumps(data)

    elif request.method == "DELETE":
        return error("Not implemented yet")
        doc = db.transactions.find({"_id": tid})
        if doc is None:
            return error("Deletion of `{0}` failed.")

    else:
        return error("You are too mysterious.[Wrong HTTP method.]")


#TODO: refactor
def get_predictions(user_id, starts, ends):
    data = {}

    #get all different topics
    table = g.db["transactions"]["users"]
    cats = set([doc['category'] for doc in table.find({},{"category": 1})])
    print cats
    for cat in cats:
        key = "pred_{0}".format(cat)
        print starts, ends, ":"
        print table.find({
                    "user_id": user_id,
                    "datetime": {
                        "$gte" : starts,
                        "$lte" : ends}
                    },
                    {
                    "datetime" :  1,
                    "amount": 1
                    }).count()
        
        #data[key] = [(doc["datetime"], doc["amount"]) for doc in docs]

@api.route("/api/userstats/<uid>", methods = ["GET"])
def users_stat(uid = 0):
    user = g.db["users_stat"].find_one({"$or": 
            [{"user_id": uid}, {"user_id": int(uid)}]})
    if uid == 1:
        uid = 4
    #user.update(
    print user["starts"], user["ends"]
    get_predictions(uid, user["starts"], user["ends"])
    if user is None:
        return error("User with given id `{0}` dont exist in database.".format(uid))
    else:
        return mjson.mongo_dumps(user)

@api.route("/api/usermetrics/<uid>", methods = ["GET"])
def user_metrics(uid):
    from datetime import datetime, timedelta

    ends = datetime.utcnow() 
    ends -= timedelta(hours = ends.hour, minutes = ends.minute)
    starts = ends - timedelta(days = 120)

    if request.args.has_key("starts"):
        try:
            datetime.strptime(request.args["starts"], "%Y-%m-%d")
        except:
            print "wrong date format: `{0}`".format({request.args[starts]})

    if request.args.has_key("ends"):
        try:
            datetime.strptime(request.args["ends"], "%Y-%m-%d")
        except:
            print "wrong date format: `{0}`".format({request.args[ends]})

    docs = list(g.db["usermetrics"].find({
            "$or": [{"user_id": uid}, {"user_id": int(uid)}],
            "datetime": {"$gt": starts, "$lte" : ends}}))
    
    data = {
        "user_id": uid,
        "dates":[doc["_id"] for doc in docs],
        "daily_balances":   [doc["daily_balance"] for doc in docs],
        "daily_incomes":    [doc["daily_income"] for doc in docs],
        "daily_expenses":   [doc["daily_expense"] for doc in docs],
        }

    return jsonify(data)
