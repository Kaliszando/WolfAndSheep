from math import sqrt


def euclidean_dist(a, b):
    dist = (b[0] - a[0]) ** 2 + (b[1] - a[1]) ** 2
    return sqrt(dist)


def vector(a, b):
    ux = b[0] - a[0]
    uy = b[1] - a[1]
    return ux, uy


def vec_norm(u, x):
    ux = u[0] / x
    uy = u[1] / x
    return ux, uy
