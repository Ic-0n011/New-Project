import keyboard
import random
import os

"""
* <классы>
поле
муравей
муравьед
муравейник
клетка игрового поля
*
"""
ROWS = 7
COLS = 11
ANTHILL_MIN = 1
ANTHILL_MAX = 4


class GameObject():
    """
    !!!запретить создание экземпляра!!!
    пустой игровой обьект
    """
    def __init__(self, y, x, img) -> None:
        self.y = y
        self.x = x
        self.img = img


class Field:
    """
    класс поле
    через поле делается многие вещи
    """
    def __init__(self) -> None:
        self.rows = ROWS
        self.cols = COLS
        self.cells = []
        self.anthills = []
        self.player = Player((ROWS//2)+1, (COLS//2)+1)
        self.ants = None

    def creating_a_field(self) -> None:
        """создание самого поля"""
        for _ in range(ROWS):
            row = [0] * self.cols
            self.cells.append(row)
        for y in range(self.rows):
            for x in range(self.cols):
                cell = Cell(y+1, x+1)
                self.cells[y][x] = cell

    def create_anthills(self):
        quantity_anthills = random.randint(ANTHILL_MIN, ANTHILL_MAX)
        for _ in range(quantity_anthills):
            y = random.randint(1, ROWS)
            x = random.randint(1, COLS)
            print(y, ',', x)
            self.anthills.append(Anthill(x, y))

    def draw(self) -> None:
        """прорисовка и обовление клеток"""
        for row in self.cells:
            for col in row:
                col.cell_updater()
                print(col.content, end=' ')
            print()


class Cell:
    """
    класс клетка
    клеток в игре ROWS*COLS
    """
    def __init__(self, y=int, x=int) -> None:
        self.y = y
        self.x = x
        self.content = None
        self.img = '.'

    def cell_updater(self) -> None:
        """обновление содержимого клетки"""
        for anthill in game.field.anthills:
            if anthill.x == self.x and anthill.y == self.y:
                self.content = anthill.img
        if (self.y == game.field.player.y) and (self.x == game.field.player.x):
            self.content = game.field.player.img
        else:
            self.content = self.img


class Ant(GameObject):
    """
    класс муравей
    двигается рандомно
    !!как спавнятся?!!
    """
    def __init__(self, y, x) -> None:
        self.img = '+'
        super().__init__(y, x, img=self.img)


class Anthill(GameObject):
    """
    класс муравейник
    марионетка управляемая полем и игрой
    спавнится от 1 до 4 шт рандомно по полю
    !!как взаимодействует с Ant?!!
    """
    def __init__(self, y, x) -> None:
        self.img = 'A'
        super().__init__(y, x, img=self.img)


class Player(GameObject):
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

    def start_game(self):
        """подготовка и начало игры"""
        self.field.creating_a_field()
        self.field.create_anthills()
        cury = self.field.player.y
        curx = self.field.player.x
        while self.game_run:
            #os.system('cls')
            print(
                "для движения используйте стрелки: вверх, влево, впрво и вниз;",
                "что бы остановить игру нажмите пробел.",
                sep="\n"
                )
            print("")
            self.field.draw()
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

game = Game()
game.start_game()
