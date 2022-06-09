from search import *
import string


class Flight:
    def __init__(self, start_city, start_time, end_city, end_time):
        self.start_city = start_city
        self.start_time = start_time
        2
        self.end_city = end_city
        self.end_time = end_time

    def __str__(self):
        return str((self.start_city, self.start_time)) + "->" + str((self.end_city, self.end_time))

    def matches(self, city_and_time):
        city, time = city_and_time
        return (self.start_city == city and self.start_time >= time)
    
    __repr__ = __str__


flightDB = [Flight("Rome", 1, "Paris", 4),
Flight("Rome", 3, "Madrid", 5),
Flight("Rome", 5, "Istanbul", 10),
Flight("Paris", 2, "London", 4),
Flight("Paris", 5, "Oslo", 7),
Flight("Paris", 5, "Istanbul", 9),
Flight("Madrid", 7, "Rabat", 10),
Flight("Madrid", 8, "London", 10),
Flight("Istanbul", 10, "Constantinople", 10)]


class FlightItinerary(Problem):
    def __init__(self, initial, goal=None):
        """The constructor specifies the initial state, and possibly a goal
        state, if there is a unique goal.  Your subclass's constructor can add
        other arguments."""
        self.initial = initial; self.goal = goal

    def actions(self, state):
        """Return the actions that can be executed in the given
        state. The result would typically be a list, but if there are
        many actions, consider yielding them one at a time in an
        iterator, rather than building them all at once."""
        queue = []
        for i in range(len(flightDB)):
            if flightDB[i].matches(state):
                queue.append((flightDB[i].end_city, flightDB[i].end_time))
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
        return (state[0] == self.goal[0] and state[1] <= self.goal[1])

    def path_cost(self, c, state1, action, state2):
        """Return the cost of a solution path that arrives at state2 from
        state1 via action, assuming cost c to get up to state1. If the problem
        is such that the path doesn't matter, this function will only look at
        state2.  If the path does matter, it will consider c and maybe state1
        and action. The default method costs 1 for every step in the path."""
        return state2[1] - state1[1] + c

    def value(self, state):
        """For optimization problems, each state has a value.  Hill-climbing
        and related algorithms try to maximize this value."""
        pass


def find_itinerary(start_city, start_time, end_city, deadline):
    flight_itinerary = FlightItinerary((start_city, start_time), (end_city, deadline))
    try:
        plan = depth_first_graph_search(flight_itinerary).solution()
        next_city, next_time = plan[0]
        for f in range(len(flightDB)):
            if flightDB[f].end_time == next_time and flightDB[f].end_city == next_city and flightDB[f].start_city == start_city and flightDB[f].start_time >= start_time:
                plan.insert(0, (flightDB[f].start_city, flightDB[f].start_time))
    except AttributeError:
        return "Unable to find any possible plan."    
    return plan


def find_shortest_itinerary(start_city, end_city):
    deadline = 1
    start_time = 1
    plan = find_itinerary(start_city, start_time, end_city, deadline)
    while plan == "Unable to find any possible plan.":
        deadline += 1 
        plan = find_itinerary(start_city, start_time, end_city, deadline)
    return plan


def find_shortest_itinerary_challenge(start_city, end_city):
    valid_deadlines = set()
    start_time = 1
    for f in range(len(flightDB)):
        if flightDB[f].end_city == end_city:
            valid_deadlines.add(flightDB[f].end_time)

    valid_deadlines = sorted(valid_deadlines)
    
    for idx in range(len(valid_deadlines)):
        plan = find_itinerary(start_city, start_time, end_city, valid_deadlines[idx])
        if plan == "Unable to find any possible plan.":
            continue
        else:
            return plan

    return "Unable to find any possible plan."


def run():
    print("Implementation of find_itinerary():")
    print(find_itinerary("Rome", 1, "Istanbul", 10))

    print("Implementation of find_shortest_itinerary():")
    print(find_shortest_itinerary("Rome", "Istanbul"))

    print("Implementation of find_shortest_itinerary_challenge():")
    print(find_shortest_itinerary_challenge("Rome", "Istanbul"))
    return


if __name__ == "__main__":
    run()