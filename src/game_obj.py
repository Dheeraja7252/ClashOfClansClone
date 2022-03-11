import numpy as np


class GameObject:
    def __init__(self, pos_x, pos_y, width, height, ch):
        self._pos_x = pos_x
        self._pos_y = pos_y
        self._height = height
        self._width = width
        self.object = np.array([[ch for j in range(width)] for i in range(height)], dtype='object')

    def get_position(self):
        return self._pos_x, self._pos_y

    def get_dim(self):
        return self._width, self._height
