import pygame as pg
from random import randint
from button import Button

pg.init()

size = WIDTH, HEIGHT = 450, 450

screen = pg.display.set_mode(size)
pg.display.set_caption("Sudoku")

clock = pg.time.Clock()
FPS = 30


class Cell():
    margin = 2

    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.width = WIDTH // 9 - self.margin
        self.height = HEIGHT // 9 - self.margin
        self.rect = pg.Rect(self.x, self.y, self.width, self.height)
        self.number = 0
        self.can_change_number = True
        self.block_prohibited_numbers = []
        self.row_prohibited_numbers = []
        self.collumn_prohibited_numbers = []
        self.color_text = "black"
        self.color = "skyblue"

    def draw(self):
        pg.draw.rect(screen, pg.Color(self.color), self.rect)
        self.color_text = "black"
        if not self.can_change_number:
            self.color_text = "darkgreen"

        if self.number > 0:
            font = pg.font.Font(None, 25)
            text = font.render(str(self.number), True, pg.Color(self.color_text))
            text_rect = text.get_rect()
            text_rect.center = self.rect.center
            screen.blit(text, text_rect)

    def set_number(self):
        keys = pg.key.get_pressed()
        number_keys = [keys[pg.K_1], keys[pg.K_2], keys[pg.K_3],
                       keys[pg.K_4], keys[pg.K_5], keys[pg.K_6],
                       keys[pg.K_7], keys[pg.K_8], keys[pg.K_9]]

        for i, v in enumerate(number_keys):
            if number_keys[i] and self.rect.collidepoint(pg.mouse.get_pos()) and self.can_change_number \
                    and not (i + 1) in self.block_prohibited_numbers and not (i + 1) in self.row_prohibited_numbers \
                    and not (i + 1) in self.collumn_prohibited_numbers:
                self.number = i + 1

            if keys[pg.K_0] and self.can_change_number:
                self.number = 0

    def change_equal_numbers(self, block):
        collumn = []
        row = []
        block = [block[i].number for i, v in enumerate(block)]
        for i, v in enumerate(blocks):
            cells = blocks[i].cells
            for j, _ in enumerate(cells):
                if self.x == cells[j].x and self.rect != cells[j].rect:
                    collumn.append(cells[j].number)
                if self.y == cells[j].y and self.rect != cells[j].rect:
                    row.append(cells[j].number)


        if (self.number in collumn or self.number in row) and self.number in block and self.number > 0:
            self.number = randint(1, 9)


class Block():
    def __init__(self, x, y, cells):
        self.x = x
        self.y = y
        self.cells = cells
        self.width = (cells[0].width + self.cells[0].margin) * 3
        self.height = (cells[0].height + self.cells[0].margin) * 3
        self.not_repeat_numbers = []

    def draw(self):
        pg.draw.rect(screen, pg.Color("black"), (self.x, self.y, self.width, self.height), 1)

    def get_prohibited_numbers(self):
        prohibited_numbers = []
        for cell, v in enumerate(self.cells):
            prohibited_numbers.append(self.cells[cell].number)

        for c, k in enumerate(self.cells):
            if not self.cells[c] in self.cells[c].block_prohibited_numbers:
                self.cells[c].block_prohibited_numbers = prohibited_numbers
                self.cells[c].change_equal_numbers(self.cells)

    def set_numbers(self):
        k = 0
        number = randint(1, 9)
        if len(self.not_repeat_numbers) < 3:
            while len(self.not_repeat_numbers) < 3:
                if not number in self.not_repeat_numbers:
                    self.not_repeat_numbers.append(number)
                    k += 1
                else:
                    number = randint(1, 9)

            for j, v in enumerate(self.not_repeat_numbers):
                index = randint(0, len(self.cells) - 1)
                if self.cells[index].number > 0:
                    while self.cells[index].number > 0:
                        index = randint(0, len(self.cells) - 1)
                self.cells[index].number = self.not_repeat_numbers[j]
                self.cells[index].can_change_number = False

        self.get_prohibited_numbers()


blocks = [
    Block(0, 0,
          [Cell(x, y) for x in range(0, WIDTH // 3, WIDTH // 9) for y in range(0, HEIGHT // 3, HEIGHT // 9)]),
    Block(150, 0,
          [Cell(x + 150, y) for x in range(0, WIDTH // 3, WIDTH // 9) for y in range(0, HEIGHT // 3, HEIGHT // 9)]),
    Block(300, 0,
          [Cell(x + 300, y) for x in range(0, WIDTH // 3, WIDTH // 9) for y in range(0, HEIGHT // 3, HEIGHT // 9)]),
    Block(0, 150,
          [Cell(x, y + 150) for x in range(0, WIDTH // 3, WIDTH // 9) for y in range(0, HEIGHT // 3, HEIGHT // 9)]),
    Block(150, 150,
          [Cell(x + 150, y + 150) for x in range(0, WIDTH // 3, WIDTH // 9) for y in
           range(0, HEIGHT // 3, HEIGHT // 9)]),
    Block(300, 150,
          [Cell(x + 300, y + 150) for x in range(0, WIDTH // 3, WIDTH // 9) for y in
           range(0, HEIGHT // 3, HEIGHT // 9)]),
    Block(0, 300,
          [Cell(x, y + 300) for x in range(0, WIDTH // 3, WIDTH // 9) for y in range(0, HEIGHT // 3, HEIGHT // 9)]),
    Block(150, 300,
          [Cell(x + 150, y + 300) for x in range(0, WIDTH // 3, WIDTH // 9) for y in
           range(0, HEIGHT // 3, HEIGHT // 9)]),
    Block(300, 300,
          [Cell(x + 300, y + 300) for x in range(0, WIDTH // 3, WIDTH // 9) for y in
           range(0, HEIGHT // 3, HEIGHT // 9)]),
]


def get_row_cells():
    index = 0
    rows = []
    row = []
    cells = [i.cells[j] for i in blocks for j, v in enumerate(i.cells)]
    for j, v in enumerate(cells):
        for i, v in enumerate(cells):
            if cells[index].y == cells[i].y:
                row.append(cells[i])
        else:
            if index < len(cells):
                rows.append(row)
                index += 1
                row = []

    return rows


def get_collumn_cells():
    index = 0
    collumn = []
    col = []
    cells = [i.cells[j] for i in blocks for j, v in enumerate(i.cells)]
    for j, v in enumerate(cells):
        for i, v in enumerate(cells):
            if cells[index].x == cells[i].x:
                col.append(cells[i])
        else:
            if index < len(cells):
                collumn.append(col)
                index += 1
                col = []

    return collumn


for i, v in enumerate(blocks):
    cells = blocks[i].cells
    for j, v in enumerate(cells):
        cells[j].set_number()
        blocks[i].set_numbers()
        cells[j].change_equal_numbers(cells)

ext = False

def create_menu():
    global screen, FPS, clock, ext
    while not ext:
        clock.tick(FPS)
        screen.fill(pg.Color("skyblue"))
        for event in pg.event.get():
            if event.type == pg.QUIT:
                ext = True

        start_button = Button(WIDTH // 2 - 100, HEIGHT // 2 - 50, 200, 100, "Start Game")
        start_button.draw_button(screen, (0, 65, 114))
        start_button.add_event(play)

        pg.display.update()
    return


def play():
    global ext
    while not ext:
        screen.fill(pg.Color("white"))
        for event in pg.event.get():
            if event.type == pg.QUIT:
                ext = True

        for i, v in enumerate(blocks):
            cells = blocks[i].cells
            for j, v in enumerate(cells):
                cells[j].draw()
                cells[j].set_number()
                blocks[i].set_numbers()
                blocks[i].draw()

        for r, v in enumerate(rows := get_row_cells()):
            cells = [rows[r][i] for i, v in enumerate(rows[r])]
            row_numbers = [cells[i].number for i, v in enumerate(cells)]
            for c, v in enumerate(cells):
                cells[c].row_prohibited_numbers = row_numbers

        for k, v in enumerate(collumns := get_collumn_cells()):
            cells = [collumns[k][i] for i, v in enumerate(collumns[k])]
            col_numbers = [cells[i].number for i, v in enumerate(cells)]
            for cell, _ in enumerate(cells):
                cells[cell].collumn_prohibited_numbers = col_numbers

        pg.display.flip()
        clock.tick(FPS)


create_menu()
pg.quit()
