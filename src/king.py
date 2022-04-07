from time import monotonic as clock
from src.constants import *
from src.game_obj import GameObject
# from colorama import Fore, Back, Style

class King(GameObject):
    def __init__(self, pos_x, pos_y):
        super().__init__(pos_x, pos_y, KING_WIDTH, KING_HEIGHT, 'K', KING_MAX_HEALTH)
        self.controls = ['w', 'a', 's', 'd']
        self.damage = KING_DAMAGE
        self.attack_aoe = KING_ATTACK_AOE
        self.last_moved = 0
        self.speed = KING_SPEED

    def move(self, ch):
        if clock() - self.last_moved < 1/self.speed:
            return
        if ch == 'w':
            self._pos_x -= 1
            self.set_last_move(-1, 0)
        if ch == 's':
            self._pos_x += 1
            self.set_last_move(1, 0)
        if ch == 'a':
            self._pos_y -= 1
            self.set_last_move(0, -1)
        if ch == 'd':
            self._pos_y += 1
            self.set_last_move(0, 1)
        self.last_moved = clock()
