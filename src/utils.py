import sys
import termios
from select import select


def getch():
    return sys.stdin.read(1)


def key_press():
    dr, dw, de = select([sys.stdin], [], [], 0)
    return dr != []


def flush():
    termios.tcflush(sys.stdin, termios.TCIOFLUSH)


def check_collision(obj1, obj2):
    pos_x1, pos_y1 = obj1.get_position()
    width1, height1 = obj1.get_dim()

    pos_x2, pos_y2 = obj2.get_position()
    width2, height2 = obj2.get_dim()

    collision_x = pos_x1 + height1 > pos_x2 and pos_x2 + height2 > pos_x1
    collision_y = pos_y1 + width1 > pos_y2 and pos_y2 + width2 > pos_y1

    return collision_x and collision_y


def get_distance(obj1, obj2):
    pos_x1, pos_y1 = obj1.get_position()
    width1, height1 = obj1.get_dim()

    pos_x2, pos_y2 = obj2.get_position()
    width2, height2 = obj2.get_dim()

    dx = 0
    if pos_x1 + height1 < pos_x2:
        dx = pos_x2 - (pos_x1 + height1)
    if pos_x2 + height2 < pos_x1:
        dx = pos_x1 - (pos_x2 + height2)

    dy = 0
    if pos_y1 + width1 < pos_y2:
        dy = pos_y2 - (pos_y1 + width1)
    if pos_y2 + width2 < pos_y1:
        dy = pos_y1 - (pos_y2 + width2)

    return dx + dy
