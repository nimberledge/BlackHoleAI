from math import *

import pygame

import button
import colour as col


class game_circle(object):
    '''
    Class to create circle objects
    '''

    def __init__(self, radius=None, centre=(0, 0), colour=(0, 0, 0), value=None):
        '''
        Constructor.
        Instance variables are self explanatory.
        '''
        self.radius = radius
        self.centre = centre
        self.x = centre[0]
        self.y = centre[1]
        self.colour = colour
        self.value = value
        self.text = ''
        if self.value:
            self.text = str(self.value)
        self.generate_tbox()  # Generating the textbox to display the value

    def generate_tbox(self):
        '''
        Generating the textbox to display the value.
        '''
        x = int(self.x - (self.radius / sqrt(2)))
        y = int(self.y - (self.radius / sqrt(2)))
        w = int(sqrt(2) * self.radius)
        fnt = pygame.font.SysFont('Times New Roman', 25)
        self.tbox = button.button(self.text, x, y, w, w, self.colour, col.WHITE, fnt)

    def draw_circle(self, screen):
        '''
        Draws circle onto screen.
        '''
        pygame.draw.circle(screen, self.colour, self.centre, self.radius, 0)
        self.tbox.draw(screen)

    def is_clicked(self, mpos):
        '''
        Boolean to determine if a mouseclick is within the range of a circle.
        '''
        if (self.x - self.radius) < mpos[0] < (self.x + self.radius) and (self.y - self.radius) < mpos[1] < (
                    self.y + self.radius):
            return True
        return False

    def update_circle(self, colour, value):
        '''
        Changes a circle's colour and value.
        '''
        self.colour = colour
        self.value = value
        # Regenerate textbox
        if value:
            self.text = str(self.value)
        else:
            self.text = ''
        self.generate_tbox()

    def is_adjacent(self, circle):
        '''
        Boolean to find if one circle is adjacent to another. Change
        margin of error for large patterns.
        '''
        p1 = self.centre
        p2 = circle.centre
        dist = int(sqrt((p1[0] - p2[0]) ** 2 + (p1[1] - p2[1]) ** 2))
        moa = 10  # Margin of error
        if abs(2 * self.radius - dist) < moa:
            return True
        return False
