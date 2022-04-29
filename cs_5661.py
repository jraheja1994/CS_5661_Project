# -*- coding: utf-8 -*-
"""CS_5661.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1RSzYMeadWVjrEUAkyVjOQNPTaWkWg5Il
"""

# Libraries install & import

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.dates as mdates

import tensorflow as tf
from tensorflow import keras

from sklearn.preprocessing import MinMaxScaler
from sklearn.cluster import KMeans
from sklearn.metrics import accuracy_score
from sklearn.model_selection import cross_val_score, GridSearchCV
from sklearn.tree import DecisionTreeClassifier
from sklearn import metrics

from keras.models import Sequential
from keras.layers import Activation, Dense, LSTM, GRU, Bidirectional, Flatten, Dropout
from tensorflow.keras.optimizers import Adam, SGD
from keras.wrappers.scikit_learn import KerasRegressor
from keras.callbacks import ModelCheckpoint, EarlyStopping

from sklearn.metrics import mean_absolute_percentage_error, mean_squared_error
import math
from math import sqrt
from random import randint


np.random.seed(1356)
plt.style.use('ggplot')

import warnings
warnings.simplefilter(action='ignore', category=FutureWarning)

# Read data from csv
df_btc = pd.read_csv("https://raw.githubusercontent.com/jraheja1994/CS_5661_Project/main/BTC-USD.csv", index_col='Date', parse_dates=['Date'])
print(df_btc)

# Plot Bitcoin price trend

plt.figure(figsize=(8,4))
plt.rcParams['figure.dpi'] = 360
plt.plot(df_btc['Close'], linewidth=0.8)
plt.xlabel("Date", fontsize=8) 
plt.ylabel('Close (USD)', fontsize=6)
plt.gca().xaxis.set_major_formatter(mdates.DateFormatter("%m/%Y"))
plt.xticks(fontsize=8, rotation=90)
plt.yticks(fontsize=4)
plt.title("Bitcoin USD (BTC-USD)")

# Data Spliting

days_to_forcast = 30
df_train = df_btc['Close'][:len(df_btc['Close']) - days_to_forcast]
df_test = df_btc['Close'][len(df_btc['Close']) - days_to_forcast:]

# Plot Train & Test Data
plt.figure(figsize=(8,4))
plt.rcParams['figure.dpi'] = 360
plt.plot(df_train, label="Train Data", color = 'red', linewidth=0.8)
plt.plot(df_test, label="Test Data", color = 'blue', linewidth=0.8)
plt.xlabel("Date", fontsize=8) 
plt.ylabel('Close (USD)', fontsize=6)
plt.gca().xaxis.set_major_formatter(mdates.DateFormatter("%m/%Y"))
plt.xticks(fontsize=8, rotation=90)
plt.yticks(fontsize=4)
plt.title("Train & Test Data")

# Data Preprocessing, reshaping  & scaling
scaler = MinMaxScaler()

train_df = df_train.values
train_df = np.reshape(train_df, (len(train_df), 1))

train_df = scaler.fit_transform(train_df)

# Generate the Train dataset
X_train = train_df[0:len(train_df)-1]
y_train = train_df[1:len(train_df)]
X_train = np.reshape(X_train, (len(X_train), 1, 1))

print(train_df.shape)
print(X_train.shape)
print(y_train.shape)

# reshaping Test Set
test_set = df_test.values
modelInputs = np.reshape(test_set, (len(test_set), 1))
modelInputs = scaler.transform(modelInputs)
modelInputs = np.reshape(modelInputs, (len(modelInputs), 1, 1))
print(modelInputs.shape)

# LSTM model

model_LSTM = Sequential()
model_LSTM.add(LSTM(units = 4, activation = 'ReLU', input_shape = (None, 1)))
model_LSTM.add(Dense(units = 1))
model_LSTM.compile(optimizer = 'adam', loss = 'mean_squared_error')
model_LSTM.fit(X_train, y_train, batch_size = 32, epochs = 100)

# Predicting Bitcoin price using LSTM
predicted_BTC_price_LSTM  = model_LSTM.predict(modelInputs)
predicted_BTC_price_LSTM  = scaler.inverse_transform(predicted_BTC_price_LSTM)
MSE_LSTM = mean_squared_error(predicted_BTC_price_LSTM, test_set)
RMSE_LSTM = math.sqrt(MSE_LSTM)
MAPE_LSTM = mean_absolute_percentage_error(test_set, predicted_BTC_price_LSTM)

print("Mean Square Error (MSE) using LSTM:", MSE_LSTM)
print("Root Mean Square Error (MSE) using LSTM:", RMSE_LSTM)
print("Mean Absolute Percentage Error (MAPE) using LSTM:", MAPE_LSTM)

# Visualising the LSTM results
plt.figure(figsize=(8,4))
plt.rcParams['figure.dpi'] = 360
plt.plot(test_set, label = 'Real BTC Price', linewidth=0.8)
plt.plot(predicted_BTC_price_LSTM, color = 'blue', label = 'Predicted BTC Price', linewidth=0.8)
df_test = df_test.reset_index()
x = df_test.index
labels = df_test['Date'].apply(lambda x: x.strftime('%Y-%m-%d'))
plt.xticks(x, labels, rotation = 'vertical')
plt.xlabel("Date", fontsize=8) 
plt.ylabel('BTC Price(USD)', fontsize=6)
plt.xticks(fontsize=8, rotation=90)
plt.yticks(fontsize=4)
plt.legend(loc='upper right', prop={'size': 8})
plt.title("LSTM Prediction")

# GRU model

model_GRU = Sequential()
model_GRU.add(GRU(units = 4, activation = 'ReLU', input_shape = (None, 1))) # try change sigmoid to tangent-
model_GRU.add(Dense(units = 1))
model_GRU.compile(optimizer = 'adam', loss = 'mean_squared_error')
model_GRU.fit(X_train, y_train, batch_size = 32, epochs = 100)

# Prediction from the trained GRU network
predicted_BTC_price_GRU  = model_GRU.predict(modelInputs)
predicted_BTC_price_GRU  = scaler.inverse_transform(predicted_BTC_price_GRU)
MSE_GRU = mean_squared_error(predicted_BTC_price_GRU, test_set)
RMSE_GRU = math.sqrt(MSE_GRU)
MAPE_GRU = mean_absolute_percentage_error(test_set, predicted_BTC_price_GRU)

print("Mean Square Error (MSE) using GRU:", MSE_GRU)
print("Root Mean Square Error (MSE) using GRU:", RMSE_GRU)
print("Mean Absolute Percentage Error (MAPE) using GRU:", MAPE_GRU)

# Visualising the results
plt.figure(figsize=(8,4))
plt.rcParams['figure.dpi'] = 360
plt.plot(test_set, label = 'Real BTC Price', linewidth=0.8)
plt.plot(predicted_BTC_price_GRU, color = 'blue', label = 'Predicted BTC Price', linewidth=0.8)

labels = df_test['Date'].apply(lambda x: x.strftime('%Y-%m-%d'))
plt.xticks(x, labels, rotation = 'vertical')
plt.xlabel("Date", fontsize=8) 
plt.ylabel('BTC Price(USD)', fontsize=6)
plt.xticks(fontsize=8, rotation=90)
plt.yticks(fontsize=4)
plt.legend(loc='upper right', prop={'size': 8})
plt.title("GRU Prediction")

# Bidirectional-LSTM model
model_Bi_LSTM = Sequential()
model_Bi_LSTM.add(Bidirectional(LSTM(units = 4, return_sequences=True), input_shape=(None, 1)))
model_Bi_LSTM.add(Bidirectional(LSTM(units = 4)))
model_Bi_LSTM.add(Dense(1))
model_Bi_LSTM.compile(optimizer = 'adam', loss = 'mean_squared_error')
model_Bi_LSTM.fit(X_train, y_train, batch_size = 32, epochs = 100)

# Prediction from the trained GRU network
predicted_BTC_price_Bi_LSTM = model_Bi_LSTM.predict(modelInputs)
predicted_BTC_price_Bi_LSTM = scaler.inverse_transform(predicted_BTC_price_Bi_LSTM)
MSE_Bi_LSTM = mean_squared_error(predicted_BTC_price_Bi_LSTM, test_set)
RMSE_Bi_LSTM = math.sqrt(MSE_Bi_LSTM)
MAPE_Bi_LSTM = mean_absolute_percentage_error(test_set, predicted_BTC_price_Bi_LSTM)

print("Mean Square Error (MSE) using Bidirectional LSTM:", MSE_Bi_LSTM)
print("Root Mean Square Error (MSE) using Bidirectional LSTM:", RMSE_Bi_LSTM)
print("Mean Absolute Percentage Error (MAPE) using Bidirectional LSTM:", MAPE_Bi_LSTM)

# Visualising the results
plt.figure(figsize=(8,4))
plt.rcParams['figure.dpi'] = 360
plt.plot(test_set, label = 'Real BTC Price', linewidth=0.8)
plt.plot(predicted_BTC_price_Bi_LSTM, color = 'blue', label = 'Predicted BTC Price', linewidth=0.8)

labels = df_test['Date'].apply(lambda x: x.strftime('%Y-%m-%d'))
plt.xticks(x, labels, rotation = 'vertical')
plt.xlabel("Date", fontsize=8) 
plt.ylabel('BTC Price(USD)', fontsize=6)
plt.xticks(fontsize=8, rotation=90)
plt.yticks(fontsize=4)
plt.legend(loc='upper right', prop={'size': 8})
plt.title("Using Bidirectional LSTM")

# Visualising the results
plt.figure(figsize=(8,4))
plt.rcParams['figure.dpi'] = 360
plt.plot(test_set, label = 'Real BTC Price', linewidth=0.8)
plt.plot(predicted_BTC_price_LSTM, color = 'blue', label = 'LSTM', linewidth=0.8)
plt.plot(predicted_BTC_price_GRU, color = 'green', label = 'GRU', linewidth=0.8)
plt.plot(predicted_BTC_price_Bi_LSTM, color = 'yellow', label = 'Bi_LSTM', linewidth=0.8)

labels = df_test['Date'].apply(lambda x: x.strftime('%Y-%m-%d'))
plt.xticks(x, labels, rotation = 'vertical')
plt.xlabel("Date", fontsize=8) 
plt.ylabel('BTC Price(USD)', fontsize=6)
plt.xticks(fontsize=8, rotation=90)
plt.yticks(fontsize=4)
plt.legend(loc='upper right', prop={'size': 8})
plt.title("Combined Prediction vs Actual Price Chart")

from tabulate import tabulate

data = [['LSTM', MSE_LSTM, RMSE_LSTM, MAPE_LSTM],
['GRU', MSE_GRU, RMSE_GRU, MAPE_GRU],
['Bidirectional LSTM', MSE_Bi_LSTM, RMSE_Bi_LSTM, MAPE_Bi_LSTM]]
print (tabulate(data, headers=["Model", "Mean Square Error(MSE)", "Root Mean Square Error(RMSE)", "Mean Absolute Percentage Error(MAPE)"]))