'''
    The Actual prediction algorithms
'''

import numpy as np
import os, sys
import warnings
from www.app import init_settings
from datetime import datetime
from calendar import monthrange

def connect_db():
    import pymongo
    settings = init_settings()["DATABASE"] #builds nice connection string
    conn = pymongo.Connection(
        host = settings["host"], 
        port= settings["port"])
    db = conn[settings["db"]]
    if settings.has_key('user'):
        db.authenticate(settings['user'], settings['password'])
    return db

class Prediction(object):
    def __init__(self,preRange = 7,Data = None):
        # Define the data structure properly
        # Income: Dictionary --> The time and amount
        # Transactions: A predified row based data; keep the number of column to 4: Grocery | Entertain | Other | Schedule
        # Prediction Strategy:
        '''
                Prediction Strategy:

                1. The prediction class will be called when the use wants to do prediction
                2. Also, the prediction function will also be called when there is new data added. ( Optional )

                INPUT DATA FORMAT

                X --> Number of days \\times Number of Catogories ( A formulation function can be written for this)
                
                preRange --> Set how many days the user wanted to predict. 

                (optionals):
                    We should probably set up a possible confidence settings.
        '''
        self.categoryClass = {"Grocery":0,"Entertain":1,"Other":2,"Schedule":3}
        if Data is None:
            self.X = self.acquireData(start = datetime(2010,1,1),end = datetime(2011,12,31))
        else:
            self.X = Data
        self.preRange = preRange;
        self.predict = np.zeros((self.preRange,self.X.shape[1]))
        self.predictAll = np.zeros((self.preRange,1))

    def acquireData(self, start = None, end = None):
        c = connect_db()
        db = c['transactions.users']
        field_filters = {}
        constrains = {"user_id":4}
        if start is not None:
            constrains["date"] = {"$gte": start}

        if end is not None:
            constrains["date"]["$lte"] = end 
        else:
            constrains["date"]["$lte"] = datetime.utcnow()
        #constrains["user_id"] = 4

        # Matrix Generation Code
        X = np.zeros((365 * 2,4))
        i = 0
        for keys in self.categoryClass.keys():
            constrains["category"] = keys
            print keys
            rows = db.find(constrains)
            data = []
            for row in rows:
                data.append(row.values())
            raw = np.array(data)[:,[0,2]]
            X[:,i] = raw[:,1].astype(float)
            i = i + 1
        return X

    def predictSingle(self,B,W,category):
        X = np.concatenate((self.X[-W.shape[0]+1:,self.categoryClass[category]].reshape((1,W.shape[0]-1)),np.ones((1,1))),axis = 1 )
        prediction = np.dot(self.mysigmoid(np.dot(X,W)),B)
        return prediction
    
    def predictOverAll(self):
        if not np.where(sum(self.predict,0) == 0):
            print "The final result might not be complete"
        predictOverAll = np.sum(self.predict,1)
        return predictOverAll

    def train(self,category):
        training_x,training_y,validation_x,validation_y = self.SplitData(category)
        # Extreme Learning Machine 
        # Simple enough for small data, can be scaled if you want. GPU scaling.
        best_prediction = +np.Inf
        neuron = [5,8,11,14,17,20,40,60,80]
        for no_neuron in neuron:
            W = np.random.rand(training_x.shape[1] + 1,no_neuron)
            X = np.concatenate((training_x,np.ones((training_x.shape[0],1))),axis=1)
            Y = training_y
            H = self.mysigmoid(np.dot(X,W))
            B = np.dot(np.linalg.pinv(H),Y)

            X_val = np.concatenate((validation_x,np.ones((validation_x.shape[0],1))),axis = 1)
            Y_val = validation_y
            prediction_val = np.dot(self.mysigmoid(np.dot(X_val,W)),B)
            err =  np.var((prediction_val - Y_val ))/np.var(Y_val);
            if err < best_prediction:
                B_best = B
                W_best = W
                best_prediction = err
                NO = no_neuron
                Yt_best = np.dot(self.mysigmoid(np.dot(X,W)),B)
                prediction_val_best = np.dot(self.mysigmoid(np.dot(X_val,W)),B)
        print "The number of neuron is %d, and best performance is %f"%(NO,best_prediction)
        return B_best,W_best,Y_val,prediction_val_best#Y_val,prediction_val

    def SplitData(self,category):
        raw = self.X[:,self.categoryClass[category]]
        X = np.zeros((1,9 * self.preRange))
        Y = np.zeros((1, self.preRange))
        if self.X.shape[0]  >= self.preRange * 10 :
            for i in xrange(0,self.X.shape[0] - self.preRange * 10):
                X = np.vstack((X,raw[i:i+9*self.preRange].reshape((1,9*self.preRange))))
                Y = np.vstack((Y,raw[i+9*self.preRange:i+10*self.preRange].reshape((1,self.preRange))))
        else:
            warnings.warn("More data shall be added or what? I feel like not analyzing you. :/")
            warnings.warn("The data is probably not sufficient enough for the prediction.")
            warnings.warn("The maximum we can do is to predict %f"%(self.X.shape[0]/4))
            raise IndexError
        X = X[1:,:].copy()
        Y = Y[1:,:].copy()

        randomize = 0
        if randomize:
            idx = np.random.permutation(X.shape[0])
            X = X[idx].copy()
            Y = Y[idx].copy()
        split_idx = np.floor(0.8 * X.shape[0])
        training_X = X[:split_idx]
        validation_X = X[split_idx:]
        training_Y = Y[:split_idx]
        validation_Y = Y[split_idx:]
        return training_X, training_Y, validation_X, validation_Y

    def model(self,category = "Grocery"):
        [B, W,val_y,val_t] = self.train(category)

        predict = self.predictSingle(B,W,category)
        self.predict[:,self.categoryClass[category]] = predict
        visualize = 1
        if visualize:
            import matplotlib.pyplot as plt
            plt.plot(val_y)
            plt.plot(val_t,'r--')
            plt.ylabel('Something')
            plt.show()
        return predict

    def mysigmoid(self,x):
        return 1/(1+np.exp(-x))

    def insertFakeData(self):
        # Create Four different category data
        '''
            Grocery,Entertain,Other,Schedule
        '''
        grocery = np.random.normal(10,2,365 * 2) # mu = 10 EUR, sigma = 2
        entertain = np.zeros(grocery.shape)
        Raw = np.random.normal(50,20, ( 365 * 2 / 7 ) * 2)
        j = 5
        for i in xrange(Raw.shape[0]):
            if j < entertain.shape[0]:
                entertain[j:j+2] = Raw[i:i+2]
                j = j + 5;
        other = np.zeros(grocery.shape)
        Raw = 100 * np.random.poisson(1,10 * 24)
        idx = np.random.permutation(other.shape[0])
        other[idx[:100]] = Raw
        schedule = np.zeros(grocery.shape)
        noDay = []
        for i in xrange(1,13):
            [temp,month_day] = monthrange(2011,i)
            noDay.append(month_day)
        noDay = np.array(noDay)
        noDay = np.hstack((noDay,noDay))
        schedule_event = {
                "salary":[5000,15],
                "rent":[-800,6],
                "telephone":[-40,13],
                "internet":[-40,6],
                "water":[-20,6],
                "insurance":[-40,13],
                "electricity":[-40,6]}
        j = 0
        for i in schedule_event.keys():
            for offset in noDay:
                schedule[j+ schedule_event[i][1]] = schedule_event[i][0]
                j = j + offset
            j = 0

        Data = {
                "Grocery":-grocery,
                "Entertain":-entertain,
                "Other":-other,
                "Schedule":schedule
                }

        # Document Insertion

        try: 
            c = connect_db()
        except ConnectionFailure, e:
            sys.stderr.write("Could not connect to Server %s" %e)
            sys.exit(1)

        db_transaction = c['transactions']
        for year in [2010,2011]:
            for month in xrange(1,13):
                for date in xrange(1,noDay[month-1]+1):
                    #print "Date: %d,%d,%d"%(year,month,date)
                    index_transaction = (year - 2010 ) * 365 + sum(noDay[:month-1]) + date - 1
                    #print "Index: %d"%(index_transaction)
                    for category in Data.keys():
                        transaction_doc = {
                                "user_id": 4,
                                "category": category,
                                "amount": Data[category][index_transaction],
                                "date": datetime(year,month,date)
                                }
                        db_transaction.users.insert(transaction_doc,safe = True)
                        print "Successfully Inserted document: %s"% transaction_doc
        return None


    def forcast(self,day = datetime.now().day, month = datetime.now().month,year = 2012,Goal,howManyDay = 0):
        '''
        # Get the current Date
        # Predict the future remaining Date
        # Compute the gaol setting amount versus time
        # For time until present
        #   Compute the present daily allownace --> fork it to the panels
        #   Compute the summation of all the new daily allowance I got
        # 
        '''
        [temp, noDay] = monthrange(year,month)
        prediction_month = self.predictOverlAll() # Fix this function --> Include the single predictions
        if howManyDay == 0:
            howManyDay = noDay - 1
        Goal_diff = prediction_month[howManyDay] - Goal
        daily_allowance = np.zeros((noDay,1))
        actual_transactions = self.acquireData(start = datetime(year,month,1),end = datetime(year,month,day))
        daily_allowance[:actual_transactions.shape[0]] = sum(actual_transactions,1) - prediction_month[actual_transactions.shape[0]]
        GoalGather = sum( daily_allowance ) / Goal_diff
        return GoalGather,daily_allowance[:actual_transactions.shape[0]]


if __name__ == "__main__":
    import numpy as np
    import ipdb 
    from scipy.io import loadmat
    T = loadmat('ts.mat')
    Data = np.random.rand(200,4)
    Data[:,0] = T['ts'][:,:200]
    TestPrediction = Prediction(preRange = 1,Data = None)
    #TestPrediction.insertFakeData()
    predict_grocery = TestPrediction.model(category = "Grocery")
    predict_entertain = TestPrediction.model(category = "Entertain")
    predict_other = TestPrediction.model(category = "Other")
    predict_Schedule = TestPrediction.model(category = "Schedule")
    predict_all = TestPrediction.predictOverAll()
