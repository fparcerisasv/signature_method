
import numpy as np
import discrete_signature_lib.signature_wrapper as sw
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

    signature : list of floats
    
    '''
    
    def calculate_signature(self, t_m, t_n):
        m = np.where(self.timestamps == t_m)[0][0]
        n = np.where(self.timestamps == t_n)[0][0]
        return sw.calculate_signature(self.signature, m, n)
