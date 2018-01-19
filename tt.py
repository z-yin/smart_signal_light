from numba import jit
from numpy import arange
from datetime import datetime

# jit decorator tells Numba to compile this function.
# The argument types will be inferred by Numba when function is called.


@jit
def sum2d(arr):
    M, N = arr.shape
    result = 0.0
    for i in range(M):
        for j in range(N):
            result += arr[i,j]
    return result

a = arange(9999999).reshape(3333333,3)
start = datetime.now()
print(sum2d(a))
stop = datetime.now()
print(stop-start)