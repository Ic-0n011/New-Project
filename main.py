import keyboard
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


class Field:
    """
    класс поле
    через поле делается многие вещи
    """
    def __init__(self) -> None:
        self.rows = ROWS
        self.cols = COLS
        self.cells = []
        self.anthill = Anthill(1, 1)
        self.player = Player((ROWS//2)+1, (COLS//2)+1)

    def creating_a_field(self) -> None:
        """создание самого поля"""
        for _ in range(ROWS):
            row = [0] * self.cols
            self.cells.append(row)
        for y in range(self.rows):
            for x in range(self.cols):
                cell = Cell(y+1, x+1)
                self.cells[y][x] = cell

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
        if (self.y == game.field.player.y) and (self.x == game.field.player.x):
            self.content = game.field.player.img
        else:
            self.content = self.img


class Ant():
    """
    класс муравей
    двигается рандомно
    !!где спавнятся?!!
    """
    def __init__(self) -> None:
        self.y = None
        self.x = None
        self.img = '+'


class Anthill():
    """
    класс муравейник
    марионетка управляемая полем и игрой
    !!как взаимодействует с Ant?!!
    """
    def __init__(self, y, x) -> None:
        self.y = y
        self.x = x
        self.img = 'A'


class Player():
    """
    класс игрок
    марионетка управляемая полем, игрой и игроком
    """
    def __init__(self, y, x) -> None:
        self.y = y
        self.x = x
        self.img = 'P'


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
        while self.game_run:
            os.system('cls')
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
                    if not (self.field.player.x == COLS):
                        self.field.player.x += 1
                if key.name == 'left':
                    if not (self.field.player.x == 1):
                        self.field.player.x -= 1
                if key.name == 'up':
                    if not (self.field.player.y == 1):
                        self.field.player.y -= 1
                if key.name == 'down':
                    if not (self.field.player.y == ROWS):
                        self.field.player.y += 1
                if key.name == 'space':
                    break


game = Game()
game.start_game()
