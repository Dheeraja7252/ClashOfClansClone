from time import monotonic as clock

from src.barbarian import Barbarian
from src.cannon import Cannon
from src.game_obj import GameObject
from src.keyboard import KeyBoard
from src.input import *
from src.king import King
from src.screen import Screen
from src.constants import *
from src.utils import *


# Tasks left:
# modify cannons?
# Game speed
# Spells?
# Replays
# colour based on health

class Game:
    def __init__(self):
        self._width = SCREEN_WIDTH
        self._height = SCREEN_HEIGHT
        self._screen = Screen(self._width, self._height)

        # create game objects
        self._king = King(KING_POS_X, KING_POS_Y)

        townhall = GameObject(TOWNHALL_POS_X, TOWNHALL_POS_Y, TOWNHALL_WIDTH, TOWNHALL_HEIGHT, 'T', TOWNHALL_HITPOINTS)
        self._buildings = [townhall]
        for hut_pos in HUT_POS:
            hut = GameObject(hut_pos[0], hut_pos[1], HUT_WIDTH, HUT_HEIGHT, 'H', HUT_HITPOINTS)
            self._buildings.append(hut)

        self._walls = []
        for wall_pos in WALL_POS:
            wall = GameObject(wall_pos[0], wall_pos[1], 1, 1, '*', WALL_HITPOINTS)
            self._walls.append(wall)

        self._barbarians = []

        self._spawning_points = SPAWN_POINTS

        for i in range(len(SPAWN_POINTS)):
            self._screen.mark_point(SPAWN_POINTS[i][0], SPAWN_POINTS[i][1], MARK_SPAWN[i])

        self._cannons = []
        for cannon_pos in CANNON_POS:
            cannon = Cannon(cannon_pos[0], cannon_pos[1])
            self._cannons.append(cannon)

        self._kb = KeyBoard()
        # self._kb_input = Get()

    def render(self):
        frame = 0
        while True:
            start_time = clock()

            self.handle_kb_input()
            self.troops_attack()
            self.cannons_fire()
            self.purge_game_objects()
            self.move_troops()
            self.handle_collisions()
            self._draw_objects()

            while clock() - start_time < TIME_BW_FRAMES:
                pass
            self._screen.display_map()
            print(frame)
            frame += 1

    def _draw_objects(self):
        self._screen.clear_map()

        pos_x, pos_y = self._king.get_position()
        self._screen.add_object(pos_x, pos_y, self._king._object)

        for wall in self._walls:
            pos_x, pos_y = wall.get_position()
            self._screen.add_object(pos_x, pos_y, wall._object)

        for building in self._buildings:
            pos_x, pos_y = building.get_position()
            self._screen.add_object(pos_x, pos_y, building._object)

        for barb in self._barbarians:
            pos_x, pos_y = barb.get_position()
            self._screen.add_object(pos_x, pos_y, barb._object)

        for cannon in self._cannons:
            pos_x, pos_y = cannon.get_position()
            self._screen.add_object(pos_x, pos_y, cannon._object)

    # TODO: use tut input class
    def handle_kb_input(self):
        if not key_press():
            return

        ch = getch()
        # ch = input_to(getch(), 0)

        if ch == 'q':
            self.game_over(False)
        if ch in self._king.controls:
            self._king.move(ch)
        if ch == ' ':
            self._king_attack()
        if ch in ['1', '2', '3']:
            ind = int(ch) - 1
            self.spawn_troops(self._spawning_points[ind][0], self._spawning_points[ind][1])

        flush()

    def game_over(self, win):
        # print(CLEAR)
        if win:
            print("win")
        else:
            print("lose")
        raise SystemExit

    def handle_collisions(self):
        self._king_collisions()
        self._barbarian_collisions()

    def _king_collisions(self):
        for obj in self._walls:
            if check_collision(self._king, obj):
                self._king.undo_last_move()

        for obj in self._buildings:
            if check_collision(self._king, obj):
                self._king.undo_last_move()

        pos_x, pos_y = self._king.get_position()
        width, height = self._king.get_dim()

        new_pos_x = max(1, min(pos_x, self._height - height - 1))
        new_pos_y = max(1, min(pos_y, self._width - width - 1))
        self._king.set_position(new_pos_x, new_pos_y)

    def _barbarian_collisions(self):
        for barb in self._barbarians:
            for obj in self._walls:
                if check_collision(barb, obj):
                    barb.undo_last_move()
                    if clock() > barb.last_attack_time + BARB_ATTACK_TIMESTEP:
                        barb.last_attack_time = clock()
                        obj.deal_damage(barb.damage)

            for obj in self._buildings:
                if check_collision(barb, obj):
                    barb.undo_last_move()

    def _king_attack(self):
        for obj in self._walls:
            if get_distance(self._king, obj) <= self._king.attack_aoe:
                obj.deal_damage(self._king.damage)

        for obj in self._buildings:
            if get_distance(self._king, obj) <= self._king.attack_aoe:
                obj.deal_damage(self._king.damage)

    def purge_game_objects(self):
        if self._king.get_health() <= 0:
            self._king = None

        new_barb = []
        for barb in self._barbarians:
            if barb.get_health() > 0:
                new_barb.append(barb)
        self._barbarians = new_barb

        new_walls = []
        for wall in self._walls:
            if wall.get_health() > 0:
                new_walls.append(wall)
        self._walls = new_walls

        new_buildings = []
        for building in self._buildings:
            if building.get_health() > 0:
                new_buildings.append(building)
        self._buildings = new_buildings

        if self._king is None and len(self._barbarians) == 0:
            self.game_over(False)
        elif len(self._buildings) == 0:
            self.game_over(True)

    def spawn_troops(self, pos_x, pos_y):
        for _ in range(TROOP_SIZE):
            new_barb = Barbarian(pos_x, pos_y)
            self._barbarians.append(new_barb)

    def move_troops(self):
        cur_time = clock()

        for barb in self._barbarians:
            if cur_time < barb.last_attack_time + BARB_ATTACK_TIMESTEP:
                continue

            closest = None
            for building in self._buildings:
                if closest is None:
                    closest = building
                elif get_distance(barb, building) < get_distance(barb, closest):
                    closest = building

            barb_pos_x, barb_pos_y = barb.get_position()
            build_pos_x, build_pos_y = closest.get_position()
            width, height = closest.get_dim()

            x = 0
            if barb_pos_x < build_pos_x:
                x = 1
            elif barb_pos_x > build_pos_x + height:
                x = -1

            y = 0
            if barb_pos_y < build_pos_y:
                y = 1
            elif barb_pos_y > build_pos_y + width:
                y = -1
            barb.move(x, y)

    def troops_attack(self):
        cur_time = clock()

        for barb in self._barbarians:
            if cur_time < barb.last_attack_time + BARB_ATTACK_TIMESTEP:
                continue
            for building in self._buildings:
                if get_distance(barb, building) < 1:
                    building.deal_damage(barb.damage)
                    barb.last_attack_time = cur_time
                    break

            # if cur_time < barb.last_attack_time + BARB_ATTACK_TIMESTEP:
            #     continue
            # for wall in self._walls:
            #     if get_distance(barb, wall) < 1:
            #         wall.deal_damage(barb.damage)
            #         barb.last_attack_time = cur_time
            #         break

    def cannons_fire(self):
        for cannon in self._cannons:
            if clock() < cannon.last_fired + CANNON_COOL_OFF:
                continue

            target = self._king
            for barb in self._barbarians:
                if get_distance(barb, cannon) < get_distance(target, cannon):
                    target = barb
            if get_distance(target, cannon) <= cannon.range:
                target.deal_damage(cannon.damage)
                cannon.last_fired = clock()
