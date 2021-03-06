from src.constants import *
from src.game_obj import GameObject


class Cannon(GameObject):
    def __init__(self, pos_x, pos_y):
        super().__init__(pos_x, pos_y, 1, 1, 'C', CANNON_HEALTH)
        self.damage = CANNON_DAMAGE
        self.last_fired = 0
        self.range = CANNON_RANGE
        self.fore = Fore.RESET

    def deal_damage(self, damage):
        self._health -= damage
        for i in range(len(HEALTH_RANGE) - 1):
            if 100 * self._health / self._max_health <= HEALTH_RANGE[i]:
                self.fore = OBJECT_COLOUR[i]
                break
