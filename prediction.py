'''
    The Actual prediction algorithms
'''

import numpy as np
import os, sys
import warnings
from www.app import init_settings
from datetime import datetime
from calendar import monthrange
import matplotlib.pyplot as plt

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
        self.mean_X = None
        self.std_X = None
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
        X = None
        i = 0
        for keys in self.categoryClass.keys():
            constrains["category"] = keys
            print keys
            rows = db.find(constrains)
            data = []
            for row in rows:
                data.append(row.values())
            raw = np.array(data)[:,[0,2]]
            if X == None:
                X = np.zeros((raw.shape[0],4))
            X[:,i] = raw[:,1].astype(float)
            i = i + 1
        self.mean_X = np.mean(X,0)
        self.std_X = np.std(X,0)
        X = np.apply_along_axis(lambda x,m:np.subtract(x,m),1,X,self.mean_X)
        X = np.apply_along_axis(lambda x,m:np.divide(x,m),1,X,self.std_X)
        return X

    def predictSingle(self,B,W,category):
        X = np.concatenate((self.X[-W.shape[0]+1:,self.categoryClass[category]].reshape((1,W.shape[0]-1)),np.ones((1,1))),axis = 1 )
        prediction = np.dot(self.mysigmoid(np.dot(X,W)),B)
        prediction = np.apply_along_axis(lambda x,m:np.multiply(x,m),1,prediction,self.std_X[self.categoryClass[category]])
        prediction = np.apply_along_axis(lambda x,m:np.add(x,m),1,prediction,self.mean_X[self.categoryClass[category]])
        return prediction
    
    def predictOverAll(self):
        if not np.where(sum(self.predict,0) == 0):
            print "The final result might not be complete"
        for keys in self.categoryClass.keys():
            [B,W,temp,temp1] = self.train(keys)
            self.predict[:,self.categoryClass[keys]] = self.predictSingle(B,W,keys)
        predictOverAll = np.sum(self.predict,1)
        return predictOverAll,self.predict

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
            B = np.dot(np.dot( np.linalg.inv(np.dot(H.T,H) + 0.0001 * np.eye(H.shape[1]) ) , H.T), Y)

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
        return B_best,W_best,Y_val,prediction_val_best

    def SplitData(self,category):
        raw = self.X[:,self.categoryClass[category]]
        if self.X.shape[0]  >= self.preRange * 10 :
            X = np.zeros((1,9 * self.preRange))
            Y = np.zeros((1, self.preRange))
            for i in xrange(0,self.X.shape[0] - self.preRange * 10):
                X = np.vstack((X,raw[i:i+9*self.preRange].reshape((1,9*self.preRange))))
                Y = np.vstack((Y,raw[i+9*self.preRange:i+10*self.preRange].reshape((1,self.preRange))))
        else:
            warnings.warn("More data shall be added or what? I feel like not analyzing you. :/")
            warnings.warn("The data is probably not sufficient enough for the prediction.")
            warnings.warn("The maximum we can do is to predict %f"%(self.X.shape[0]/4))
            warnings.warn("Anyway, I will produce a predictor based on the existing data")
            X = np.zeros((1,self.preRange))
            Y = np.zeros((1,self.preRange))
            ipdb.set_trace()
            for i in xrange(0,self.X.shape[0] - self.preRange * 1):
                X = np.vstack((X,raw[i:i+ 1 * self.preRange].reshape((1,self.preRange))))
                Y = np.vstack((Y,raw[i+1 * self.preRange:i+ 2 * self.preRange].reshape((1,self.preRange))))
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
            plt.plot(val_y[:,0])
            plt.plot(val_t[:,0],'r--')
            plt.ylabel('Balance')
            plt.xlabel('Time')
            plt.show()
            #plt.savefig('Validation')
        return predict

    def mysigmoid(self,x):
        return 1/(1+np.exp(-x))

    def insertFakeData(self):
        # Create Four different category data
        '''
            Grocery,Entertain,Other,Schedule
        '''
        sample = np.zeros((7,1))
        sample[:,0] = [50,40,20,20,20,20,20]
        sample = np.repeat(sample,109,axis = 1)
        sample = sample.flatten('F')[:761]
        grocery = sample + np.random.normal(5,3,365 * 2 + 31) # mu = 10 EUR, sigma = 2
        sample = np.zeros((7,1))
        sample[:,0] = [0,0,0,0,50,60,30]
        sample = np.repeat(sample,109,axis = 1)
        sample = sample.flatten('F')[:761]
        entertain = sample + np.random.normal(10,1,365 * 2 + 31)
        #ipdb.set_trace()
        other = np.zeros(grocery.shape)
        #other = np.multiply(np.random.binomial(1,0.1,365 * 2),np.random.normal(50,10,365 * 2))
        idx = np.random.permutation(grocery.shape[0])
        other = np.multiply(np.random.normal(1,0.1,365 * 2 + 31),grocery[idx,:])
        schedule = np.zeros(grocery.shape)
        noDay = []
        for i in xrange(1,13):
            [temp,month_day] = monthrange(2011,i)
            noDay.append(month_day)
        noDay = np.array(noDay)
        noDay = np.hstack((noDay,noDay))
        noDay = np.hstack((noDay,31))
        schedule_event = {
                "salary":[6000,15],
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
                        print "Successfully Inserted document %s"%(transaction_doc)

        for year in [2012]:
            for month in xrange(1,2):
                for date in xrange(1,noDay[-1]):
                    for category in Data.keys():
                        index_transaction = 730 - 1 + date
                        transaction_doc = {
                                "user_id": 4,
                                "category": category,
                                "amount": Data[category][index_transaction],
                                "date": datetime(year,month,date)
                                }
                        db_transaction.users.insert(transaction_doc,safe = True)
                        print "Successfully Inserted document %s"%(transaction_doc)

        return None

    def PredictionDataInsertion(self,prediction_month,month,year,noDay):
        try: 
            c = connect_db()
        except ConnectionFailure, e:
            sys.stderr.write("Could not connect to Server %s" %e)
            sys.exit(1)
#
        db_transaction = c['transactions']
        Data = {"Grocery":prediction_month[:,0],
                "Entertain":prediction_month[:,1],
                "Other":prediction_month[:,2],
                "Schedule":prediction_month[:,3]}
        for date in xrange(0,noDay):
            for category in Data.keys():
                transaction_doc = {
                        "user_id": "Prediction",
                        "category": category,
                        "amount": Data[category][date],
                        "date": datetime(year,month,date + 1)
                        }
                db_transaction.users.insert(transaction_doc)
                print "Successfully Inserted document: %s"% transaction_doc
        return None


    def forcast(self,Goal,day = None, month = None,year = None, produce_daily_allowance = 0):
        '''
        # Get the current Date
        # Predict the future remaining Date
        # Compute the gaol setting amount versus time
        # For time until present
        #   Compute the present daily allownace --> fork it to the panels
        #   Compute the summation of all the new daily allowance I got
        # 
        '''
        if day is None:
            day = datetime.now().day
        if month is None:
            month = datetime.now().month
        if year is None:
            year = 2012
        self.preRange = day
        [prediction, prediction_detail]= self.predictOverAll() # Fix this function --> Include the single predictions
    #    self.PredictionDataInsertion(prediction_detail,month,year,day)
        if produce_daily_allowance:
            if howManyDay == 0:
                howManyDay = Total - 1
            Goal_diff = prediction[howManyDay] - Goal
            print prediction[howManyDay]
            daily_allowance = np.zeros((HowManyDay,1))
            actual_transactions = self.acquireData(start = datetime(year,month,1),end = datetime(year,month,day))
            actual_transactions = np.apply_along_axis(lambda x,m:np.multiply(x,m),1,actual_transactions,self.std_X)
            actual_transactions = np.apply_along_axis(lambda x,m:np.add(x,m),1,actual_transactions,self.mean_X)
            self.daily_allowance = np.sum(actual_transactions,1) - prediction[actual_transactions.shape[0]]
            self.GoalGather = sum( daily_allowance ) / Goal_diff
            return None
        else:
            return None

    def simpleGraph(self):
        Old = self.X[-200:,:]
        Old = np.apply_along_axis(lambda x,m:np.multiply(x,m),1,Old,self.std_X)
        Old = np.apply_along_axis(lambda x,m:np.add(x,m),1,Old,self.mean_X)
        Predict = self.predict
        #Predict = np.apply_along_axis(lambda x,m:np.multiply(x,m),1,Predict,self.std_X)
        #Predict = np.apply_along_axis(lambda x,m:np.add(x,m),1,Predict,self.mean_X)
        np.savetxt('Validation.txt',Old)
        np.savetxt('Prediction.txt',Predict)
        trans = self.actual_trans(2012,1,31)
        np.savetxt('Actual.txt',trans)

        return None
    
    def actual_trans(self,year,month,day):
        trans = self.acquireData(start = datetime(year,month,1),end = datetime(year,month,day))
        trans = np.apply_along_axis(lambda x,m:np.multiply(x,m),1,trans,self.std_X)
        trans = np.apply_along_axis(lambda x,m:np.add(x,m),1,trans,self.mean_X)

        return trans


if __name__ == "__main__":
    import numpy as np
    import ipdb 
    from scipy.io import loadmat
    T = loadmat('ts.mat')
    Data = np.random.rand(200,4)
    Data[:,0] = T['ts'][:,:200]
    noDay = []
    TestPrediction = Prediction(preRange = 31,Data = None)
    for i in xrange(1,13):
        [temp,month_day] = monthrange(2012,i)
        noDay.append(month_day)
    noDay = np.array(noDay)
    for i in xrange(1,2):
        TestPrediction.forcast(Goal = 5000,day = noDay[i-1],month = i,year = 2012, produce_daily_allowance = 0)
    TestPrediction.simpleGraph()
    TestPrediction.model('Grocery')
    #for i in xrange(1,13):
    #    print "day %f,month %f"%(noDay[i-1],i)
    #    TestPrediction = Prediction(preRange = noDay[i-1],Data = None)
    #    TestPrediction.forcast(Goal = 5000,day = noDay[i-1],month = i, year = 2012, produce_daily_allowance = 0 )
    #    del TestPrediction
    #TestPrediction.insertFakeData()
    #for keys in TestPrediction.categoryClass.keys():
    #    predict = TestPrediction.model(keys)
    #predict_all = TestPrediction.predictOverAll()
    #print GoalGather,daily_allowance
