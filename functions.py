from math import sqrt
import logging


def calc_euclid_dist(a, b):
    dist = (b[0] - a[0]) ** 2 + (b[1] - a[1]) ** 2
    logging.debug('functions.euclidean_dist({}, {}) returns: {}'.format(a, b, sqrt(dist)))
    logging.info('functions.euclidean_dist() = {}'.format(sqrt(dist)))
    return sqrt(dist)
