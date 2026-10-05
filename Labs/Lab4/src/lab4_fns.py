import numpy as np
import bottleneck as bn

def knn(x_train, class_train, x_test, n_neighbours=3):
    """Algorithme des K plus proches voisins
 
    x_train      : (N_train, d)
    class_train  : (N_train,)
    x_test       : (N_test, d)
    n_neighbours : K
    Returns class_pred : (N_test,) predicted labels
    """
    
    class_train = class_train.astype(int)
    N_test = x_test.shape[0]
    class_pred = np.zeros(N_test, dtype=int)
 
    for q in range(N_test):
        # distance de "q" avec tous les points du training set
        # on calcule pour ça la norme de x_train-q, qui par broadcast correspond à la matrice
        # (x_train_1 - q, ..., x_train_N - q)
        # donc calculer la norme de chaque ligne de cette matrice nous donne les distances
        distances = np.linalg.norm(x_train - x_test[q], axis=1)
 
        # indices des K plus petites distances
        idx = bn.argpartition(distances, n_neighbours - 1)[:n_neighbours] # indices des K plus proches voisins
        labels = class_train[idx] # on récupère les labels de ces points voisins
 
        # vote majoritaire parmis "labels" = c'est notre prédiction
        class_pred[q] = np.argmax(np.bincount(labels))
        # (for regression you would return labels.mean() instead)
 
    return class_pred