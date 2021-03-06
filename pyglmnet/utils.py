"""
A few miscellaneous helper functions for pyglmnet.py
"""

import numpy as np


def softmax(w):
    """Softmax function of given array of number w

    Parameters
    ----------
    w: array | list
        The array of numbers.

    Returns
    -------
    dist: array
        The resulting array with values ranging from 0 to 1.
    """
    w = np.array(w)
    maxes = np.amax(w, axis=1)
    maxes = maxes.reshape(maxes.shape[0], 1)
    e = np.exp(w - maxes)
    dist = e / np.sum(e, axis=1, keepdims=True)
    return dist


def label_binarizer(y):
    """Mimics scikit learn's LabelBinarizer


    Parameters
    ----------
    y: ndarray, shape (n_samples, )
        one dimensional array of class labels

    Returns
    -------
    yb: array, shape (n_samples, n_classes)
        one-hot encoding of labels in y
    """
    if y.ndim != 1:
        raise ValueError('y has to be one-dimensional')
    y_flat = y.ravel()
    yb = np.zeros([len(y), y.max() + 1])
    yb[np.arange(len(y)), y_flat] = 1
    return yb


def log_likelihood(y, yhat, distr):
    """Helper to compute the log likelihood."""
    eps = np.spacing(1)
    if distr in ['softplus', 'poisson']:
        return np.sum(y * np.log(eps + yhat) - yhat)
    elif distr == 'binomial':
        # Log likelihood of model under consideration
        return 2 * len(y) * \
            np.sum(y * np.log((yhat == 0) + yhat) / np.mean(yhat) +
                   (1 - y) * np.log((yhat == 1) +
                                    1 - yhat) / (1 - np.mean(yhat)))
    elif distr == 'gaussian':
        return np.sum((y - yhat)**2)
    elif distr == 'multinomial':
        y = label_binarizer(y)
        # yhat is the probability of each output
        if yhat.ndim != y.ndim:
            msg = 'yhat and ynull must be (n_samples, n_class) ndarrays'
            raise ValueError(msg)
        return np.sum(y * np.log(yhat))


def tikhonov_from_prior(PriorCov, n_samples):
    """Given a prior covariance matrix, returns a Tikhonov matrix"""
    [U, S, V] = np.linalg.svd(PriorCov, full_matrices=False)
    Tau = np.dot(np.diag(1. / np.sqrt(S)), U)
    Tau = 1. / np.sqrt(np.float(n_samples)) * Tau / Tau.max()
    return Tau
