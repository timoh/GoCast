
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

    

