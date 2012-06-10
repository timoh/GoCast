'''
Runs map/reduce like job against mongodb.
'''

from collections import defaultdict
from prediction import connect_db
from datetime import datetime
from pprint import pprint


def daily_total(db, constraints = {}):
    ''' '''
    #get earliest date user has

    counts = defaultdict(lambda : 0)
    rows = db.transactions.find(
        constraints, 
        {"datetime": 1,
        "amount": 1}).sort("datetime")
    for row in rows:
        key = row["datetime"]
        counts[key] += float(row['amount'])

    results = {'success' : False}
    if len(counts) > 0:
        counts = [(key, val) for key, val in counts.items()]
        counts = sorted(counts, key= lambda x: x[0])
    else:
        counts = []

    return counts

def run_tasks(user_id):
    db = connect_db()
    constraints = {"user_id": user_id}
    totals = daily_total(db, constraints)
    constraints["income"] = True
    incomes = daily_total(db, constraints)
    constraints["income"] = False
    expenses = daily_total(db, constraints)
    
    dates = set()
    dates.update([item[0] for item in totals])
    dates.update([item[0] for item in incomes])
    dates.update([item[0] for item in expenses])


    if len(dates) == 0:
        print "Empty job: {0}".format(user_id)
        return False

    db["users_stat"].insert({
        "user_id": user_id,
        "starts": min(dates),
        "ends": max(dates),
        "daily_balances": totals,
        "daily_incomes": incomes,
        "daily_expenses": expenses,
        "computed" : datetime.utcnow()
        })
    return True

def alluser_tasks():
    db= connect_db()
    user_ids = db.transactions.find({}, {"user_id":1}).distinct("user_id")
    [run_tasks(user_id) for user_id in user_ids]
