
import numpy as np
import sys
import os
import importlib.util
spec = importlib.util.spec_from_file_location("signature_wrapper", os.path.join(os.path.dirname(__file__), "./signature_wrapper.py"))
sw = importlib.util.module_from_spec(spec)
sys.modules['signature_wrapper'] = sw
spec.loader.exec_module(sw)
class FlatDiscreteSignature:
    '''
    Class for computing the flat discrete signature of a given data object
    k : int
        maximum length of the word
    timestamps : numpy array
        array of timestamps
    values : numpy array
        array of values
    mu : float
    '''
    def __init__(self,k,timestamps,values, mu = 0): 
        self.k = k
        self.timestamps = timestamps
        self.values = values


        if timestamps.shape[0] != values.shape[0]:
            print("The number of timestamps and values should be the same.")
            return None
        if timestamps.shape[0] == 0:
            print("The array of timestamps is empty.")
            return None
        if values.shape[0] == 0:
            print("The array of values is empty.")
            return None
        if np.isnan(self.timestamps).any() or np.isnan(self.values).any():
            print("The arrays contain NaN values.")
            return None
        self.data = self.create_data()
        self.signature = self.create_signature()
        self.set_mu(mu)
        self.set_delta_mu()
        

    def create_data(self):
        if len(self.values.shape) == 1:
            self.values = np.expand_dims(self.values, axis = 1)
        data = sw.create_data(self.values.shape[0], self.values.shape[1]) 
        sw.set_times(data, self.timestamps)
        sw.set_values(data, self.values)
        sw.calculate_delta_X(data)
        return data
    
    def create_signature(self):
        return sw.create_signature(self.k, self.data)
    
    def set_mu(self, mu):
        self.mu = mu
        sw.set_mu(self.signature, mu)
    
    def set_delta_mu(self):
        sw.set_delta_mu(self.signature)

    '''
    Returns the flat discrete signature of the data object
    t_m : float
        start time
    t_n : float
        end time
    
    Returns

    signature : numpy array 
    
    '''
    
    def calculate_signature(self, t_m, t_n):
        m = np.argmin(np.abs(self.timestamps - t_m))
        n = np.argmin(np.abs(self.timestamps - t_n))
        return sw.calculate_signature(self.signature, m, n)

    '''
    Returns the words of the signature
    '''
    def get_words(self):
        return sw.get_words(self.signature)
    


''' 
Function to fill the NaN values in a numpy array using the forward fill method
'''
    
def ffill_roll(arr, fill=0, axis=0):
    mask = np.isnan(arr)
    replaces = np.roll(arr, 1, axis)
    slicing = tuple(0 if i == axis else slice(None) for i in range(arr.ndim))
    replaces[slicing] = fill
    while np.count_nonzero(mask) > 0:
        arr[mask] = replaces[mask]
        mask = np.isnan(arr)
        replaces = np.roll(replaces, 1, axis)
    return arr


def ffill_loop(arr, fill=0):
    mask = np.isnan(arr[0])
    arr[0][mask] = fill
    for i in range(1, len(arr)):
        mask = np.isnan(arr[i])
        arr[i][mask] = arr[i - 1][mask]
    return arr