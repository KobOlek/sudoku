import pygame as pg
from button import Button

pg.init()

size = WIDTH, HEIGHT = 500, 500

screen = pg.display.set_mode(size)
pg.display.set_caption("Test")

clock = pg.time.Clock()
FPS = 30

button = Button(WIDTH//2-50, HEIGHT//2-50, 250, 250, "Play")

ext = False
while not ext:
    clock.tick(FPS)
    for event in pg.event.get():
        if event.type == pg.QUIT:
            ext = True

    button.draw_button(screen, "red")

    if button.is_pressed():
        print("The button is pressed")
    else:
        print("The button is not pressed")

    pg.display.flip()
pg.quit()