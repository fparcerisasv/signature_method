# signature_wrapper.py

import ctypes
import numpy as np

# Load the shared library
signature_lib = ctypes.CDLL('./signature.so')

# Define structures for Data and Signature
class Data(ctypes.Structure):
    _fields_ = [
        ('times', ctypes.POINTER(ctypes.c_double)),
        ('values', ctypes.POINTER(ctypes.POINTER(ctypes.c_double))),
        ('d', ctypes.c_int),
        ('num_times', ctypes.c_int)
    ]

class Signature(ctypes.Structure):
    _fields_ = [
        ('k', ctypes.c_int),
        ('data', Data),
        ('mu', ctypes.c_double),
        ('delta_mu', ctypes.POINTER(ctypes.c_double)),
        ('iscomputed', ctypes.POINTER(ctypes.c_bool)),
        ('words', ctypes.POINTER(ctypes.c_char_p)),
        ('sig', ctypes.POINTER(ctypes.POINTER(ctypes.POINTER(ctypes.c_double))))
    ]

# Define function signatures for the C functions
signature_lib.create_data.argtypes = [ctypes.c_int, ctypes.c_int]
signature_lib.create_data.restype = ctypes.POINTER(Data)

signature_lib.set_times.argtypes = [ctypes.POINTER(Data), ctypes.POINTER(ctypes.c_double)]
signature_lib.set_times.restype = None

signature_lib.set_values.argtypes = [ctypes.POINTER(Data), ctypes.POINTER(ctypes.POINTER(ctypes.c_double))]
signature_lib.set_values.restype = None

signature_lib.calculate_delta_X.argtypes = [ctypes.POINTER(Data)]
signature_lib.calculate_delta_X.restype = ctypes.POINTER(ctypes.POINTER(ctypes.c_double))

signature_lib.create_signature.argtypes = [ctypes.c_int, ctypes.POINTER(Data)]
signature_lib.create_signature.restype = ctypes.POINTER(Signature)

signature_lib.set_mu.argtypes = [ctypes.POINTER(Signature), ctypes.c_double]
signature_lib.set_mu.restype = None

signature_lib.set_delta_mu.argtypes = [ctypes.POINTER(Signature)]
signature_lib.set_delta_mu.restype = None

signature_lib.calculate_signature.argtypes = [ctypes.POINTER(Signature), ctypes.c_int, ctypes.c_int]
signature_lib.calculate_signature.restype = ctypes.POINTER(ctypes.POINTER(ctypes.c_double))


# Define wrapper functions for Data and Signature classes
def create_data(num_times, d):
    return signature_lib.create_data(num_times, d)

def set_times(data, times):
    c_times = (ctypes.c_double * len(times))(*times)
    signature_lib.set_times(data, c_times)

def set_values(data, values):
    # Convert Python list of lists to array of arrays of doubles
    c_values = (ctypes.POINTER(ctypes.c_double) * len(values))()
    for i, row in enumerate(values):
        c_values[i] = (ctypes.c_double * len(row))(*row)
    # Pass the array of arrays of doubles to the C function
    signature_lib.set_values(data, c_values)





def calculate_delta_X(data):
    return signature_lib.calculate_delta_X(data)

def create_signature(k, data):
    return signature_lib.create_signature(k, data)

def set_mu(signature, mu):
    signature_lib.set_mu(signature, mu)

def set_delta_mu(signature):
    signature_lib.set_delta_mu(signature)

def calculate_signature(signature, m, n):
    return signature_lib.calculate_signature(signature, m, n).contents
