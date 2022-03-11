from time import monotonic as clock

from src.player import Player
from src.screen import Screen
import src.utils as utils

import sys
import termios
import atexit
from select import select


class Game:
    def __init__(self):
        self._width = utils.SCREEN_WIDTH
        self._height = utils.SCREEN_HEIGHT
        self._screen = Screen(self._width, self._height)

        self._player = Player(10, 10, 5, 5)


    def render(self):
        frame = 0
        while True:
            start_time = clock()

            dr, dw, de = select([sys.stdin], [], [], 0)
            if dr != []:
                if sys.stdin.read(1) == 'w':
                    self._player.pos_x += 1

            self._draw_objects()

            while clock() - start_time < 1:
                pass
            self._screen.display_map()
            print(frame)
            frame += 1

    def _draw_objects(self):
        self._screen.add_object(self._player.pos_x, self._player.pos_y, self._player.object)