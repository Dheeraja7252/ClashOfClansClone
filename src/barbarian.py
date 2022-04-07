from time import monotonic as clock
from src.constants import *
from src.game_obj import GameObject


class Barbarian(GameObject):
    def __init__(self, pos_x, pos_y):
        super().__init__(pos_x, pos_y, 1, 1, 'B', BARB_MAX_HEALTH)
        self.damage = BARB_DAMAGE
        self.last_attack_time = 0
        self.last_moved = 0
        self.speed = BARB_SPEED

    def move(self, x, y):
        if clock() - self.last_moved < 1/self.speed:
            return
        self._pos_x += x
        self._pos_y += y
        self.set_last_move(x, y)
        self.last_moved = clock()
