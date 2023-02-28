import pandas as pd
from sklearn.linear_model import LinearRegression
from sklearn.model_selection import train_test_split
import numpy as np
import time
import urllib.request
import os
'''
Import required libraries. Firstly configure virtual environment ('python -m venv venv'), activete, using 'venv/Scripts/activate' for WIN, and
'source env/bin/activate' for Linux. After run 'pip install -r requirements.txt', after run python.exe main.py.
'''

'''
Download data from Yahoo Finance, and import it into the csv file.
unix_time is the time in unix format, we need to download the newes data from site.
urllib.request.urlretrieve(url, destination) - download process, data.csv will be downloaded frum 'url' to 'destination'
'''
unix_time = int(time.time()) 
destination = 'data.csv'
url = 'https://query1.finance.yahoo.com/v7/finance/download/BTC-USD?period1=1410912000&period2={0}&interval=1d&events=history&includeAdjustedClose=true'.format(unix_time)
urllib.request.urlretrieve(url, destination)


data = pd.read_csv('data.csv')

projection = 1 # I need prediction for one day, so here will be 1


data['prediction'] = data['Close'].shift(-projection) # Making prediction column in data.csv

X = data[['Close']] # This line  selects the 'Close' column from the DataFrame 'data' and stores it in the 'X' settings.
y = data['prediction'] # This line  selects the 'prediction' column from the DataFrame 'data' and stores it in the 'y' settings.



X = X[:-projection]
#This code removes the last 'projection' lines from 'X', because there are no 'prediction' values ​​for these rows, we cannot predict future values ​​for these rows.
y = y[:-projection]
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42) 
#This code splits the data into training and test samples in a ratio of 80:20.


'''
I'll use Linear regression to make predictions, because this is easier way, but in future i'll be able to use better types
'''
model = LinearRegression() 
model.fit(X_train, y_train) #training procedure


print('Tomorrow BTC may be', round(model.predict(data[['Close']][-projection:])[0], 2), '$') # I am adjusting the value to cents since it is the smallest unit 

path = 'data.csv' #Clear trash after program execution
os.remove(path)