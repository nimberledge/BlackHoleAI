import abc
from abc import abstractmethod
import time
import random


class BaseGameState(object):
    __metaclass__ = abc.ABCMeta

    def __init__(self, parent=None, agg_fn=max, children=None):
        assert agg_fn in (max, min)
        self.__parent = parent
        if children:
            self._children = children
        else:
            self._children = []
        self.state_scores_cache = {}
        self.agg_fn = agg_fn

    @property
    def parent(self):
        """
        :return: the parent game state of the current state
        """
        return self.__parent

    @property
    @abstractmethod
    def children(self):
        """
        :return: list of game states immediately reachable from current state
        """
        pass

    @property
    @abstractmethod
    def static_score(self):
        """
        :return: evaluation function - customize to your game
        """
        raise NotImplementedError

    @abstractmethod
    def __str__(self):
        """
        :return: string value of self
        """
        raise NotImplementedError

    def dynamic_score(self, depth, termination_time=None):
        """
        :param depth: level of recursive depth to compute score
        :param termination_time: time (as an absolute system time) passed to halt execution. optional parameter
        :return: normalized minimax score of a state
        """
        assert depth >= 0
        if depth in self.state_scores_cache:
            return self.state_scores_cache[depth]

        if depth == 0:
            score = self.static_score
            self.state_scores_cache[depth] = score
            return score

        if not self.children:
            return self.static_score
            
        if termination_time:
            if time.time() > termination_time:
                return self.state_scores_cache[depth-1]

        children_scores = []
        for child in self.children:
            if termination_time and time.time() >= termination_time:
                return self.state_scores_cache[depth-1]
                # continue

            children_scores.append(child.dynamic_score(depth - 1, termination_time=termination_time))

        score = self.agg_fn(children_scores)
        self.state_scores_cache[depth] = score
        return self.state_scores_cache[depth]

    def next_move(self, depth, termination_time=None):
        """
        :param depth: level of recursive depth to compute move
        :param termination_time: time (as an absolute system time) passed to halt execution. optional parameter
        :return: suggested child of state to play
        """
        score = self.dynamic_score(depth, termination_time=termination_time)

        if not self.children:
            return None

        for child in self.children:

            if child.dynamic_score(depth-1, termination_time=termination_time) == score:
                return child

        # If it doesn't match any of its children
        return self.children[random.randint(0, len(self.children)-1)]


if __name__ == "__main__":
    print 'Hellow, world! This is me using Python 2'
