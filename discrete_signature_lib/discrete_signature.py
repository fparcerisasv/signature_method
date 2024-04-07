
import numpy as np
from discrete_signature_lib import signature_wrapper as sw
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
    def __init__(self,k,timestamps,values, mu = 1): 
        self.k = k
        self.timestamps = timestamps
        self.values = values

        if len(self.timestamps) != len(self.values):
            print("The number of timestamps and values should be the same.")
            return None
        if len(self.timestamps) == 0:
            print("The array of timestamps is empty.")
            return None
        if len(self.values) == 0:
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

        data = sw.create_data(len(self.timestamps), len(self.values[0])) 
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
        m = np.where(self.timestamps == t_m)[0][0]
        n = np.where(self.timestamps == t_n)[0][0]
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
