from math import sqrt
import logging


def euclidean_dist(a, b):
    dist = (b[0] - a[0]) ** 2 + (b[1] - a[1]) ** 2
    logging.debug('functions.euclidean_dist({}, {}) returns: {}'.format(a, b, sqrt(dist)))
    logging.info('functions.euclidean_dist() = {}'.format(sqrt(dist)))
    return sqrt(dist)


def vector(a, b):
    ux = b[0] - a[0]
    uy = b[1] - a[1]
    logging.debug('functions.vector({}, {}) returns: {}'.format(a, b, (ux, uy)))
    logging.info('functions.vector() = {}'.format((ux, uy)))
    return ux, uy


def vec_norm(u, x):
    ux = u[0] / x
    uy = u[1] / x
    logging.debug('functions.vector({}, {}) returns: {}'.format(u, x, (ux, uy)))
    logging.info('functions.vec_norm() = {}'.format((ux, uy)))
    return ux, uy
