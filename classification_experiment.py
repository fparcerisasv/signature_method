import os
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import discrete_signature_lib.discrete_signature as ds
from sklearn.ensemble import RandomForestClassifier
from sklearn.linear_model import LogisticRegression
from sklearn.model_selection import train_test_split
from sklearn.metrics import confusion_matrix
from sklearn.preprocessing import StandardScaler
from tqdm import tqdm
from utils import generate_timestamps
def generate_samples(a,b,c,length):
    prev_error = 0
    timeseries = np.zeros(length)
    timeseries[0] = a
    for i in range(1,length):
        error = np.random.normal(0,1)
        timeseries[i] = a + error + b*prev_error + c*timeseries[i-1]
        prev_error = error
    return np.array(timeseries)

def main():
    X = []
    y = []
    timestamps = generate_timestamps(0,100,1)
    file_path = os.path.join(os.path.dirname(__file__), "class_experiment.csv")
    for i in range(500):
        series_0 = generate_samples(0.5,0.5,0.4,100)
        series_1 = generate_samples(0.5,0.7,0.8,100)
        #if i== 0:
        #    plt.plot(series_0)
        #    plt.plot(series_1)
        #    plt.show()
        sig0 = ds.FlatDiscreteSignature(values = series_0,timestamps = timestamps, k = 3)
        sig1 = ds.FlatDiscreteSignature(values = series_1,timestamps = timestamps, k = 3)
        X.append(sig0.calculate_signature(0,99)[1:])
        y.append(0)
        X.append(sig1.calculate_signature(0,99)[1:])
        y.append(1)
    X = StandardScaler().fit_transform(X)
    train_X, test_X, train_y, test_y = train_test_split(X, y, test_size=0.3, random_state=0) #splitting the data into train and test
    clf = RandomForestClassifier(n_estimators=100)
    clf.fit(train_X,train_y)
    test_cm = confusion_matrix(test_y, clf.predict(test_X))
    print("Test confusion matrix")
    print(test_cm)
    print(clf.score(test_X,test_y))
    train_cm = confusion_matrix(train_y, clf.predict(train_X))  
    print("Train confusion matrix")
    print(train_cm)
    print(clf.score(train_X,train_y))
    file = open(file_path, "w")
    file.write("Test confusion matrix\n")
    file.write(str(test_cm))
    file.write("\n")
    file.write(str(clf.score(test_X,test_y)))
    file.write("\n")
    file.write("Train confusion matrix\n")
    file.write(str(train_cm))
    file.write("\n")
    file.write(str(clf.score(train_X,train_y)))
    file.close()

if __name__ == "__main__":
    main()

    
    