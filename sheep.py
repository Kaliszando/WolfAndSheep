import random
import functions
import logging
from directions import Directions


class Sheep:
    def __init__(self, sheep_move_dist, sheep_id, init_pos_limit):
        self._x = random.uniform(-init_pos_limit, init_pos_limit)
        self._y = random.uniform(-init_pos_limit, init_pos_limit)
        self._move_dist = sheep_move_dist
        self.wolf_dist = None
        self.id = sheep_id
        logging.debug('Sheep.__init__({}, {}, {}) returns: {}'.format(sheep_move_dist, sheep_id, init_pos_limit, None))
        logging.info('Sheep id:{} created on {}'.format(self.id, (self._x, self._y)))

    def move(self):
        direction = random.choice(list(Directions))
        if direction is Directions.NORTH:
            self._y += self._move_dist
        elif direction is Directions.SOUTH:
            self._y -= self._move_dist
        elif direction is Directions.EAST:
            self._x -= self._move_dist
        elif direction is Directions.WEST:
            self._x += self._move_dist
        logging.debug('Sheep.move(), direction: {} returns: {}'.format(direction, None))
        logging.info('Sheep.move() id:{} direction: {}'.format(self.id, direction))

    def update(self, wolf_pos):
        tmp_wolf_dist = self.wolf_dist
        self.wolf_dist = functions.euclidean_dist((self._x, self._y), wolf_pos)
        logging.debug('Sheep.update({}) returns: {}'.format(wolf_pos, None))
        logging.info('Sheep.update() id:{} sheep updated distance to Wolf: {} => {}'.format(
            self.id, tmp_wolf_dist, self.wolf_dist))

    def get_pos(self):
        logging.debug('Sheep.get_pos() returns: {}'.format((self._x, self._y)))
        logging.info('Sheep.get_pos() id:{} pos:{}'.format(self.id, (self._x, self._y)))
        return self._x, self._y
