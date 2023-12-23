import keyboard
import os
import time
from sys import exit
import variables
from field import Field
from Table_of_Record import TableOfRecords


class Game():
    """
    класс игра
    включает в себя игровой цикл и обновление поля
    """
    def __init__(self, nike) -> None:
        self.field = Field()
        self.player_name = nike
        self.tableofrecord = TableOfRecords(filename='records.txt')
        self.game_run = True

    def menu(self) -> None:
        """Меню игры"""
        variable = 0
        arrow1, arrow2, arrow3, arrow4 = "<--", "", "", ""
        arrow_list = [arrow1, arrow2, arrow3, arrow4]
        while True:
            if variable == 0:
                arrow_list[0] = "<--"
            else:
                arrow_list[0] = ""
            if variable == 1:
                arrow_list[1] = "<--"
            else:
                arrow_list[1] = ""
            if variable == 2:
                arrow_list[2] = "<--"
            else:
                arrow_list[2] = ""
            if variable == 3:
                arrow_list[3] = "<--"
            else:
                arrow_list[3] = ""
            print(
                "\n             <<Ловкий муравьед>>\n"
                f"\n\n       Добро пожаловать {self.player_name}!!!\n"
                f"\n          |    Начать новую игру   | {arrow_list[0]}",
                f"\n          |    таблица рекордов    | {arrow_list[1]}",
                f"\n          |        Правила         | {arrow_list[2]}",
                f"\n          |         Выход          | {arrow_list[3]}",
                "\n\nвыберете параметр и нажмите <<enter>>"
                )
            key = keyboard.read_event()
            os.system('cls')
            if key.event_type == keyboard.KEY_DOWN:
                if key.name == variables.BUTTONS[3]:
                    if variable != 0:
                       variable -= 1
                elif key.name == variables.BUTTONS[4]:
                    if variable != 3:
                       variable += 1
                elif key.name == variables.BUTTONS[0]:
                    if variable == 0:
                        self.start_game()
                    elif variable == 1:
                        self.tableofrecord.show_scores()
                        self.pause()
                    elif variable == 2:
                        self.show_rule()
                    elif variable == 3:
                        os.system('cls')
                        print("  . . . Подождите выходим . . .")
                        self.tableofrecord.sorted_scores()
                        self.tableofrecord.write_records_to_file()
                        time.sleep(2)
                        exit()

    def show_rule(self):
        print(
            "\n Вы - голодный, но очень ловкий муравьед (вы <<P>> на поле)."
            "\n Ваша любимая еда это муравьи (они обозначаются <<+>> на поле)."
            "\n На поле так же есть муравейники (<<A>> на поле)."
            "\n Муравьи будут выходить из муравейников и хаотично двигаться,"
            "\n после того как они окажутся на краю поля они могут сбежать,"
            "\n ну ваша поймать и задача съесть их всех. Удачи!"
            "\n \n Чтобы двигаться вы можете использовать стрелки:"
            "\n вверх, влево, впрво и вниз "
            "\n Также вы можете выйти из начатой игры клавишей [esc]"
            )
        self.pause()

    def show_the_update_screen(self) -> None:
        """прорисовка поля и обновление параметров"""
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
        list_of_coordinatess = []
        for anthill in self.field.anthills:
            tx = str(anthill.x)
            ty = str(anthill.y)
            list_of_coordinatess.append(tx+ty)
        current_y = self.field.player.y
        current_x = self.field.player.x
        if key.name == variables.BUTTONS[1]:
            if current_x != variables.COLS:
                if not (str(current_x+1)+str(current_y) in list_of_coordinatess):
                    current_x += 1
        elif key.name == variables.BUTTONS[2]:
            if current_x != 1:
                if not (str(current_x-1)+str(current_y) in list_of_coordinatess):
                    current_x -= 1
        elif key.name == variables.BUTTONS[3]:
            if current_y != 1:
                if not (str(current_x)+str(current_y-1) in list_of_coordinatess):
                    current_y -= 1
        elif key.name == variables.BUTTONS[4]:
            if current_y != variables.ROWS:
                if not (str(current_x)+str(current_y+1) in list_of_coordinatess):
                    current_y += 1
        elif key.name == variables.BUTTONS[5]:
            self.game_run = False
        self.field.player.y = current_y
        self.field.player.x = current_x

    def end_the_game(self) -> None:
        """конец игрового цикла"""
        os.system('cls')
        print(
            "\n Игра законченна!"
            F"\n вы съели:{self.field.score_points} - муравьев"
            "\nмуравьев упущенно:"
            f"{self.field.quantity_ants-self.field.score_points}"
            )
        record = {'name': self.player_name, 'points': self.field.score_points}
        self.tableofrecord.add_record(record)
        self.tableofrecord.sorted_scores()
        self.tableofrecord.write_records_to_file()
        self.pause()

    def pause(self):
        input("\n\nнажмите <<enter>> для продолжений")
        while True:
            key = keyboard.read_event()
            if key.event_type == keyboard.KEY_DOWN:
                if key.name == variables.BUTTONS[0]:
                    self.game_run = False
                    break

    def full_verification(self) -> None:
        """
        проверяет наличие ошибок
        """
        if len(self.field.cells) <= 2:
            print("Ошибка поля")
            exit()
        elif len(self.field.anthills) <= 0:
            print("На поле нету муравейников")
            exit()
        elif not self.field.player:
            print("В игре отсутствует игрок")
            exit()
        elif not (
            variables.IMG_ANT
            or variables.IMG_ANTHILL
            or variables.IMG_CELL
            or variables.IMG_ANTHILL
                ):
            print("Один или несколько параметров IMG_ не указан")
            exit()
        elif len(variables.BUTTONS) <= 4:
            print("Не указанны кнопки взаимодействия")
            exit()


    def start_game(self) -> None:
        """подготовка и начало игры"""
        self.field.creating_a_field()
        self.field.create_anthills(self)
        self.full_verification()
        self.show_the_update_screen()
        while self.game_run:
            if len(self.field.ants) <= 0:
                self.end_the_game()
                break
            key = keyboard.read_event()
            if key.event_type == keyboard.KEY_DOWN:
                self.moving_the_player(key)
            else:
                continue
            os.system('cls')
            self.show_the_update_screen()


print(
    "Добро пожаловать в игру ЛОВКИЙ МУРАВЕД!!!"
    "\nЕсли вы хотите продолжить то  вам необходимо придумать свой ник!"
    "\nОбратите внимание что ник должен состоять не менее чем из 3 символов"
    "\nа также не более чем из 8 смиволов"
    )
patience = 2
while True:
    time.sleep(0.5)
    nike = input("\nнапишите свой игровой ник: ")
    if len(nike) < 3 or len(nike) > 8 or not nike:
        if patience == 0:
            print("вы ввели ник неправильно несколько раз")
            print("поэтому мы присвоили вам ник <Муравьед")
            nike = "Муравьед"
            time.sleep(1.5)
            break
        print("такой ник не допустим, поробуйте еще раз")
        patience -= 1
    else:
        break


game = Game(nike)
game.menu()
exit()
