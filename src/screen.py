import src.constants as utils
import numpy as np
from colorama import Fore, Back, Style

from src.cannon import Cannon


class Screen:
    def __init__(self, width, height):
        self._height = height
        self._width = width

        self._base_map = np.array([[utils.BG_CHAR for j in range(width)] for i in range(height)], dtype='object')
        for i in range(width):
            self._base_map[0][i] = utils.BORDER_CHAR
            self._base_map[height-1][i] = utils.BORDER_CHAR
        for i in range(height):
            self._base_map[i][0] = utils.BORDER_CHAR
            self._base_map[i][width-1] = utils.BORDER_CHAR

        self._map = np.array(self._base_map)

    def clear_map(self):
        self._map = np.array(self._base_map)

    def add_object(self, obj):
        pos_x, pos_y = obj.get_position()
        obj_height, obj_width = obj._object.shape
        if pos_x >= self._width and pos_y >= self._height:
            return
        if pos_x + obj_width < 0 and pos_y + obj_height < 0:
            return

        if obj.fore == Fore.RED:
            if obj.style == Style.DIM:
                obj.style = Style.NORMAL
            else:
                obj.style = Style.DIM

        # indices of the area to be copied
        obj_left, obj_right = max(0, -pos_y), min(obj_width, self._width-pos_y)
        obj_top, obj_bottom = max(0, -pos_x), min(obj_height, self._height-pos_x)
        map_left, map_right = max(0, pos_y), min(self._width, pos_y+obj_width)
        map_top, map_bottom = max(0, pos_x), min(self._height, pos_x+obj_height)

        self._map[map_top:map_bottom, map_left:map_right] = obj.fore + obj.style + obj._object[obj_top:obj_bottom, obj_left:obj_right].copy() + Style.RESET_ALL

        if type(obj) == Cannon and obj.style == Style.BRIGHT:
            obj.style = Style.NORMAL


    def mark_point(self, pos_x, pos_y, ch):
        if pos_x in range(self._height) and pos_y in range(self._width):
            self._base_map[pos_x][pos_y] = ch

    # TODO: add colour
    def display_map(self):
        print(utils.RESET_CURSOR)
        for i in range(self._height):
            for j in range(self._width):
                print(self._map[i][j], end='')
                # print(Fore.RESET)
            print("")
