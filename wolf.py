import functions
import logging

from animal import Animal


class Wolf(Animal):

    closest_sheep_pos = []

    def __init__(self, wolf_move_dist, init_pos_x=0, init_pos_y=0):
        self._pos = [init_pos_x, init_pos_y]
        self._move_dist = wolf_move_dist

        logging.debug('Wolf.__init__({}, {}, {}) returns: {}'.format(wolf_move_dist, init_pos_x, init_pos_x, None))
        logging.info('object of Wolf created on position {}'.format(self._pos))

    def move(self):
        x = functions.calc_euclid_dist(self._pos, self.closest_sheep_pos)
        vec = [self.closest_sheep_pos[i] - self._pos[i] for i in range(len(self._pos))]
        norm_vec = [vec[i] / x for i in range(len(self._pos))]
        new_pos = [self._pos[i] + norm_vec[i] * self._move_dist for i in range(len(self._pos))]
        logging.info('Wolf.move() Wolf moved from {} to {}'.format(self._pos, new_pos))
        self._pos = new_pos
        logging.debug('Wolf.move({}) returns: {}'. format(self.closest_sheep_pos, None))

    @property
    def position(self):
        return self._pos

    @property
    def move_dist(self):
        return self._move_dist
