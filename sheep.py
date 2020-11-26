import random
import functions
import logging

from animal import Animal
from directions import Directions


class Sheep(Animal):

    def __init__(self, sheep_move_dist, sheep_id, init_pos_limit):
        self._pos = [
            random.uniform(-init_pos_limit, init_pos_limit),
            random.uniform(-init_pos_limit, init_pos_limit)]
        self._move_dist = sheep_move_dist
        self.id = sheep_id
        logging.debug('Sheep.__init__({}, {}, {}) returns: {}'.format(sheep_move_dist, sheep_id, init_pos_limit, None))
        logging.info('Sheep id:{} created on {}'.format(self.id, self._pos))

    def move(self):
        direction = random.choice(list(Directions))
        if direction is Directions.NORTH:
            self._pos[1] += self._move_dist
        elif direction is Directions.SOUTH:
            self._pos[1] -= self._move_dist
        elif direction is Directions.WEST:
            self._pos[0] -= self._move_dist
        elif direction is Directions.EAST:
            self._pos[0] += self._move_dist

        logging.debug('Sheep.move(), direction: {} returns: {}'.format(direction, None))
        logging.info('Sheep.move() id:{} direction: {}'.format(self.id, direction))

    @property
    def position(self):
        return self._pos
