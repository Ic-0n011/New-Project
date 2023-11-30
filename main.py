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
    через поле делается многие вещи
    """
    def __init__(self) -> None:
        self.rows = ROWS
        self.cols = COLS
        self.anthills = []
        self.cells = []
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

    def create_anthills(self):
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
    """
    def __init__(self, y=int, x=int) -> None:
        self.y = y
        self.x = x
        self.content = None
        self.img = '.'

    def cell_updater(self):
        """обновление внутреклеточного контента и картинки"""
        self.content = None
        if game.field.player.x == self.x and game.field.player.y == self.y:
            self.content = game.field.player.img
        for _ in range(QUANTITY_ANTHILLS):
            for anthill in game.field.anthills:
                if anthill.x == self.x and anthill.y == self.y:
                    self.content = anthill.img
                for ant in anthill.ants:
                    if ant.y == self.y and ant.x == self.x:
                        self.content = ant.img
        if not self.content:
            self.content = self.img


class Ant(GameObject):
    _abstract = False
    """
    класс муравей
    """
    def __init__(self, y, x) -> None:
        self.img = '+'
        super().__init__(y, x, img=self.img)


class Anthill(GameObject):
    _abstract = False
    """
    класс муравейник
    спавнится от 1 до 4 шт рандомно по полю
    """
    def __init__(self, y, x) -> None:
        self.img = 'A'
        self.quantiti_ants = randint(1, 10)
        self.ants = []
        super().__init__(y, x, img=self.img)

    def find_free_nearby_cells(self):
            self.closest_free_cells = []
            """поиск рядом находящихся пустых клеток"""
            self.allowed_x = [self.x, self.x-1, self.x+1]
            self.allowed_y = [self.y, self.y-1, self.y+1]
            for row in game.field.cells:
                for cell in row:
                    if (cell.x in self.allowed_x) and (cell.y in self.allowed_y):
                        if not (self.x == cell.x and self.y == cell.y):
                            cell.cell_updater()
                            if cell.content == '.':
                                self.closest_free_cells.append(cell)

    def spawn_ants(self):
        """спавн муравьев в рядом находящиеся пустые клетки"""
        if self.quantiti_ants > 0:
            self.find_free_nearby_cells()
            if self.closest_free_cells:
                suitable_cell = None
                suitable_cell = choice(self.closest_free_cells)
                ant = Ant(suitable_cell.y, suitable_cell.x)
                self.ants.append(ant)
                self.quantiti_ants -= 1
        else:
            pass


class Player(GameObject):
    _abstract = False
    """
    класс игрок
    марионетка управляемая полем, игрой и игроком
    """
    def __init__(self, y, x) -> None:
        self.img = 'P'
        super().__init__(y, x, img=self.img)


class Game():
    """
    класс игра
    здесь происходят необЪяснимые явления
    """
    def __init__(self) -> None:
        self.field = Field()
        self.game_run = True

    def showing_everything(self):
        """два в одном: показ правил и прорисовка поля"""
        print(
                "\nЧтобы двигаться вы можете использовать стрелки на клавиатуре:"
                "\nвверх, влево, впрво и вниз "
                "\nЕсли надоест играть вы можете остановить игру нажав пробел."
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

    def start_game(self):
        """подготовка и начало игры"""
        self.field.creating_a_field()
        self.field.create_anthills()
        cury = self.field.player.y
        curx = self.field.player.x
        self.showing_everything()
        while self.game_run:
            """здесь начинается игровой цикл игры"""
            key = keyboard.read_event()
            if key.event_type == keyboard.KEY_DOWN:
                if key.name == 'right':
                    if not (curx == COLS):
                        curx += 1
                elif key.name == 'left':
                    if not (curx == 1):
                        curx -= 1
                elif key.name == 'up':
                    if not (cury == 1):
                        cury -= 1
                elif key.name == 'down':
                    if not (cury == ROWS):
                        cury += 1
                elif key.name == 'space':
                    break
            self.field.player.y = cury
            self.field.player.x = curx
            os.system('cls')
            self.showing_everything()
            time.sleep(0.16)

game = Game()
game.start_game()
