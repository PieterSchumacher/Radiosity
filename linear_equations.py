import numpy as np


def gauss_seidel(A, b, max_it):
    """ 
    Lost het stelsel Ax = b op naar x via Gauss_Seidel methode.

    var A = Radiositeitsmatrix in de vorm zoals ze in de slides staat, voorgesteld door numpy.array
    var b = Vector met bekenden, in numpy.array
    return: oplossing x in numpy.array vorm

    Source: https://en.wikipedia.org/wiki/Gauss–Seidel_method
    """
    
    for i in range(A.shape[0]):
        row = ["{0:3g}*x{1}".format(A[i, j], j + 1) for j in range(A.shape[1])]

    x = np.zeros_like(b)
    for it_count in range(1, max_it):
        x_new = np.zeros_like(x)
        for i in range(A.shape[0]):
            s1 = np.dot(A[i, :i], x_new[:i])
            s2 = np.dot(A[i, i + 1:], x[i + 1:])
            x_new[i] = (b[i] - s1 - s2) / A[i, i]
        if np.allclose(x, x_new, rtol=1e-8):
            break
        x = x_new
    return x
