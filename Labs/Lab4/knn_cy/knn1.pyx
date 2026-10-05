import numpy as np

def compute(array_1, array_2, alpha):
    """
    This function must implement the formula
    array_1 + alpha * array_2

    array_1 and array_2 are 2D.
    """
    x_max = array_1.shape[0]
    y_max = array_1.shape[1]

    assert array_1.shape == array_2.shape

    result = np.zeros((x_max, y_max), dtype=array_1.dtype)

    for x in range(x_max):
        for y in range(y_max):
            tmp = array_1[x, y]
            tmp = tmp + array_2[x, y] * alpha
            result[x, y] = tmp

    return result
