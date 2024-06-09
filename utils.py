import numpy as np


def generate_timestamps(start, end, step):
    timestamps = []
    current = start
    while current < end:
        timestamps.append(current)
        current += step
    return np.array(timestamps)

def generate_values(timestamps, function):
    return np.array([function(t) for t in timestamps])



def generate_samples(num_samples,distribution,param,noise = 0):
    if distribution == "exp":
        samples = np.random.exponential(param,num_samples)
    elif distribution == "lognorm":
        samples = np.random.lognormal(param[0],param[1],num_samples)
    elif distribution == "gamma":
        samples = np.random.gamma(param[0],param[1],num_samples)
    else:
        raise ValueError("Invalid distribution")
    if noise != 0:
        samples += np.random.normal(0,noise,num_samples)
    

    return samples



def generate_data(num_samples,distribution,param,noise = 0,start = 0,end = 10,step = 0.1):
    samples = generate_samples(num_samples,distribution,param,noise)
    hist, bins = np.histogram(samples, bins = int((end-start)/step))
    hist = hist/np.sum(hist)
    return bins[:-1],hist


