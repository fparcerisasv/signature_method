# main.py


import time

import numpy as np
import discrete_signature_lib.discrete_signature as ds  
start_time = time.time()
# Example data object
sig = ds.FlatDiscreteSignature(2, np.array([0, 1, 1.5, 2.5, 3]), np.array([[1, 1], [3, 4], [3, 2], [5, 2], [8, 6]], dtype=float), mu=0.693)
# Calculate the signature
signature = sig.calculate_signature(0, 3)
end_time = time.time()
print(f" Execution time: {end_time - start_time:.8f}")

print(f"Signature: \n {list(signature)}")