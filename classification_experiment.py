import os
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import discrete_signature_lib.discrete_signature as ds
from sklearn.linear_model import LogisticRegression
from sklearn.model_selection import train_test_split
from sklearn.metrics import confusion_matrix
from tqdm import tqdm
from utils import generate_timestamps
def generate_samples(a,b,length):
    prev_error = 0
    timeseries = np.zeros(length)
    for i in range(length):
        error = np.random.normal(0,1)
        timeseries[i] = a*error + b*prev_error
        prev_error = error
    return np.array(timeseries)

def main():
    X = []
    y = []
    timestamps = generate_timestamps(0,100,1)
    for i in tqdm(range(500),"Generating dataset"):
        series_0 = generate_samples(0.5,0.5,100)
        series_1 = generate_samples(0.5,0.75,100)
        if i== 0:
            plt.plot(series_0)
            plt.plot(series_1)
            plt.show()
        sig0 = ds.FlatDiscreteSignature(values = series_0,timestamps = timestamps, k = 2)
        print("got there")
        sig1 = ds.FlatDiscreteSignature(values = series_1,timestamps = timestamps, k = 2)
        X.append(sig0.calculate_signature(0,100)[1:])
        y.append(0)
        X.append(sig1.calculate_signature(0,100)[1:])
        y.append(1)
    train_X, test_X, train_y, test_y = train_test_split(X, y, test_size=0.3, random_state=0) #splitting the data into train and test
    clf = LogisticRegression(random_state=0).fit(train_X, train_y)
    test_cm = confusion_matrix(test_y, clf.predict(test_X))
    print("Test confusion matrix")
    print(test_cm)
    print(clf.score(test_X,test_y))
    train_cm = confusion_matrix(train_y, clf.predict(train_X))  
    print("Train confusion matrix")
    print(train_cm)
    print(clf.score(train_X,train_y))

if __name__ == "__main__":
    main()

    
    