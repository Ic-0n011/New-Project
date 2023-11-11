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
table = []

"""
for _ in range(ROWS):
    row = [0] * COLS
    table.append(row)

for y in range(ROWS):
    for x in range(COLS):
        table[y][x] = (y+1,x+1)

for row in table:
    print(*row)
"""

class Field:
    def __init__(self) -> None:
        self.rows = ROWS
        self.cols = COLS
        self.cells = ROWS*COLS

    def draw(self) -> None:
        for _ in range(ROWS):
            row = [0] * self.cols
            table.append(row)
        for y in range(self.rows):
            for x in range(self.cols):
                cell = Cell(y+1,x+1)
                table[y][x] = (cell.img)
        for row in table:
            print(*row)

    
class Cell:
    def __init__(self, y=int, x=int, img) -> None:
        self.img = '.'
        self.y = y
        self.x = x
    


field = Field()
field.draw()