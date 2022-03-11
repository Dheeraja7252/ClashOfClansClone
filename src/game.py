from time import monotonic as clock

from src.king import King
from src.screen import Screen
import src.constants as utils
from src.constants import *

import sys
import termios
import atexit
from select import select


class Game:
    def __init__(self):
        self._width = utils.SCREEN_WIDTH
        self._height = utils.SCREEN_HEIGHT
        self._screen = Screen(self._width, self._height)

        self._king = King(10, 10, 5, 5)


    def render(self):
        frame = 0
        while True:
            start_time = clock()

            dr, dw, de = select([sys.stdin], [], [], 0)
            if dr != []:
                if sys.stdin.read(1) == 'w':
                    self._king._pos_x += 1

            self._draw_objects()

            while clock() - start_time < TIME_BW_FRAMES:
                pass
            self._screen.display_map()
            print(frame)
            frame += 1

    def _draw_objects(self):
        pos_x, pos_y = self._king.get_position()
        self._screen.add_object(pos_x, pos_y, self._king.object)