import pygame
import random
import time
from blackholestate import BlackHoleState
from BlackHoleFiles.drawblackhole import BHBoard

from boardentry import BoardEntry
def game_loop():
    pygame.init()  # Initialize pygame
    pygame.font.init()  # Initialize fonts
    screen_size = (1024, 576)  # Initialize screen_size
    screen = pygame.display.set_mode(screen_size)

    pygame.display.set_caption("Black Hole versus AI")
    screen.fill((0, 213, 242))

    board = BHBoard(screen)
    toss = random.randint(1, 4)

    if toss == 1:
        temp_state = board.state
        temp_state[0] = BoardEntry(1, 0)
        board.update_to_state(temp_state)
    done = False
    end_game = False
    cpu_player = 0
    tl = 1  # time limit for AI move
    msg = ''
    while not done:
        events = pygame.event.get()
        for event in events:
            if event.type == pygame.QUIT:
                done = True
                continue

            if event.type == pygame.MOUSEBUTTONDOWN:
                if end_game:
                    pass
                elif cpu_player == 0:
                    mpos = pygame.mouse.get_pos()
                    board.update_from_input(mpos)
                    cpu_player = 1
                    if sum([1 for key in range(len(board.state)) if board.state[key]]) == 20:
                        board.draw(screen)
                        pygame.display.flip()
                        end_game = True

        if end_game:
            delay(3)
            for key in range(len(board.state)):
                if board.state[key] is None:
                    for ney in BlackHoleState.N_MAP[key+1]:
                        board.circles[ney-1].update_circle((0, 0, 0), None)

            board.draw(screen)
            pygame.display.flip()

            red_score = 0
            blue_score = 0

            for key in range(len(board.state)):

                if board.state[key] is not None:
                    if board.state[key].player == 1:
                        if is_near_black_hole(key, board.state):
                            blue_score += board.state[key][0]
                    else:
                        if is_near_black_hole(key, board.state):
                            red_score += board.state[key][0]

            # print "red lost:", red_score
            # print "blue lost:", blue_score

            if red_score > blue_score:
                msg = "2nd player wins"
            elif red_score < blue_score:
                msg = "1st player wins"
            else:
                msg = "It's a tie"
            delay(2.5)
            done = True
            continue

        board.draw(screen)
        pygame.display.flip()

        if cpu_player == 1:
            mc = sum([1 for key in range(len(board.state)) if board.state[key]])
            bh_state = BlackHoleState(board.state)
            st = time.time()
            end = st + tl
            i = 1
            while time.time() < end:
                move = bh_state.next_move(i, termination_time=end)
                i += 1

            board.update_to_state(move.state)
            cpu_player = 0
            continue

            ##################################################################################
            # Use the following block of code if you want to let the AI kick in after
            # a certain number of moves
            # if sum([1 for key in board.state if board.state[key]]) >= 10:
            #     bh_state.state = board.state
            #     bh_node = BlackHoleNode(bh_state)
            #     bh_node.generate_children()
            #     st = time.time()
            #     i = 1
            #     move = bh_node
            #     while time.time() - st < tl:
            #         move = bh_node.next_move(recurse=i) or move
            #         i += 1
            #     if move:
            #         board.update_to_state(move.state_dict)
            #         player = 0
            #         continue
            # else:
            #     temp_state = board.state
            #     rand_key = 1
            #     while temp_state[rand_key] is not None:
            #         rand_key = random.randint(1, 21)
            #     move_count =sum([1 for key in board.state if board.state[key]])
            #     value = move_count//2 + 1
            #     play = move_count % 2
            #     move_tuple = (value, play)
            #     temp_state[rand_key] = move_tuple
            #     board.update_to_state(temp_state)
            #     player = 0
                ##################################################################################

        if sum([1 for key in range(len(board.state)) if board.state[key]]) == 20:
            end_game = True
            continue

        pygame.display.flip()
    pygame.quit()
    print msg
    quit()

def delay(t):
    st = time.time()
    while time.time() - st < t:
        pass
    return

def is_near_black_hole(index, state):
    for nbr in BlackHoleState.N_MAP[index+1]:
        if state[nbr-1] is None:
            return True
    return False

if __name__ == '__main__':
    game_loop()
