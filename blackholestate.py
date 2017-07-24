from basegamestate import BaseGameState
from boardentry import BoardEntry

class BlackHoleState(BaseGameState):

    # Map of neighbours
    N_MAP = {
        1: (2, 3),
        2: (1, 3, 4, 5),
        3: (1, 2, 5, 6),
        4: (2, 5, 7, 8),
        5: (2, 3, 4, 6, 8, 9),
        6: (3, 5, 9, 10),
        7: (4, 8, 11, 12),
        8: (4, 5, 7, 9, 12, 13),
        9: (5, 6, 8, 10, 13, 14),
        10: (6, 9, 14, 15),
        11: (7, 12, 16, 17),
        12: (7, 8, 11, 13, 17, 18),
        13: (8, 9, 12, 14, 18, 19),
        14: (9, 10, 13, 15, 19, 20),
        15: (10, 14, 20, 21),
        16: (11, 17),
        17: (11, 12, 16, 18),
        18: (17, 12, 13, 19),
        19: (18, 13, 14, 20),
        20: (19, 14, 15, 21),
        21: (20, 15)
    }

    def __init__(self, state_list, parent=None, children=None):
        self.state_list = state_list
        agg_fn = (min, max)[sum([1 for index in range(len(self.state_list)) if self.state_list[index]]) % 2]
        super(BlackHoleState, self).__init__(parent=parent, agg_fn=agg_fn, children=children)
        self.string_rep = ''
        self._static_score = None

    @property
    def children(self):
        if self._children:
            return self._children


        moves_so_far = sum([1 for index in range(len(self.state_list)) if self.state_list[index]])

        if moves_so_far == 20:
            self._children = []
            return self._children

        move_tuple = BoardEntry(moves_so_far//2 + 1, moves_so_far % 2)

        temp_state = list(self.state_list)

        for index in range(len(self.state_list)):
            if self.state_list[index] is None:
                temp_state[index] = move_tuple
                child = BlackHoleState(temp_state)
                self._children.append(child)
                temp_state = list(self.state_list)

        return self._children

    @property
    def static_score(self):
        if self._static_score:
            return self._static_score

        sum_exposed_first_player = 0
        sum_exposed_second_player = 0

        for index in range (len(self.state_list)):
            entry = self.state_list[index]
            if entry is not None:

                if entry.player == 0:
                    for nbr in self.N_MAP[index+1]:
                        if self.state_list[nbr-1] is None:
                            sum_exposed_first_player += entry.value
                            break

                if entry.player == 1:
                    for nbr in self.N_MAP[index+1]:
                        if self.state_list[nbr-1] is None:
                            sum_exposed_second_player += entry.value
                            break

        self._static_score = sum_exposed_first_player - sum_exposed_second_player
        return self._static_score

    @property
    def state(self):
        return self.state_list

    def __str__(self):
        if self.string_rep:
            return self.string_rep
        for ind, tup in enumerate(self.state_list):
            self.string_rep += str(ind+1) + ': ' + str(tup).lstrip('BoardEntry') + '\n'
        return self.string_rep

if __name__ == "__main__":
    pass
