import numpy as np

from src.game_obj import GameObject


class King(GameObject):
    def __init__(self, pos_x, pos_y, width, height):
        GameObject.__init__(self, pos_x, pos_y, width, height, 'K')

    # def move_player