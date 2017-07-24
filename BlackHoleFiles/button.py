import pygame

class button(object):
    '''
        Class to store and operate on button.
    '''
    def __init__(self, text = None, x = None, y = None, w = 10, h = 10, color = None, tColor = None, fnt = None):
        self.rect = pygame.Rect(x, y, w, h)
        self.x, self.y, self.w, self.h = x, y, w, h
        self.text = text
        self.color = color
        self.tColor = tColor
        self.fnt = fnt

    def draw(self, window):
        pygame.draw.rect(window, self.color, self.rect)
        txt = self.fnt.render(self.text, True, self.tColor)
        window.blit(txt, (self.x + self.w / 2 - txt.get_width() / 2, self.y + self.h / 2 - txt.get_height() / 2))

    def clicked(self, mpos):
        if self.x < mpos[0] < self.x + self.w and self.y < mpos[1] < self.y + self.h:
            return True
        return False
