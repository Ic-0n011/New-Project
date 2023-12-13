import variables
from abc import ABC, abstractmethod
from random import choice, randint


class GameObject(ABC):
    """
    пустой игровой обьект
    """
    @abstractmethod
    def __init__(self, y, x, img) -> None:
        self.y = y
        self.x = x
        self.img = img


class Ant(GameObject):
    """
    класс муравей
    """
    def __init__(self, y, x) -> None:
        self.img = variables.IMG_ANT
        super().__init__(y, x, img=self.img)

    def moving(self, game) -> None:
        """двигается только в пустые клетку"""
        next_x = self.x
        next_y = self.y
        allowed_x = [self.x-1, self.x+1]
        allowed_y = [self.y-1, self.y+1]
        if randint(0, 1) == 1:
            next_x = choice(allowed_x)
            if (next_x > variables.COLS) or (next_x < 1):
                game.field.ants.remove(self)
                return
        else:
            next_y = choice(allowed_y)
            if (next_y > variables.ROWS) or (next_y < 1):
                game.field.ants.remove(self)
                return
        game.field.get_empty_cells(game)
        for cell in game.field.empty_cells:
            if cell.x == next_x:
                if cell.y == next_y:
                    self.x = next_x
                    self.y = next_y
                    break
        return


class Anthill(GameObject):
    """
    класс муравейник
    спавнится от 1 до 4 шт рандомно по полю
    муравейник знает сколько в нем муравьев
    спавнит одного муравья за ход если они остались в нутри
    """
    def __init__(self, y, x) -> None:
        self.img = variables.IMG_ANTHILL
        self.ants_inside = randint(1, 10)
        super().__init__(y, x, img=self.img)

    def spawn_ants(self, game) -> None:
        """спавн муравьев в рядом находящиеся пустые клетки"""
        if self.ants_inside > 0:
            closest_free_cells = game.field.find_free_nearby_cells(
                game, self.x, self.y)
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
        self.img = variables.IMG_PLAYER
        super().__init__(y, x, img=self.img)
