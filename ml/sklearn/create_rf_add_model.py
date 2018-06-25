# -*- coding: utf-8 -*-
"""This script generates a sklearn random forest
model that predict values that were created using the
formula (a + b) / 2

The two arrays a and b must have values with range [0, 256].

"""
import numpy as np
import pickle
from sklearn import tree
from sklearn.externals.six import StringIO
from sklearn.cluster import KMeans
from sklearn.model_selection  import cross_val_score
from sklearn.model_selection  import cross_val_predict
from sklearn.metrics import mean_squared_error
from sklearn.ensemble import RandomForestRegressor
import pandas as pd
from sklearn.externals import joblib

def compute_efficiency(model_result, measurement):
    diff = model_result - measurement
    eff = 1- sum(diff * diff)/((measurement.var()) * len(measurement))
    return(eff)

print("Create training data")

# Train a value adder that represents the formula (a + b) / 2
a = np.random.randint(-1, 257, 1000)
b = np.random.randint(-1, 257, 1000)
# Create the predicting data that is used for training
c = (a + b)/2
# Cast to integer
y = c.astype(int)

print("Train random forest model")
model = RandomForestRegressor(n_estimators=100, max_depth=12, max_features="log2", n_jobs=16,
                              min_samples_split=2, min_samples_leaf=1, verbose=0)
# This is the training data with two arrays
X = pd.DataFrame()

X["a"] = a
X["b"] = b

# Fit the model and compute the model efficiency
model = model.fit(X, y)
# Predict values
predicted_values = model.predict(X)
# Compute the score of the model
score = model.score(X, y)
# Compute the mean square error
mse = mean_squared_error(predicted_values, y)

print("Model score", score, "MSE", mse)

print("Perform 10-fold cross validation")

# Perform the cross validation and compute the model efficiency
cv_score = cross_val_score(model, X, y, cv=10)
cv_predicted_values = cross_val_predict(model, X, y, cv=10)
# Compute the efficiency of the cross validation
cv_eff = compute_efficiency(cv_predicted_values, y)
# Compute the mean square error
cv_mse = mean_squared_error(cv_predicted_values, y)

print("CV score", cv_eff, "MSE", cv_mse)

print("Save the model as compressed joblib object")

# Save the model with compression
joblib.dump(value=model, filename='rf_add_model.pkl.xz', compress=("xz", 3))


