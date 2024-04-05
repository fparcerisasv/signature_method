# main.py

import classes_sig_c as sw

# Example data object
data = sw.create_data(5, 2)
times = [0, 1, 1.5, 2.5, 3]
values = [[1, 1], [3, 4], [3, 2], [5, 2], [8, 6]]
sw.set_times(data, times)
sw.set_values(data, values)

delta_X = sw.calculate_delta_X(data)
# Signature object
signature = sw.create_signature(2, data)
print(":)")
sw.set_mu(signature, 0.693)
sw.set_delta_mu(signature)

# Calculate the signature
print(sw.calculate_signature(signature, 0, 4))
