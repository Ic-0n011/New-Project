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
        self.player = Player(0, 0)

    def creating_a_field(self) -> list:
        for _ in range(ROWS):
            row = [0] * self.cols
            self.cells.append(row)
        for y in range(self.rows):
            for x in range(self.cols):
                cell = Cell(y+1,x+1,content)
                self.cells[y][x] = cell

    def draw(self) -> None: 
        for row in self.cells:
            for col in row:
                print(col.img, end=' ')
            print()


class Cell:
    def __init__(self, y=int, x=int, content=str) -> None:
        self.y = y
        self.x = x
        self.img = None
        self.content = content
        if self.content == 'P':
            self.img = 'P'
        if self.content == 'A':
            self.img = 'A'
        if self.content == '+':
            self.img = '+'
        if self.content == None:
            self.img = '.'

        

class Player():
    def __init__(self, y, x) -> None:
        self.y = y
        self.x = x
        self.img = 'P'

field = Field()
field.creating_a_field()
field.draw()
 