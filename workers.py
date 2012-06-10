'''
Runs map/reduce like job against mongodb.
'''

from collections import defaultdict
from prediction import connect_db
from datetime import datetime, timedelta
from pprint import pprint

def calc_sum(coll):
    result = 0.0
    if coll is None:
        result
    for item in coll:
        result += float(item)
    return result


def calc_daily_value(db, contraints = {}):
    '''Calcs user metrics for every day'''
    #get users daily transactions and sum together
    docs = db["transactions"].find(contraints, {"amount" : 1})
    coll = [float(doc["amount"]) for doc in docs]
    return calc_sum(coll)

def calc_daily_metrics(db, user_id,  starts, ends):
    
    balances = []
    incomes = []
    expenses = []
    days = (ends - starts).days
    today = starts - timedelta(hours = ends.hour, minutes = ends.minute) #to midnight
    constraints = {
        "user_id": user_id,
        "datetime": {}
    }

    for day in xrange(days):
        tomorrow = today  + timedelta(days = 1)
        constraints= {"datetime": {"$gte": today, "$lte": tomorrow}}
        balance = calc_daily_value(db, constraints)
        
        constraints["income"] = True
        income = calc_daily_value(db, constraints)

        constraints["income"]= False
        expense = calc_daily_value(db, constraints)
        db["usermetrics"].insert({
            "_id" : today.strftime("%Y-%m-%d"),
            "datetime": today, 
            "user_id" : user_id,
            "daily_balance": balance,
            "daily_income" : income,
            "daily_expense": expense
            })

        today = tomorrow



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
