import time
from math import *

import colour as col
import game_circle


class Board(object):
    '''
    Class to create and play on a single game
    '''
    pattern = [1,2,3,4,5,6] #Number of circles on each line
    player1_col = col.RED  #Colour for player 1
    player2_col = col.BLUE   #Colour for player 2
    moves = [(i//2 + 1) for i in range(sum(pattern) - 1)] #Determines which number to place on game board
    points_lost_p1 = 0 #For final point counting
    points_lost_p2 = 0 #For final point counting
    end_flag = 0       #Determines end of game, and other animation-based ideas
    
    def __init__(self, screen):
        '''
        Constructor
        Only grid and player_turn are instance variables
        '''
        self.grid = []              #List of game circles
        self.initialize_grid(screen)
        self.player_turn = 0        #Determines player's turns
        

    def initialize_grid(self, screen):
        '''
        Determines centres and radii as per screen size
        and generates the grid of game-circles as per requirement.
        '''
        centres = Board.get_centres(screen)
        radius = Board.get_radius(centres)
        for i in range(len(centres)):
            #Create the game circle, add it to the list
            ob = game_circle.game_circle(radius, centres[i])
            self.grid.append(ob)

    def draw_board(self, screen):
        '''
        Draws circles onto screen, and accounts for the endgame.
        ''' 
        for circle in self.grid: #Draw circles
            circle.draw_circle(screen)
        if self.player_turn == len(Board.moves) and Board.end_flag==1: #Black out circles adjacent to black hole
            Board.delay_loop(1)
            self.adjacent_to_black_hole()
            Board.end_flag = -1
        elif self.player_turn == len(Board.moves) and Board.end_flag == 0: #Endgame flag
            Board.end_flag = 1

    def update_board(self, mpos):
        '''
        Updates the state of the board based on a mouse click.
        '''
        colour = None #Default initialization
        if self.player_turn >= len(Board.moves): #If endgame, don't register the click
            return None
        for circle in self.grid:
            #If a circle is clicked and it has not been clicked before, update the colour and value of that circle
            if circle.is_clicked(mpos) and circle.colour == game_circle.game_circle.def_col:
                #Determine which player's turn it is
                if self.player_turn %2==1:
                    colour = Board.player2_col
                elif self.player_turn%2==0:
                    colour = Board.player1_col
                value = Board.moves[self.player_turn]
                circle.update_circle(colour, value)
                self.player_turn +=1
                break

    @staticmethod
    def draw_static(board_dict):
        pass

    @staticmethod
    def delay_loop(t):
        '''
        Gives a delay loop of exactly t seconds
        '''
        st = time.time()
        while time.time()-st <t:
            pass

    def black_hole(self):
        '''
        Finds the black hole in the board. To be used only after endgame is reached.
        Returns the index of the blackhole in the grid.
        '''
        for circle in self.grid:
            if circle.colour == game_circle.game_circle.def_col: #Find the circle with the unchanged colour
                return self.grid.index(circle)

    def adjacent_to_black_hole(self):
        '''
        Blanks out all the squares adjacent to the black hole, and
        totals the points of the game.
        '''
        black_hole = self.black_hole()
        for circle in range(len(self.grid)):
            if circle == black_hole:
                continue
            elif self.grid[circle].is_adjacent(self.grid[black_hole]):
                #Add the points to required points_lost variable
                if self.grid[circle].colour == Board.player1_col:
                    Board.points_lost_p1 += self.grid[circle].value
                elif self.grid[circle].colour == Board.player2_col:
                    Board.points_lost_p2 += self.grid[circle].value
                #Blanks out the square
                self.grid[circle].update_circle(game_circle.game_circle.def_col, value = None)
        
        
    @staticmethod
    def get_square_grid(screen):
        '''
        Returns a list of points in a square grid to place circles.
        If N rows of circles are to be placed, the grid has dimension
        N * (2N -1). This is to achieve the pyramid pattern.
        '''
        pattern = Board.pattern
        points = []
        side = 2*len(pattern) - 1
        screen_size = screen.get_size()
        width = int(0.5 * screen_size[0])  #Use 50% of the width
        height = int(0.8 * screen_size[1]) #Use 80% of the height
        delta_w = int(screen_size[0] * 0.25) #Middle 50% of the width
        delta_h = int(screen_size[1] * 0.2)  #Lower 80% of the height
        for i in range(len(pattern)):
            row = []
            for j in range(side):
                #row contains tuples of the form (x,y)
                row.append((delta_w + j * (width//side), delta_h + i * (height//len(pattern))))
            points.append(row)
        return points
                
    @staticmethod
    def get_centres(screen):
        '''
        Extrapolates the centres of the circles from the square grid.
        '''
        pattern = Board.pattern
        centres = []
        points = Board.get_square_grid(screen)
        for i in range(len(pattern)):
            start_x = (len(points[i])//2)-i              #starting index of a circle in the ith row
            for j in range(pattern[i]):
                centres.append(points[i][start_x + 2*j]) #centre of the jth circle in the row
        return centres

    @staticmethod
    def get_radius(centres):
        '''
        Extrapolates ideal radius for the screen size and number of
        circles.
        '''
        p1,p2 = centres[0], centres[1]
        #Use distance formula
        return int(sqrt((p1[0]-p2[0])**2 + (p1[1] - p2[1])**2))//2
            
            
        

        
        
            
            
        
        
        
