from search import *
import string

class WordLadder(Problem):

    def __init__(self, initial, goal = None):
        super().__init__(initial, goal)

    def actions(self, state):
        """Return the actions that can be executed in the given
        state. The result would typically be a list, but if there are
        many actions, consider yielding them one at a time in an
        iterator, rather than building them all at once."""
        queue = []

        word_length = len(state)
        for idx in range(word_length):
            for alphabet in string.ascii_lowercase:
                if state[idx] != alphabet:
                    new_word = state[:idx] + alphabet + state[idx+1:]
                    if is_valid_word(new_word):
                        queue.append(new_word)
        return queue

    def result(self, state, action):
        """Return the state that results from executing the given
        action in the given state. The action must be one of
        self.actions(state)."""
        return action

    def goal_test(self, state):
        """Return True if the state is a goal. The default method compares the
        state to self.goal, as specified in the constructor. Override this
        method if checking against a single self.goal is not enough."""
        return state == self.goal

    def path_cost(self, c, state1, action, state2):
        """Return the cost of a solution path that arrives at state2 from
        state1 via action, assuming cost c to get up to state1. If the problem
        is such that the path doesn't matter, this function will only look at
        state2.  If the path does matter, it will consider c and maybe state1
        and action. The default method costs 1 for every step in the path."""
        return c + 1

    def value(self, state):
        """For optimization problems, each state has a value.  Hill-climbing
        and related algorithms try to maximize this value."""
        pass


WORDS = set(i.lower().strip() for i in open("words2.txt"))


def is_valid_word(word):
    return word in WORDS


def get_solution(word_ladder):
    try:
        if not is_valid_word(word_ladder.initial) or not is_valid_word(word_ladder.goal):
            raise ValueError
        solution = breadth_first_tree_search(word_ladder).solution()

        if solution != "":
            print("initial state:'{}'".format(str(word_ladder.initial)) + " -> " + "actions:{}".format(solution))
    
    except AttributeError:
        print("initial state:'{}'".format(str(word_ladder.initial)) + " -> unable to find any solution")

    except ValueError:
        print("invalid initial state: '{}'/ goal state: '{}'".format(str(word_ladder.initial),str(word_ladder.goal)))


def run():
    test_cases = [("ctrs", "cats"), ("cold", "warm"), ("best", "math")]
    for test in test_cases:
        word_ladder = WordLadder(test[0], test[1])
        get_solution(word_ladder=word_ladder)


if __name__ == "__main__":
    run()
