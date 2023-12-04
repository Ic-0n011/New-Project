import keyboard
from random import randint, choice, sample
import os
import time
from sys import exit
from abc import ABC, abstractmethod
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
IMG_PLAYER = "P"
IMG_ANT = "+"
IMG_ANTHILL = "A"
IMG_CELL = "."
BUTTONS = ['space', 'right', 'left', 'up', 'down']


class GameObject(ABC):
    """
    пустой игровой обьект
    """
    @abstractmethod
    def __init__(self, y, x, img) -> None:
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
        self.quantity_ants = 0
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
                if cell.content == cell.img:
                    self.empty_cells.append(cell)

    def create_anthills(self) -> None:
        """создание муравейников"""
        self.get_empty_cells()
        random_empty_cell = sample(self.empty_cells, QUANTITY_ANTHILLS)
        for cell in random_empty_cell:
            anthill = Anthill(cell.y, cell.x)
            self.anthills.append(anthill)
            self.quantity_ants += anthill.ants_inside

    def find_free_nearby_cells(self, x, y) -> list:
        """поиск рядом находящихся пустых клеток"""
        temporary_list = []
        allowed_x = [x, x-1, x+1]
        allowed_y = [y, y-1, y+1]
        for row in self.cells:
            for cell in row:
                if (cell.x in allowed_x) and (cell.y in allowed_y):
                    if not (x == cell.x and y == cell.y):
                        cell.cell_updater()
                        if cell.content == IMG_CELL:
                            temporary_list.append(cell)
        return temporary_list


class Cell():
    
    """
    класс клетка
    клеток в игре ROWS*COLS
    клетка может обновиться, знает что в ней лежит
    """
    def __init__(self, y=int, x=int) -> None:
        self.y = y
        self.x = x
        self.content = None
        self.img = IMG_CELL

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
    """
    класс муравей
    """
    def __init__(self, y, x) -> None:
        self.img = IMG_ANT
        super().__init__(y, x, img=self.img)

    def moving(self) -> None:
        """двигается только в пустые клетку"""
        #FIXME: упростить
        closest_free_cells = game.field.find_free_nearby_cells(
            self.x, self.y)
        if closest_free_cells:
            temporary_list = []
            for cell in closest_free_cells:
                if (cell.x == self.x) or (cell.y == self.y):
                    if not ((cell.x == self.x) and (cell.y == self.y)):
                        temporary_list.append(cell)
        if temporary_list:
            if self.x==(1 or COLS) or self.y==(1 or ROWS) and randint(1,3)!=1:
                game.field.ants.remove(self)
            else:
                tcell = choice(temporary_list)
                self.x = tcell.x
                self.y = tcell.y


class Anthill(GameObject):
    
    """
    класс муравейник
    спавнится от 1 до 4 шт рандомно по полю
    муравейник знает сколько в нем муравьев
    спавнит одного муравья за ход если они остались в нутри
    """
    def __init__(self, y, x) -> None:
        self.img = IMG_ANTHILL
        self.ants_inside = randint(1, 10)
        super().__init__(y, x, img=self.img)

    def spawn_ants(self) -> None:
        """спавн муравьев в рядом находящиеся пустые клетки"""
        if self.ants_inside > 0:
            closest_free_cells = game.field.find_free_nearby_cells(
                self.x, self.y)
            if closest_free_cells:
                temporary_cell = choice(closest_free_cells)
                ant = Ant(temporary_cell.y, temporary_cell.x)
                game.field.ants.append(ant)
                self.ants_inside -= 1


class Player(GameObject):
    """
    класс игрок
    """
    def __init__(self, y, x) -> None:
        self.img = IMG_PLAYER
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

    def show_the_screen(self) -> None:
            """два в одном: показ текстовой части и прорисовка поля"""
            os.system('cls')
            print(
                 "\n Чтобы двигаться вы можете использовать стрелки:"
                "\n вверх, влево, впрво и вниз "
                "\n Если надоест играть вы можете остановить игру нажав пробел"
                "\n "
                )
            if self.field.ants:
                for ant in self.field.ants:
                    ant.moving()
            for anthill in self.field.anthills:
                anthill.spawn_ants()
            for row in self.field.cells:
                for col in row:
                    col.cell_updater()
                    print(col.content, end=' ')
                print()
            self.field.get_empty_cells()
            print(
                "\n набранно очков:"
                f"{self.score_points}/{self.field.quantity_ants}"
                "\n "
                )  

    def moving_the_player(self, key) -> None:
            """движение игрока при помощи кнопок"""
            temporary_list = []
            for anthill in self.field.anthills:
                tx = str(anthill.x)
                ty = str(anthill.y)
                temporary_list.append(tx+ty)
            cury = self.field.player.y
            curx = self.field.player.x
            if key.name == BUTTONS[1]:
                if curx != COLS:
                    if not (str(curx+1)+str(cury) in temporary_list):
                        curx += 1
            elif key.name == BUTTONS[2]:
                if curx != 1:
                    if not (str(curx-1)+str(cury) in temporary_list):
                        curx -= 1
            elif key.name == BUTTONS[3]:
                if cury != 1:
                    if not (str(curx)+str(cury-1) in temporary_list):
                        cury -= 1
            elif key.name == BUTTONS[4]:
                if cury != ROWS:
                    if not (str(curx)+str(cury+1) in temporary_list):
                        cury += 1
            elif key.name == BUTTONS[0]:
                self.game_run = False
            self.field.player.y = cury
            self.field.player.x = curx

    def end_the_game(self) -> None:
            """конец игрового цикла"""
            os.system('cls')
            print(
                "\n Игра законченна!"
                F"\n вы съели:{self.score_points} - муравьев"
                f"\nмуравьев упущенно:{self.field.quantity_ants - self.score_points}"
                )
            self.game_run = False

    def full_verification(self) -> None:
        """
        проверяет наличие ошибок
        если находит ошибку то складывает ее в лист
        если лист не пустой то печатает его и выходит из программы
        """
        error_text = []
        if len(self.field.cells) <= 2:
            error_text.append("Ошибка поля")
        if len(self.field.anthills) <= 0:
            error_text.append("На поле нету муравейников")
        if not self.field.player:
            error_text.append("В игре отсутствует игрок")
        if not (IMG_ANT or IMG_ANTHILL or IMG_CELL or IMG_ANTHILL):
            error_text.append("Один или несколько параметров IMG_ не указан")
        if len(BUTTONS) <= 4:
            error_text.append("Не указанны кнопки взаимодействия")
        if error_text:
            print("НАЙДЕНЫ ОШИБКИ!!!")
            print("----")
            print(", ".join(error_text) if len(error_text) > 1 else error_text[0])
            print("----")
            exit()

    def start_game(self) -> None:
        """подготовка и начало игры"""
        self.field.creating_a_field()
        self.field.create_anthills()
        self.full_verification()
        self.show_the_screen()
        while self.game_run:
            """здесь начинается игровой цикл игры"""
            if len(self.field.ants) <= 0:
                self.end_the_game()
                break
            key = keyboard.read_event()
            if key.event_type == keyboard.KEY_DOWN:
                self.moving_the_player(key)
            self.show_the_screen()
            time.sleep(0.1)

"""
FIXME:
    У игрока проблемы с движением, он пропускает ходы.
TODO:
    В целом код плохо читается, в нем нет консистентности.
"""
game = Game()
game.start_game()
exit()