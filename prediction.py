'''
    The Actual prediction algorithms
'''

import numpy as np
import os, sys
import warnings
from www.app import init_settings

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
        if Data is None:
            self.X = self.acquireData()
        else:
            self.X = Data
        #self.categoryClass = {"Grocery":0,"Entertain":1,"Other":2,"Schedule":3}
        #self.preRange = preRange;
        #self.predict = np.zeros((self.preRange,self.X.shape[1]))
        #self.predictAll = np.zeros((self.preRange,1))

    def acquireData(self, start = None, end = None):
        from datetime import datetime
        db = connect_db()
        field_filters = {
            "currency": 0,
            "added": 0,
            "_id": 0
        }
        constrains = {}
        if start is not None:
            constrains["datetime"] = {"$gte": start}

        if end is not None:
            constrains["datetime"]["$lt"] = end 
        else:
            constrains["datetime"]["$lt"] = datetime.utcnow()


        rows = db.transactions.find(constrains, field_filters)
        data = []
        for row in rows:
            data.append(row.values())
            
        return np.array(data)

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
                Yt_best = np.dot(np.tanh(np.dot(X,W)),B)
                prediction_val_best = np.dot(np.tanh(np.dot(X_val,W)),B)
        print "The number of neuron is %d, and best performance is %f"%(NO,best_prediction)
        return B_best,W_best,Y,Yt_best#Y_val,prediction_val

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
        # Add the combination functionality to another function
        #self.predict = np.concatenate((predict_grocery,predict_entertain,predict_other),axis = 1)
        #self.predictOverAll = self.predictOverAll()
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




if __name__ == "__main__":
    import numpy as np
    import ipdb 
    from scipy.io import loadmat
    T = loadmat('ts.mat')
    Data = np.random.rand(1000,4)
    Data[:,0] = T['ts']
    TestPrediction = Prediction(preRange = 1,Data = Data)
    predict_grocery = TestPrediction.model(category = "Grocery")
    predict_entertain = TestPrediction.model(category = "Entertain")
    predict_other = TestPrediction.model(category = "Other")
    predict_Schedule = TestPrediction.model(category = "Schedule")
    predict_all = TestPrediction.predictOverAll()
