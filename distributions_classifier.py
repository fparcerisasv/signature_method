from tqdm import tqdm
from utils import *
import numpy as np
import discrete_signature_lib.discrete_signature as ds
import time
from sklearn.decomposition import PCA
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
import pandas as pd
import os
def build_dataset(num_samples,dataset_size):
    X = []
    y = []
    for i in range(dataset_size):
        scale = np.random.uniform(0.5,2)
        timestamps,values=generate_data(num_samples,"exp",scale)
        X.append(values)
        y.append("Exponential")

        sigma = np.random.uniform(0.25,1)
        timestamps,values=generate_data(num_samples,"lognorm",(0,sigma))
        X.append(values)
        y.append("Lognormal")

        shape = np.random.uniform(0.5,10)
        timestamps,values=generate_data(num_samples,"gamma",(2,shape))
        X.append(values)
        y.append("Gamma")
    return X,y,timestamps

def get_results(k,n_estimators,test_size,num_samples,dataset_size):
    X,y,timestamps = build_dataset(num_samples,dataset_size)
    #Random Forest Classifier
    clf = RandomForestClassifier(n_estimators=n_estimators)
    clf_sig = RandomForestClassifier(n_estimators=n_estimators)
    clf_pca = RandomForestClassifier(n_estimators=n_estimators)
    #Training with raw data
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=test_size, random_state=0) #splitting the data into train and test

    start_time = time.time()
    clf.fit(X_train, y_train)
    time1 = time.time() - start_time


    #Training with signature
    X_train_sig = []
    y_train_sig = []
    y_test_sig = []
    X_test_sig = []
    for i in range(len(X_train)):
        signature = ds.FlatDiscreteSignature(values = X_train[i],timestamps = timestamps, k =k)
        sig = signature.calculate_signature(0,5)
        if not np.isnan(sig).any():
            X_train_sig.append(sig)
            y_train_sig.append(y_train[i])
    for i in range(len(X_test)):
        signature = ds.FlatDiscreteSignature(values = X_test[i],timestamps = timestamps, k =k)
        sig = signature.calculate_signature(0,5)
        if not np.isnan(sig).any():
            X_test_sig.append(sig)
            y_test_sig.append(y_test[i])


    start_time = time.time()

    clf_sig.fit(X_train_sig, y_train_sig)
    time2 = time.time() - start_time

    vector_size = len(X_train_sig[0])
    pca = PCA(n_components=vector_size)
    X_train_pca = pca.fit_transform(X_train)
    X_test_pca = pca.transform(X_test)
    start_time = time.time()
    clf_pca.fit(X_train_pca, y_train)
    time3 = time.time() - start_time

    return {"raw":{"score":clf.score(X_test,y_test),"time":time1},"signature":{"score":clf_sig.score(X_test_sig,y_test_sig),"time":time2},"pca":{"score":clf_pca.score(X_test_pca,y_test),"time":time3}}
def save_results(results,raw_csv_path):
    results_df = pd.DataFrame(results)
    results_df.to_csv(raw_csv_path)

def main():
    ks = [4,5]
    num_sampleses = [100,1000,10000]
    dataset_sizes = [100,1000,10000]
    n_estimators = 100
    test_size = 0.2
    num_experiments = 25
    for k in ks:
        for num_samples in num_sampleses:
            for dataset_size in dataset_sizes:
                if num_samples >= 1000 and dataset_size == 10000:
                    break
                directory = f"experimental_results/k_{k}_num_samples_{num_samples}_dataset_size_{dataset_size}"
                if not os.path.exists(directory):
                    os.makedirs(directory)
                results = {"raw":[],"signature":[],"pca":[]}
                for i in tqdm(range(num_experiments),f"k = {k}, num_samples = {num_samples}, dataset_size = {dataset_size}"):
                    results_ = get_results(k,n_estimators,test_size,num_samples,dataset_size)
                    results["raw"].append(results_["raw"])
                    results["signature"].append(results_["signature"])
                    results["pca"].append(results_["pca"])
                raw_csv_path = f"{directory}/raw_results.csv"
                save_results(results["raw"],raw_csv_path)
                signature_csv_path = f"{directory}/signature_results.csv"
                save_results(results["signature"],signature_csv_path)
                pca_csv_path = f"{directory}/pca_results.csv"
                save_results(results["pca"],pca_csv_path)

if __name__ == "__main__":
    main()



