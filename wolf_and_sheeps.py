from math import sqrt

import functions
from wolf import Wolf

init_pos_limit = 10.0

x = functions.euclidean_dist((1, 1), (4, 3))
u = functions.vector((1, 1), (4, 3))

w = Wolf(5.0, 1.0, 1.0)
w.move((7, 1))