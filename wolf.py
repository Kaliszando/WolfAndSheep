import functions


class Wolf:
    def __init__(self, wolf_move_dist, init_pos_x=0, init_pos_y=0):
        self._x = init_pos_x
        self._y = init_pos_y
        self._move_dist = wolf_move_dist

    def move(self, sheep_pos):
        x = functions.euclidean_dist((self._x, self._y), sheep_pos)
        vec = functions.vector((self._x, self._y), sheep_pos)
        norm_vec = functions.vec_norm(vec, x)
        print(self._x + norm_vec[0] * self._move_dist,
              self._y + norm_vec[1] * self._move_dist,)

    def get_pos(self):
        return self._x, self._y
