class Data: # Data class
    def __init__(self):
        self.times = [] # list of times
        self.values = [] # list of values
        
        

    # Calculate delta_X
    def calculate_delta_X(self):
        self.delta_X = [[0 for i in range(self.d)] for j in range(len(self.times)-1)]
        for i in range(len(self.times)-1): # iterate through the times
            for j in range(self.d): # iterate through the dimensions of the data
                self.delta_X[i][j] = self.values[i+1][j] - self.values[i][j] # calculate delta_X as the difference between the next and current value
    
    def set_times(self, times):
        self.times = times
    
    def set_values(self, values):
        self.values = values
        self.d = len(self.values[0])

class Words:
    # Words class stores a list of all words with length <= k
    def __init__(self, k, d):
        self.k = k  # k is the maximum length of the string
        self.combinations = []  # list of combinations
        self.d = d
        self.generate_combinations()  # generate all combinations of length <= k

    def generate_combinations(self):  # generate all combinations of numbers 0,..,d-1 with signs + and - of length <= k
        # Define a recursive function to generate combinations
        def generate_helper(prefix, length):
            if length == 0:
                self.combinations.append(prefix)
            else:
                for i in range(self.d):
                    generate_helper(prefix + str(i) + '+', length - 1)
                    generate_helper(prefix + str(i) + '-', length - 1)

        # Generate combinations of lengths from 0 to k
        for length in range(self.k + 1):
            generate_helper('', length)

import math # import math library
class Signature:
    def __init__(self, k, data):
        self.k = k # maximum length of the word
        self.data = data # list of strings
        self.mu = 1 # rate of decay
        self.delta_mu = [] # list of exp(-mu*(t_n - t_{n-1}))
        self.iscomputed = {} # dictionary to store the computed values
        self.words = Words(self.k, self.data.d) # list of all words with length <= k
        # Initialize the dictionary iscomputed with False for all words
        for word in self.words.combinations: # iterate through the list of words
            for m in range(len(data.times)):
                for n in range(len(data.times)):
                    self.iscomputed[(word, m, n)] = False
        
        self.sig = {} # dictionary to store the signature values
        self.initialize_signature()
        
    def set_mu(self, mu): # set the rate of decay
        self.mu = mu
        
    def set_delta_mu(self): # set delta_mu
        self.delta_mu = [math.exp(-self.mu * (self.data.times[n] - self.data.times[n-1])) for n in range(1, len(self.data.times))] # exp(-mu*(t_n - t_{n-1}))
   

    def calculate_signature(self,t_m, t_n):
        m = self.data.times.index(t_m) # index of t_m
        n = self.data.times.index(t_n) # index of t_n
        output_sig = {}
        for word in self.words.combinations: # iterate through the list of words
            self.sig[word][m][n] = self.signature(m, n, word) # calculate the signature value
            output_sig[word] = self.sig[word][m][n] # store the signature value in the output_sig dictionary
        return output_sig # return the output_sig dictionary
    
    def initialize_signature(self): # initialize the signature values
        for word in self.words.combinations:
            self.sig[word] = [[0 for i in range(len(self.data.times))] for j in range(len(self.data.times))]
            

    def signature(self, m, n, word): # calculate an element of the signature
        if self.iscomputed[(word, m, n)]: # if the value is already computed
            return self.sig[word][m][n] # return the value
        
        if len(word) == 0: # if the length of the word is 0
            return 1 # return 1
        if m==n and len(word) != 1: # if the length of the word is >=1 and m=n
            return 0 # return 0
        #We use the recursive equation to calculate the signature
        w,i_ = word[:len(word)-2], word[len(word)-2:] # split the word into two parts
        i,sign = i_[0],i_[1] # split the second part into number and sign
        
        if sign == '-': # if it's head
            self.sig[word][m][n]  = self.delta_mu[n-1]*(self.signature(m, n-1, word) + self.data.delta_X[n-1][int(i)]*self.signature(m, n-1, w)) # calculate the signature value
        else: # if it's tail
            
            self.sig[word][m][n] =  self.delta_mu[n-1]*self.signature(m, n-1, word) + self.data.delta_X[n-1][int(i)]*self.signature(m, n, w) # calculate the signature value
        
        self.iscomputed[(word, m, n)] = True # set the value of iscomputed to True
    
        return self.sig[word][m][n] # return the signature value
    
    