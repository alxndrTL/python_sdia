import numpy as np

#docstring following the numpy format
def gradient2D(X: np.array) -> np.array:
    """
    Compute the discrete gradient of a 2D matrix along both axes.

    The derivative along each axis is approximated using forward finite
    differences (f[i+1] - f[i]). The last column (resp. last row) is set
    to zero to match the shape of the input.

    Parameters
    ----------
    X : np.ndarray
        Input 2D matrix of shape (M, N).

    Returns
    -------
    X_D : np.ndarray
        Horizontal gradient (along columns), of shape (M, N)..
    D_X : np.ndarray
        Vertical gradient (along rows), of shape (M, N).

    Raises
    ------
    ValueError
        If X has more than 2 dimensions.

    Examples
    --------
    >>> X = np.array([[1, 2, 3],
    ...               [4, 5, 6]])
    >>> X_D, D_X = gradient2D(X)
    >>> X_D  # horizontal differences
    array([[1., 1., 0.],
           [1., 1., 0.]])
    >>> D_X  # vertical differences
    array([[3., 3., 3.],
           [0., 0., 0.]])
    """
    # check that X is a 2D matrix
    if X.ndim > 2:
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

def tv(X: np.array) -> float:
    """
    Compute the Total Variation (TV) of a 2D matrix.

    The total variation is defined as the sum of the gradient magnitudes
    over all pixels, where border differences are set to zero (see gradient2D).

    ...

    References
    ----------
    .. [1] Condat, L. (2017). Discrete Total Variation: New Definition and
           Minimization. *SIAM Journal on Imaging Sciences*, 10(3), 1258–1290.
           https://hal.archives-ouvertes.fr/hal-01309685


    Parameters
    ----------
    X : np.ndarray
        Input 2D matrix of shape (M, N).

    Returns
    -------
    float
        Total variation of X (non-negative).

    Examples
    --------
    >>> tv(np.zeros((3, 3)))
    0.0
    >>> tv(np.ones((3, 3)))
    0.0
    >>> tv(np.array([[0, 1], [0, 1]]))
    2.0
    """
    X_D, D_X = gradient2D(X)
    return np.sum(np.sqrt(X_D**2 + D_X**2))

def gradient2D_adjoint(Y: np.array) -> np.array:
    """
    Compute the adjoint (negative divergence) of the 2D discrete gradient.

    Concretely, G* is the negative discrete divergence, computed via
    backward finite differences.

    Parameters
    ----------
    Y : np.ndarray
        Input array of shape (2, M, N), where Y[0] is the horizontal
        component and Y[1] is the vertical component.

    Returns
    -------
    np.ndarray
        Adjoint of the gradient applied to Y, of shape (M, N).

    Raises
    ------
    ValueError
        If Y does not have shape (2, M, N).

    Examples
    --------
    >>> Y = np.zeros((2, 3, 3))
    >>> gradient2D_adjoint(Y)
    array([[0., 0., 0.],
           [0., 0., 0.],
           [0., 0., 0.]])
    """
    if Y.ndim != 3 or Y.shape[0] != 2:
        raise ValueError("Y must have shape (2, M, N).")

    # Adjoint of the horizontal gradient
    Y_D = np.column_stack((
        -Y[0][:, 0],
        -(Y[0][:, 1:-1] - Y[0][:, :-2]),
        Y[0][:, -2]
    ))

    # Adjoint of the vertical gradient
    D_Y = np.vstack((
        -Y[1][0, :],
        -(Y[1][1:-1, :] - Y[1][:-2, :]),
        Y[1][-2, :]
    ))

    return Y_D + D_Y
