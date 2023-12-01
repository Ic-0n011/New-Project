import keyboard
from random import randint, choice
import os
import time
"""
* <классы>
игра
поле
муравей
муравьед
муравейник
клетка игрового поля
*
"""
ROWS = 7
COLS = 11
QUANTITY_ANTHILLS = randint(1, 4)


class GameObject():
    _abstract = True
    """
    пустой игровой обьект
    """
    def __init__(self, y, x, img) -> None:
        if self._abstract:
            raise NotImplementedError("Cannot instantiate abstract base class")
        self.y = y
        self.x = x
        self.img = img


class Field():
    """
    класс поле
    поле создает и(или) хранит:
        список клеток
        список с пустыми клетками
        муравейники
        муравьев
        игрока(муравьеда)
    """
    def __init__(self) -> None:
        self.rows = ROWS
        self.cols = COLS
        self.anthills = []
        self.cells = []
        self.ants = []
        self.player = Player((ROWS//2)+1, (COLS//2)+1)

    def creating_a_field(self) -> None:
        """создание поля"""
        for _ in range(ROWS):
            row = [0] * self.cols
            self.cells.append(row)
        for y in range(self.rows):
            for x in range(self.cols):
                cell = Cell(y+1, x+1)
                self.cells[y][x] = cell

    def get_empty_cells(self) -> None:
        """создание листа с пустыми клетками"""
        self.empty_cells = []
        for row in self.cells:
            for cell in row:
                cell.cell_updater()
                if cell.content == ".":
                    self.empty_cells.append(cell)

    def create_anthills(self) -> None:
        """создание муравейников"""
        for _ in range(QUANTITY_ANTHILLS):
            self.get_empty_cells()
            if len(self.empty_cells):
                empty_cell = choice(self.empty_cells)
                anthill = Anthill(empty_cell.y, empty_cell.x)
                self.anthills.append(anthill)
            else:
                break


class Cell():
    _abstract = False
    """
    класс клетка
    клеток в игре ROWS*COLS
    клетка может обновиться, знает что в ней лежит
    """
    def __init__(self, y=int, x=int) -> None:
        self.y = y
        self.x = x
        self.content = None
        self.img = '.'

    def cell_updater(self) -> None:
        """обновление внутреклеточного контента и картинки"""
        self.content = None
        if game.field.player.x == self.x and game.field.player.y == self.y:
            self.content = game.field.player.img
        for _ in range(QUANTITY_ANTHILLS):
            for anthill in game.field.anthills:
                if anthill.x == self.x and anthill.y == self.y:
                    self.content = anthill.img
                for ant in game.field.ants:
                    if ant.y == self.y and ant.x == self.x:
                        if self.content == game.field.player.img:
                            game.field.ants.remove(ant)
                            game.score_points += 1
                        else:
                            self.content = ant.img

        if not self.content:
            self.content = self.img


class Ant(GameObject):
    _abstract = False
    """
    класс муравей
    TODO:заставить муравья двигаться(как двигается муравей рандомно или с целью?)
    """
    def __init__(self, y, x) -> None:
        self.img = '+'
        super().__init__(y, x, img=self.img)


class Anthill(GameObject):
    _abstract = False
    """
    класс муравейник
    спавнится от 1 до 4 шт рандомно по полю
    муравейник знает сколько в нем муравьев
    спавнит одного муравья за ход если они остались в нутри
    """
    def __init__(self, y, x) -> None:
        self.img = 'A'
        self.ants_inside = randint(1, 10)
        super().__init__(y, x, img=self.img)

    def find_free_nearby_cells(self) -> list:
            temporary_list = []
            """поиск рядом находящихся пустых клеток"""
            self.allowed_x = [self.x, self.x-1, self.x+1]
            self.allowed_y = [self.y, self.y-1, self.y+1]
            for row in game.field.cells:
                for cell in row:
                    if (cell.x in self.allowed_x) and (cell.y in self.allowed_y):
                        if not (self.x == cell.x and self.y == cell.y):
                            cell.cell_updater()
                            if cell.content == '.':
                                temporary_list.append(cell)
            return temporary_list

    def spawn_ants(self) -> None:
        """спавн муравьев в рядом находящиеся пустые клетки"""
        if self.ants_inside > 0:
            self.closest_free_cells = self.find_free_nearby_cells()
            if self.closest_free_cells:
                suitable_cell = None
                suitable_cell = choice(self.closest_free_cells)
                ant = Ant(suitable_cell.y, suitable_cell.x)
                game.field.ants.append(ant)
                self.ants_inside -= 1
        else:
            pass


class Player(GameObject):
    _abstract = False
    """
    класс игрок
    сам класс нечего не делает
    """
    def __init__(self, y, x) -> None:
        self.img = 'P'
        super().__init__(y, x, img=self.img)


class Game():
    """
    класс игра
    включает в себя игровой цикл и обновление поля
    """
    def __init__(self) -> None:
        self.field = Field()
        self.game_run = True
        self.score_points = 0

    def multi_function(self, master_key, key) -> None|str:
        """мульти функция, выполняет несколько типов задач"""
        if master_key == "show":
            """два в одном: показ текстовой части и прорисовка поля"""
            print(
                    "\nЧтобы двигаться вы можете использовать стрелки на клавиатуре:"
                    "\nвверх, влево, впрво и вниз "
                    "\nЕсли надоест играть вы можете остановить игру нажав пробел."
                    "\n "
                    f"\n набранно очков:{self.score_points} "
                    "\n "
                    )
            for anthill in self.field.anthills:
                anthill.spawn_ants()
            for row in self.field.cells:
                for col in row:
                    col.cell_updater()
                    print(col.content, end=' ')
                print()
            self.field.get_empty_cells()
            return
        elif master_key == "movement":
                xytl = []
                for anthill in self.field.anthills:
                    tx = str(anthill.x)
                    ty = str(anthill.y)
                    xytl.append(tx+ty)
                cury = self.field.player.y
                curx = self.field.player.x
                if key.name == 'right':
                    if curx != COLS:
                        if not (str(curx + 1)+str(cury) in xytl):
                            curx += 1
                elif key.name == 'left':
                    if curx != 1:
                        if not (str(curx - 1)+str(cury) in xytl):
                            curx -= 1
                elif key.name == 'up':
                    if cury != 1:
                        if not (str(curx)+str(cury - 1) in xytl):
                            cury -= 1
                elif key.name == 'down':
                    if cury != ROWS:
                        if not (str(curx)+str(cury + 1) in xytl):
                            cury += 1
                elif key.name == 'space':
                    return "stop"
                self.field.player.y = cury
                self.field.player.x = curx
                return None

    def start_game(self):
        """подготовка и начало игры"""
        self.field.creating_a_field()
        self.field.create_anthills()
        self.multi_function("show", None)
        while self.game_run:
            """здесь начинается игровой цикл игры"""
            key = keyboard.read_event()
            if key.event_type == keyboard.KEY_DOWN:
                temporary_variable = None
                temporary_variable = self.multi_function("movement", key)
                if temporary_variable == "stop":
                    self.game_run = False
                    break
            os.system('cls')
            self.multi_function("show", None)
            time.sleep(0.16)

game = Game()
game.start_game()
