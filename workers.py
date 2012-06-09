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

	counts = [(key, val) for key, val in counts.items()]
	counts = sorted(counts, key= lambda x: x[0])
	return counts
	
	

def run_tasks(user_id):
	db = connect_db()
	constraints = {"user_id": user_id}
	total = daily_total(db, constraints)
	constraints["income"] = True
	incomes = daily_total(db, constraints)
	constraints["income"] = False
	expenses = daily_total(db, constraints)
	

	db["users_stat"].insert({
		"user_id": user_id,
		"daily_balances": total,
		"daily_income": incomes,
		"daily_outcomes": expenses,
		"computed" : datetime.utcnow()
		})

def alluser_tasks():
	db= connect_db()
	user_ids = db.transactions.find({}, {"user_id":1}).distinct("user_id")
	[run_tasks(user_id) for user_id in user_ids]
