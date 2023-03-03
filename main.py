import pandas as pd
from sklearn.linear_model import LinearRegression
from sklearn.model_selection import train_test_split
import numpy as np
import time
import urllib.request
import os
import sqlite3
from sqlite3 import Error
'''
Приветствую, Павел! Это послание Вам. Спешу сообщить, что я выбрал СКЛайт, поскольку проект простой, и не испытывает нагрузки, так что я считаю
самым нормальным способом по соотношению время/польза. Использовать постгрес, или подобные вещи - не проблема, просто посчитал избыточным
Так же были идеи переписать полностью модель для обучения на своих ошибках на другие методы, но признаюсь, пока что тяжело дается для освоения, 
но я думаю, что это не проблема в будущем
'''

'''
Import required libraries. Firstly configure virtual environment ('python -m venv venv'), activete, using 'venv/Scripts/activate' for WIN, and
'source env/bin/activate' for Linux. After run 'pip install -r requirements.txt', after run python.exe main.py.
'''

'''
Download data from Yahoo Finance, and import it into the csv file.
unix_time is the time in unix format, we need to download the newes data from site.
urllib.request.urlretrieve(url, destination) - download process, data.csv will be downloaded frum 'url' to 'destination'
'''

response = input('This program is only a project depicting knowledge in machine learning!There are no things that can predict the price of cryptocurrencies! In the event that you lose money due to the difference between the prediction and the truth, the responsibility is solely on you. This warning is duplicated in ReadMe.md. If you agree with the terms of use - press "Y", if not - "N": \n')
if response == 'Y' or 'y':
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

    predictions = model.predict(X_test)
    # errors to retrain the model
    errors = np.abs(predictions - y_test)
    mean_error = np.mean(errors)

    print('Mean error:', round(mean_error, 2))
    # Retrain the model with mistakes again
    new_X_train = np.concatenate((X_train, X_test[errors > mean_error]), axis=0)
    new_y_train = np.concatenate((y_train, y_test[errors > mean_error]), axis=0)

    model.fit(new_X_train, new_y_train) #training procedure on errors
    #getting the results and make variable to use in DB part of script
    next_day_price = round(model.predict(data[['Close']][-projection:])[0], 2)
    print('Tomorrow BTC may be', next_day_price, '$')

# Save the prediction to the database

    conn = sqlite3.connect('predictions.db')
    cursor = conn.cursor()

    
    #Create table with predictions, and check if the prediction table exists
    cursor.execute("CREATE TABLE IF NOT EXISTS predictions (date DATE PRIMARY KEY, price FLOAT)")


    # commit the transaction 
    conn.commit()
    # Check if there's already a prediction for the next day in the database ( antitrash, to dont have a lot of identical predictions)
    cursor.execute("SELECT * FROM predictions WHERE date=?", (str(data.iloc[-1]['Date']),))
    result = cursor.fetchone()

    if result:
        print('Prediction for the next day already exists in the database.')
    else:
    # If there's no prediction for the next day yet, add it to the database
        cursor.execute("INSERT INTO predictions (date, price) VALUES (?, ?)", (str(data.iloc[-1]['Date']), next_day_price))
        conn.commit()
        print('Prediction for the next day saved to the database.')
    # close the connection with the database to problem avoidance
    conn.close()
else:    
    print('Restart script to use it.')
