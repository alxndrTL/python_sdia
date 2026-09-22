import numpy as np

def gradient2D(X: np.array) -> np.array:
    # check that X is a 2D matrix
    if X.ndim >2 :
        raise ValueError("Input array must have at most 2 dimensions")

    X_D = np.column_stack((
        X[:, 1:] - X[:, :-1],
        np.zeros(X.shape[0])
    ))

    D_X = np.vstack((
        X[1:, :] - X[:-1, :],
        np.zeros(X.shape[1])
    ))

    return X_D, D_X
