import functions
import logging


class Wolf:
    def __init__(self, wolf_move_dist, init_pos_x=0, init_pos_y=0):
        self._x = init_pos_x
        self._y = init_pos_y
        self.move_dist = wolf_move_dist
        logging.debug('Wolf.__init__({}, {}, {}) returns: {}'.format(wolf_move_dist, init_pos_x, init_pos_x, None))
        logging.info('object of Wolf created on position {}'.format((self._x, self._y)))

    def move(self, sheep_pos):
        x = functions.euclidean_dist((self._x, self._y), sheep_pos)
        vec = functions.vector((self._x, self._y), sheep_pos)
        norm_vec = functions.vec_norm(vec, x)
        new_x = self._x + norm_vec[0] * self.move_dist
        new_y = self._y + norm_vec[1] * self.move_dist
        logging.info('Wolf.move() Wolf moved from {} to {}'.format((self._x, self._y), (new_x, new_y)))
        self._x = new_x
        self._y = new_y
        logging.debug('Wolf.move({}) returns: {}'. format(sheep_pos, None))

    def get_pos(self):
        logging.debug('Wolf.get_pos() returns: {}'.format((self._x, self._y)))
        logging.info('Wolf.get_pos() pos:{}'.format((self._x, self._y)))
        return self._x, self._y
