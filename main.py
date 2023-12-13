import keyboard
import os
import time
from sys import exit
import variables
from field import Field

"""
игра
field: поле, клетка игрового поля
game objects: муравей, муравьед, муравейник
все глобальные переменные находятся в variables.py
"""


class Game():
    """
    класс игра
    включает в себя игровой цикл и обновление поля
    """
    def __init__(self) -> None:
        self.field = Field()
        self.game_run = True

    def greetings(self) -> None:
        """приветствие и начало игры"""
        print(
            "Добро пожаловать в игру"
            "\n <<Ловкий муравьед>>"
            "\n______________________"
            "\n Вы - голодный, но очень ловкий муравьед (вы <<P>> на поле)."
            "\n Ваша любимая еда это муравьи (они обозначаются <<+>> на поле)."
            "\n На поле так же есть муравейники (<<A>> на поле)"
            "\n муравьи будут выходить из муравейников и искать выход,"
            "\n ваша задача съесть их всех. Удачи!"
            "\n "
            )
        input(
            'Нажмите ENTER для продолжения'
            '\n '
            )

    def show_the_screen(self) -> None:
        """два в одном: показ текстовой части и прорисовка поля"""
        print(
            "Чтобы двигаться вы можете использовать стрелки:"
            "\n вверх, влево, впрво и вниз "
            "\n Если надоест играть вы можете остановить игру нажав [esc]"
            "\n "
            )
        if self.field.ants:
            for ant in self.field.ants:
                ant.moving(self)
        for anthill in self.field.anthills:
            anthill.spawn_ants(self)
        for row in self.field.cells:
            for col in row:
                col.cell_updater(self)
                print(col.content, end=' ')
            print()
        self.field.get_empty_cells(self)
        print(
            "\n набранно очков:"
            f"{self.field.score_points}/{self.field.quantity_ants}"
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
        if key.name == variables.BUTTONS[1]:
            if curx != variables.COLS:
                if not (str(curx+1)+str(cury) in temporary_list):
                    curx += 1
        elif key.name == variables.BUTTONS[2]:
            if curx != 1:
                if not (str(curx-1)+str(cury) in temporary_list):
                    curx -= 1
        elif key.name == variables.BUTTONS[3]:
            if cury != 1:
                if not (str(curx)+str(cury-1) in temporary_list):
                    cury -= 1
        elif key.name == variables.BUTTONS[4]:
            if cury != variables.ROWS:
                if not (str(curx)+str(cury+1) in temporary_list):
                    cury += 1
        elif key.name == variables.BUTTONS[0]:
            self.game_run = False
        self.field.player.y = cury
        self.field.player.x = curx

    def end_the_game(self) -> None:
        """конец игрового цикла"""
        print(
            "\n Игра законченна!"
            F"\n вы съели:{self.field.score_points} - муравьев"
            "\nмуравьев упущенно:"
            f"{self.field.quantity_ants-self.field.score_points}"
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
        if not (
            variables.IMG_ANT
            or variables.IMG_ANTHILL
            or variables.IMG_CELL
            or variables.IMG_ANTHILL
                ):
            error_text.append("Один или несколько параметров IMG_ не указан")
        if len(variables.BUTTONS) <= 4:
            error_text.append("Не указанны кнопки взаимодействия")
        if error_text:
            print("НАЙДЕНЫ ОШИБКИ!!!")
            print("----")
            print(
                ", ".join(error_text) if len(error_text) > 1 else error_text[0]
                )
            print("----")
            exit()

    def start_game(self) -> None:
        """подготовка и начало игры"""
        self.field.creating_a_field()
        self.field.create_anthills(self)
        self.full_verification()
        self.greetings()
        self.show_the_screen()
        while self.game_run:
            """здесь начинается игровой цикл игры"""
            if len(self.field.ants) <= 0:
                self.end_the_game()
                break
            key = keyboard.read_event()
            if key.event_type == keyboard.KEY_DOWN:
                self.moving_the_player(key)
            else:
                continue
            os.system('cls')
            self.show_the_screen()
            time.sleep(0.001)


game = Game()
game.start_game()
exit()
