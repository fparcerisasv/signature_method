from scipy.optimize import least_squares,curve_fit
from utils import *
import numpy as np
import discrete_signature_lib.discrete_signature as ds
from scipy.stats import expon
import time
import pandas as pd
import tqdm
def make_experiment(k):
    timestamps = generate_timestamps(0, 5, 0.1)
    target_scale = np.random.uniform(0.5,4)
    initial_guess = np.random.uniform(0.5,4)
    times,target = generate_data(10000,"exp",target_scale,start= 0,end = 10, step = 0.1) #target signature
    target_sig = ds.FlatDiscreteSignature(values = target,timestamps = times, k=k).calculate_signature(0,10)
    def exp_sig(s):
        vals = generate_values(timestamps,expon(scale = s).pdf)
        vals = ds.ffill_roll(vals)
        signature = ds.FlatDiscreteSignature(values = vals,timestamps = timestamps, k =k)
        return signature.calculate_signature(0,5)
    def diff(s):
        return target_sig - exp_sig(s)
    def exp_pdf(x,s):
        return expon(scale = s).pdf(x)
    start = time.time() 
    res = least_squares(fun=diff ,x0=initial_guess)
    time1 = time.time() - start
    start = time.time()
    popt, pcov = curve_fit(exp_pdf,times,target,p0 = initial_guess)
    time2 = time.time() - start
    error1 = (target_scale - res.x[0])**2
    error2 = (target_scale - popt[0])**2
    return error1,error2,time1,time2

def main():
    kas = [2,3,4,5]
    mean_errors = {k:[] for k in kas}
    mean_times = {k:[] for k in kas}
    for k in kas:
        errors1 = []
        errors2 = []
        times1 = []
        times2 = []

        for i in tqdm.tqdm(range(100),desc = f"Running expermients with K = {k}"):
            error1,error2,time1,time2 = make_experiment(k)
            errors1.append(error1)
            errors2.append(error2)
            times1.append(time1)
            times2.append(time2)
        
        mean_errors[k].append(np.mean(errors1))
        mean_errors[k].append(np.mean(errors2))
        mean_times[k].append(np.mean(times1))
        mean_times[k].append(np.mean(times2))
    print(mean_errors )
    print(mean_times)
if __name__ == "__main__":
    main()