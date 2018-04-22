#! /bin/env python3

import sys


init = []
goal = []
actions = []
current_state=dict()

class State:
    def __init__(self, stateslist=dict()):
        self.states=stateslist
    '''
     not BoxAt(X)
     peut poser probleme si deux états sont possibles: at(A) & at(B)
     '''
    def update(self, state):
        if state[0].startswith('not'):
            state[0] = ' '.join(state[0].split(' ')[1:])
            if self.states.get(state[0]) == state[1]:
                self.states.pop(state[0])
        else:
            self.states[state[0]] = state[1]

    def get(self, stateName):
        return self.states.get(stateName)

class Action:
    def __init__(self, name, params):
        self.preconditions = []
        self.postconditions = []
        self.name = name.strip('_')
        self.params = params

    def apply_backward(self, state, args):
        # Check that all post-conditions are validated
        for i in self.postconditions:
            if not state.get(i):
                return False
        # Do a step backward
        for i in self.preconditions:
            state.update(i)
        return True

    def add_preconditions(self, preconds):
        self.preconditions.append(preconds)

    def add_postconditions(self, postconds):
        self.postconditions.append(postconds)

    def get_preconditions(self):
        return self.preconditions

    def get_postconditions(self):
        return self.postconditions

    def print(self):
        print(self.name, self.params)
        print(self.preconditions)
        print(self.postconditions)

# fct_parser("a(b,c, d,  e  )")
def fct_parser(line):
    name = line[:line.find('(')]
    rest_of_the_line = line[line.find(')') + 1:]
    rest_of_the_line = rest_of_the_line.strip(', ')
    line=line[line.find('(') + 1:line.find(')')]
    args=line.split(',')
    args = [a.strip(' ') for a in args]
    return name, args, rest_of_the_line

def parse_action(f):
    func = f.readline().split()
    if not func:
        return None
    if func[0] == "//":
        func = f.readline().split()
    func_name, args, new_line = fct_parser(' '.join(func))

    a = Action(func_name, args)

    for i in range(0, 2):
        conditions = f.readline().split()
        conditions_cpy = conditions[1:]
        new_line = ' '.join(conditions_cpy)
        while len(new_line):
            name, args, new_line = fct_parser(new_line)
            (a.add_preconditions((name, args)) if conditions[0] == 'Preconditions:'
                    else a.add_postconditions((name, args)))
    return a

def file_parser(f):
    for x in f:
        words = x.split()
        if not len(words):
            continue
        if len(words) > 1 and words[1] == "state:":
            words_cpy = words[2:]
            new_line = ' '.join(words_cpy)
            while len(new_line):
                name, args, new_line = fct_parser(new_line)
                (init.append((name, args)) if words[0] == "Initial"
                        else goal.append((name, args)))
        elif words[0] == 'Actions:':
            while True:
                action = parse_action(f)
                if action is None:
                    break
                actions.append(action)
                f.readline()
        else:
            raise ValueError("Not a valid keyword: {}".format(words))

def check_win(curr_state, goals):
    for i in goals:
        if not curr_state.__contains__(i[0]):
            return False
    return True

def get_variables():
    res=[]
    global init
    global goal
    for i in init:
        res.append(i[1:])
    for i in goal:
        res.append(i[1:])
    return res


def actions_that_satisfy_state(listAction, state):
    res=[]
    for a in listAction:
        for pc in a.get_postconditions():
            if not (pc[0].startswith('not') and state.get(pc[0].split(' ')[1])) or (not state.get(pc[0])):
                break
            res.append(a)

    return res

def apply_step_backwards(state, action, args):
    action.apply_backward(state)


if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: ./strips FILE.TXT")

    with open(sys.argv[1]) as f:
        file_parser(f)

    print("Initial state:")
    print(init)
    print("\nGoal state:")
    print(goal)
    print("\nActions:")
    for a in actions:
        a.print()
        print()

    for i in goal:
        current_state[i[0]] = i[1]
    my_actions = actions_that_satisfy_state(actions, current_state)
    current_state.clear()
    for i in my_actions:
        current_state[i[0]] = i[1]
    current_state = State(current_state)

    # Start the main loop
    for i in init:  # loop over all the goals (if we chain backward, inits are goals
        listPossibilities = []
        while not check_win(current_state, [i]):  # Check if we satisfy the condition
            for a in actions:
                for arg in get_variables():  # Generate an action of each type
                    listPossibilities.append((a, arg))



    print(init)
    exit(0)
