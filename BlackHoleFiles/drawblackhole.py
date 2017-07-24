from math import sqrt
from game_circle import game_circle
import pygame
import time

from boardentry import BoardEntry

def get_square_grid(screen):
    '''
    Returns a list of points in a square grid to place circles.
    If N rows of circles are to be placed, the grid has dimension
    N * (2N -1). This is to achieve the pyramid pattern.
    '''
    pattern = [i+1 for i in range(6)]
    points = []
    side = 2 * len(pattern) - 1
    screen_size = screen.get_size()
    width = int(0.5 * screen_size[0])  # Use 50% of the width
    height = int(0.8 * screen_size[1])  # Use 80% of the height
    delta_w = int(screen_size[0] * 0.25)  # Middle 50% of the width
    delta_h = int(screen_size[1] * 0.2)  # Lower 80% of the height
    for i in range(len(pattern)):
        row = []
        for j in range(side):
            # row contains tuples of the form (x,y)
            row.append((delta_w + j * (width // side), delta_h + i * (height // len(pattern))))
        points.append(row)
    return points

def get_centres(screen):
    '''
    Extrapolates the centres of the circles from the square grid.
    '''
    pattern = [i+1 for i in range(6)]
    centres = []
    points = get_square_grid(screen)
    for i in range(len(pattern)):
        start_x = (len(points[i])//2)-i              #starting index of a circle in the ith row
        for j in range(pattern[i]):
            centres.append(points[i][start_x + 2*j]) #centre of the jth circle in the row
    return centres

def get_radius(centres):
    '''
    Extrapolates ideal radius for the screen size and number of
    circles.
    '''
    p1,p2 = centres[0], centres[1]
    #Use distance formula
    return int(sqrt((p1[0]-p2[0])**2 + (p1[1] - p2[1])**2))//2


def correct_colour(player):
    if player:
        return 0, 0, 255
    return 255, 0, 0


def draw_static(board_dict, time_limit = 5):
    pygame.init()  # Initialize pygame
    pygame.font.init()  # Initialize fonts
    screen_size = (1024, 576)  # Initialize screen_size
    screen = pygame.display.set_mode(screen_size)
    pygame.display.set_caption("Black Hole Static")
    screen.fill((0, 213, 242))
    circles = []
    centres = get_centres(screen)
    radius = get_radius(centres)
    for centre in centres:
        ob = game_circle(centre=centre, radius=radius)
        circles.append(ob)
    for key in board_dict:
        index = key-1
        if board_dict[key]:
            col = correct_colour(board_dict[key][1])
            val = board_dict[key][0]
            circles[index].update_circle(col, val)

    for circle in circles:
        circle.draw_circle(screen)

    done = False
    st = time.time()
    while not done:
        events = pygame.event.get()
        for event in events:
            if event.type == pygame.QUIT:
                done = True
                continue
        if time.time() - st > time_limit:
            done = True
            continue
        pygame.display.flip()

    pygame.quit()
    # quit()


class BHBoard(object):

    P1_COL = (255, 0, 0)
    P2_COL = (0, 0, 255)

    def __init__(self, screen):
        self.state = [None for index in range(21)]
        self.centres = get_centres(screen)
        self.radius = get_radius(self.centres)
        self.circles = []
        for centre in self.centres:
            ob = game_circle(centre=centre, radius=self.radius)
            self.circles.append(ob)

    def draw(self, screen):
        for circle in self.circles:
            circle.draw_circle(screen)

    def update_circles(self):
        for index in range(len(self.state)):
            if self.state[index]:
                circle_index = index
                colour = correct_colour(self.state[index].player)
                value = self.state[index].value
                self.circles[circle_index].update_circle(colour, value)

    def update_to_state(self, t_state):
        self.state = t_state
        self.update_circles()


    def update_from_input(self, mpos):
        move_count = sum([1 for key in range(len(self.state)) if self.state[key]])
        player = move_count % 2
        value = move_count//2 + 1
        move_tuple = BoardEntry(value, player)
        for circle_index, circle in enumerate(self.circles):
            if circle.is_clicked(mpos) and circle.colour == (0, 0, 0):
                index = circle_index
                self.state[index] = move_tuple
                self.update_circles()



if __name__ == "__main__":
    S_State = {
        1: (1, 1),
        2: (2, 0),
        3: (9, 1),
        4: (4, 0),
        5: (1, 0),
        6: (3, 1),
        7: (4, 1),
        8: (5, 0),
        9: (3, 0),
        10: (5, 1),
        11: (6, 0),
        12: (6, 1),
        13: (9, 0),
        14: (2, 1),
        15: None,
        16: (7, 0),
        17: (7, 1),
        18: (8, 0),
        19: None,
        20: None,
        21: (8, 1)
    }
    # draw_static(S_State)
    state = dict(zip([i + 1 for i in range(21)], [None for i in range(21)]))
    print state