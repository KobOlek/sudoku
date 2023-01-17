import pygame as pg
class Button():
    def __init__(self, x, y, width, height, text):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.text = text
        self.rect = pg.Rect(self.x, self.y, self.width, self.height)

    def draw_button(self, screen, color):
        pg.draw.rect(screen, color, self.rect)
        font = pg.font.Font(None, self.width//4)
        text = font.render(self.text, True, pg.Color("white"))
        text_rect = text.get_rect()
        text_rect.center = self.rect.center
        screen.blit(text, text_rect)

    def add_event(self, function):
        if self.rect.collidepoint(pg.mouse.get_pos()) and pg.mouse.get_pressed()[0]:
            function()