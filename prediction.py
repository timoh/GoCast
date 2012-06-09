'''
    The Actual prediction algorithms
'''

import numpy as np
import os, sys

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
        self.categoryClass = {"Grocery":0,"Entertain":1,"Other":2,"Schedule":3}
        self.preRange = preRange;
        self.predict = np.zeros((self.preRange,self.X.shape[1]))
        self.predictAll = np.zeros((self.preRange,1))

    def acquireData(self):
        return

    def predictSingle(self,B,W,category):
        X = np.concatenate((self.X[-W.shape[0]+1:,self.categoryClass[category]].reshape((1,W.shape[0]-1)),np.ones((1,1))),axis = 1 )
        prediction = np.dot(np.tanh(np.dot(X,W)),B)
        return
    
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
        neuron = [5,10,20,40,80]
        for no_neuron in neuron:
            W = np.random.rand(training_x.shape[1] + 1,no_neuron)
            X = np.concatenate((training_x,np.ones((training_x.shape[0],1))),axis=1)
            Y = training_y
            H = np.tanh(np.dot(X,W))
            B = np.dot(np.linalg.pinv(H),Y)

            X_val = np.concatenate((validation_x,np.ones((validation_x.shape[0],1))),axis = 1)
            Y_val = validation_y
            prediction_val = np.dot(np.tanh(np.dot(X_val,W)),B)
            err =  np.sum(np.sum((prediction_val - Y_val )**2))/(Y_val.shape[0] * Y_val.shape[1])
            
            if err < best_prediction:
                B_best = B
                W_best = W
        return B_best,W_best

    def SplitData(self,category):
        raw = self.X[:,self.categoryClass[category]]
        X = np.zeros((1,3 * self.preRange))
        Y = np.zeros((1, self.preRange))
        if self.X.shape[0]  >= self.preRange * 4 :
            for i in xrange(0,self.X.shape[0] - self.preRange * 4):
                X = np.vstack((X,raw[i:i+3*self.preRange].reshape((1,3*self.preRange))))
                Y = np.vstack((Y,raw[i+3*self.preRange:i+4*self.preRange].reshape((1,self.preRange))))
        else:
            print "More data shall be added or what? I feel like not analyzing you. :/"
        X = X[1:,:].copy()
        Y = Y[1:,:].copy()

        training_X = np.array([x for i,x in enumerate(X) if i % 7 != 0])
        validation_X = np.array([x for i,x in enumerate(X) if i % 7 == 0])
        training_Y = np.array([x for i,x in enumerate(Y) if i % 7 != 0])
        validation_Y = np.array([x for i,x in enumerate(Y) if i % 7 == 0])
        return training_X, training_Y, validation_X, validation_Y

    def model(self,category = "Grocery"):
        [B, W] = self.train(category)

        predict = self.predictSingle(B,W,category)
        self.predict[:,self.categoryClass[category]] = predict
        # Add the combination functionality to another function
        #self.predict = np.concatenate((predict_grocery,predict_entertain,predict_other),axis = 1)
        #self.predictOverAll = self.predictOverAll()

        return predict


if __name__ == "__main__":
    import numpy as np
    import ipdb 
    TestPrediction = Prediction(Data = np.random.rand(100,4))
    predict_grocery = TestPrediction.model(category = "Grocery")
    predict_entertain = TestPrediction.model(category = "Entertain")
    predict_other = TestPrediction.model(category = "Other")
    predict_Schedule = TestPrediction.model(category = "Schedule")
    predict_all = TestPrediction.predictOverAll()
    ipdb.set_trace()
