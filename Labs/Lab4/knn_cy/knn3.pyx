cimport cython

import numpy as np
import bottleneck as bn

@cython.boundscheck(False)
@cython.wraparound(False)
def knn(x_train, class_train, x_test, int n_neighbours=3):
    # changement par rapport à knn2 : ascontiguousarray
    # cython stocke donc ces arrays de manière contigue en mémoire ce qui accélère les lectures
    x_train = np.ascontiguousarray(x_train, dtype=np.float64)
    x_test = np.ascontiguousarray(x_test, dtype=np.float64)
    class_train = np.asarray(class_train, dtype=np.int64) # indices donc int

    # memory views sur les tableaux de données train et test
    cdef double[:, ::1] x_train_view = x_train # vue mémoire contigue avec ::1
    cdef double[:, ::1] x_test_view = x_test

    # on définit ici les variables qui vont être utilisées dans la boucle
    cdef Py_ssize_t N_train = x_train_view.shape[0]
    cdef Py_ssize_t N_test = x_test_view.shape[0]
    cdef Py_ssize_t D = x_train_view.shape[1]
    cdef Py_ssize_t q, i, d
    cdef double s, tmp

    class_pred = np.zeros(N_test, dtype=np.int64)
    distances = np.zeros(N_train, dtype=np.float64)
    cdef double[:] dist = distances # une vue sur distance
    # (on va y stocker les distances au carré plutôt que les distances, peu importe pour le tri)

    for q in range(N_test):

        # calcule de la distance avec tous les points de train
        # contrairement au cas python, on ne peut pas utiliser le broadcast de numpy, donc on écrit une boucle
        for i in range(N_train):
            s = 0.0
            for d in range(D):
                tmp = x_train_view[i, d] - x_test_view[q, d]
                s += tmp * tmp
            dist[i] = s

        # on utilise le même bloc pour trouver la classe prédite, en utilisant bottleneck, np.bincount et np.argmax
        # comme le dit la consigne, on se concentre sur la première partie
        idx = bn.argpartition(distances, n_neighbours - 1)[:n_neighbours]
        labels = class_train[idx]
        class_pred[q] = np.argmax(np.bincount(labels))

    return class_pred
