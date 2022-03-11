import numpy as np


class Player:
    def __init__(self, pos_x, pos_y, width, height):
        self.pos_x = pos_x
        self.pos_y = pos_y
        self.height = height
        self.width = width
        self.object = np.array([['P' for j in range(width)] for i in range(height)], dtype='object')

    # def move_player