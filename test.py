class Cell:
    def __init__(self):
        self.value = " "

    def set_value(self, value):
        self.value = value

    def get_value(self):
        return self.value


class Field:
    def create_field(self, height, width):
        field = []
        for _ in range(height):
            row = [Cell() for _ in range(width)]
            field.append(row)
        return field

    def print_field(self, field):
        for row in field:
            print(".".join(cell.get_value() for cell in row))


if __name__ == "__main__":
    field = Field().create_field(5, 10)
    Field().print_field(field) 