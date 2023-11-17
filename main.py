"""

* <классы>
поле
муравей
муравьед
муравейник
клетка игрового поля
*

"""

ROWS = 5
COLS = 10



class Field:
    def __init__(self) -> None:
        self.rows = ROWS
        self.cols = COLS
        self.cells = []
        self.player = Player(1, 1)

    def creating_a_field(self) -> None:
        for _ in range(ROWS):
            row = [0] * self.cols
            self.cells.append(row)
        for y in range(self.rows):
            for x in range(self.cols):
                cell = Cell(y+1,x+1)
                self.cells[y][x] = cell

    def draw(self) -> None: 
        for row in self.cells:
            for col in row:
                col.cell_updater()
                print(col.content, end=' ')
            print()


class Cell:
    def __init__(self, y=int, x=int) -> None:
        self.y = y
        self.x = x
        self.content = None
        self.img = '.'
        
    def cell_updater(self) -> None:
        if (self.y == field.player.y) and (self.x == field.player.x):
            self.content = field.player.img
        else:
            self.content = self.img


class Player():
    def __init__(self, y, x) -> None:
        self.y = y
        self.x = x
        self.img = 'P'


field = Field()
field.creating_a_field()
field.draw()