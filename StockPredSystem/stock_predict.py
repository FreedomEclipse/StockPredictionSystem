import datetime
from dateutil.relativedelta import relativedelta
import numpy as np
import pandas as pd
import collections
import sklearn

import pandas_datareader.data as pdr
from sklearn.linear_model import LogisticRegression
from sklearn.discriminant_analysis import LinearDiscriminantAnalysis
from sklearn.discriminant_analysis import QuadraticDiscriminantAnalysis
from sklearn.svm import SVC
from sklearn.ensemble import RandomForestRegressor
#from sknn.mlp import Regressor, Layer
from sklearn.neural_network import MLPClassifier
from sklearn.preprocessing import StandardScaler

pd.options.mode.chained_assignment = None

def retrieve_data(symbol, start, end, lags=5):


   stock_data = pdr.DataReader(symbol, "yahoo", start - datetime.timedelta(days=365), end)

   endstr = end.strftime('%Y-%m-%d')

   # Create the new lagged DataFrame
   stock_lag = pd.DataFrame(index=stock_data.index)
   today_df = pd.DataFrame(index=[end])


   stock_lag["Today"] = stock_data["Adj Close"]

   #print(stock_lag)
   #print(today_df)

   # Create the shifted lag series of prior trading period close values
   for i in range(0, lags):
       stock_data["Lag%s" % str(i + 1)] = stock_data["Adj Close"].shift(i + 1)
       today_df["Lag%s" % str(i + 1)] = stock_data.ix[-(i+1)]["Adj Close"]

   #print(today_df)
   #print("tslag")
   #print(tslag)

   # Create the returns DataFrame
   stock_returns = pd.DataFrame(index=stock_lag.index)
   stock_data["PercChange"] = stock_data["Adj Close"].pct_change() * 100.0

   # If any of the values of percentage returns equal zero, set them to
   # a small number (stops issues with QDA model in scikit-learn)
   for i, x in enumerate(stock_data["PercChange"]):
       if (abs(x) < 0.0001):
           stock_data["PercChange"][i] = 0.0001

   # Create the lagged percentage returns columns
   for i in range(0, lags):
       stock_data["Lag%s PercChange" % str(i + 1)] = stock_data["Lag%s" % str(i + 1)].pct_change() * 100.0

   for i in range(0, lags-1):
       diff = today_df["Lag%s" % str(i + 1)] - today_df["Lag%s" % str(i + 2)]
       #print(diff)
       today_df["Lag%s PercChange" % str(i + 1)] = (diff / today_df["Lag%s" % str(i + 2)]) * 100

   #print(today_df)
   #print(stock_data)

   # Create the "Direction" column (+1 or -1) indicating an up/down day
   stock_data["Direction"] = np.sign(stock_data["PercChange"])
   stock_data = stock_data[stock_data.index >= start]

   #print("tsret")
   #print(tsret)

   #print("Stock Data for " + symbol)
   #print(stock_data)

   return stock_data, today_df

def run_analysis(name, model, lag_train, dir_train, lag_test, pred):
   # Fits classification model using training data and makes a prediction.

   model.fit(lag_train, dir_train)
   pred[name] = model.predict(lag_test)

   # Run this to analyze the correctness of the models - Debugging
   #pred["%s_Correct" % name] = (1.0+pred[name]*pred["Actual"])/2.0
   #hit_rate = np.mean(pred["%s_Correct" % name])
   #print("%s: %.3f" % (name, hit_rate))

def print_full(x):
   pd.set_option('display.max_rows', len(x))
   #print(x)
   pd.reset_option('display.max_rows')

def run_predict():

    master_sdata = []
    today = datetime.datetime.today()

    stocks = collections.OrderedDict([('BP', 0), ('SWN', 0), ('GLD', 0), ('USO', 0), ('^DJI', 0), ('CVX', 0)])

    for s in stocks.keys():
        sdata, today_df = retrieve_data(s, datetime.datetime(2007,1,1), today, lags=5)

        # Create training data - can change lag if needed
        lag_train_data = sdata[["Lag1 PercChange","Lag2 PercChange","Lag3 PercChange","Lag4 PercChange"]]
        today_train_data = today_df[["Lag1 PercChange","Lag2 PercChange","Lag3 PercChange","Lag4 PercChange"]]
        dir_train_data = sdata["Direction"]

        today_train_data1 = lag_train_data.append(today_train_data)

        # Test data start - one year ago
        test_start_date = datetime.datetime.now() - relativedelta(years=1)

        lag_train_set = today_train_data1[today_train_data1.index < test_start_date]
        lag_test_set = today_train_data1[today_train_data1.index >= test_start_date]
        dir_train_set = dir_train_data[dir_train_data.index < test_start_date]
        dir_test_set = dir_train_data[dir_train_data.index >= test_start_date]

        #scaler = StandardScaler()
        #scaler.fit(lag_train_set)
        #scaler.fit(dir_train_set)
        #lag_train_set = scaler.transform(lag_train_set)
        #dir_train_set = scaler.transform(dir_train_set)
        #lag_test_set = scaler.transform(lag_test_set)

        #print("LAG_TRAIN")
        #print_full(lag_train_set)
        #print("DIR_TRAIN")
        #print_full(dir_train_set)
        #print(dir_train_set['continuous'])

        # Prediction results
        pred = pd.DataFrame(index=lag_test_set.index)
        #print("PREDPRED")
        #print(pred.index)
        pred["Actual"] = dir_test_set

        # Running machine learning analysis with the models
        models = [("SVC", SVC()), ("LR", LogisticRegression(solver='lbfgs', multi_class='multinomial')),
            ("Forest", RandomForestRegressor(n_estimators=1, n_jobs=-1)),
            ("LDA", LinearDiscriminantAnalysis()), ("QDA", QuadraticDiscriminantAnalysis()),
            ("NN", MLPClassifier(algorithm='sgd', alpha=1e-5, learning_rate='adaptive', learning_rate_init=0.0001,
            hidden_layer_sizes=(5, 8), random_state=3, max_iter=400, activation='relu')) ]



        for m in models:
           run_analysis(m[0], m[1], lag_train_set, dir_train_set, lag_test_set, pred)

        pred = pred.ix[1:]

        #print_full(pred)

        man_date = '2016-4-18'
        print("Actual for " + s + "  " + str(pred.ix[man_date]["Actual"]))
        print("Prediction SVM: " + str(pred.ix[man_date]["SVC"]))
        print("Prediction Linear Regression: " + str(pred.ix[man_date]["LR"]))
        print("Prediction Linear Discriminant Analysis: " + str(pred.ix[man_date]["LDA"]))
        print("Prediction Quad Discriminate Analysis: " + str(pred.ix[man_date]["QDA"]))
        print("Prediction Random Forest: " + str(pred.ix[man_date]["Forest"]))
        print("Prediction Neural Network: " + str(pred.ix[man_date]["NN"]))


        stocks[s] = pred.ix[-1]["NN"]

        master_sdata.append(sdata)

    return master_sdata, stocks

master, stocks = run_predict()





