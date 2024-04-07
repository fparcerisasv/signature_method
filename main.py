# main.py


import time

import numpy as np
from discrete_signature_lib import discrete_signature as ds  
start_time = time.time()
# Example data object
array = np.array([[1, 1], [3, 4], [np.nan, 2], [5, np.nan], [8, 6]], dtype=float)
array = ds.ffill_roll(array) # Fill NaN values 
sig = ds.FlatDiscreteSignature(2, np.array([0, 1, 1.5, 2.5, 3]), array, mu=0.693)
# Calculate the signature
signature = sig.calculate_signature(0, 3)
words = sig.get_words()
end_time = time.time()
print(f"Array: \n {array}")
print(f" Execution time: {end_time - start_time:.8f}")

print(f"Words: \n {list(words)}")
print(f"Signature: \n {list(signature)}")