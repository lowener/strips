#! /bin/env python3

import sys
import queue
import copy
import itertools as it


#List( (etat, [literals]) ) ex: [(At, [X]), (Blabla, [U, V])]
init = []
goal = []

#List ( ActionClass )
actions = []

current_state = []

class State:
    def __init__(self, stateslist=list()):
        self.states=stateslist
    '''
     not BoxAt(X)
     peut poser probleme si deux états sont possibles: at(A) & at(B)
     '''
    def update(self, state):
        new_states = self.states
        new_states += (st for st in state)
        print(new_states)
        for st in state:
            if st[0].startswith('not'):
                st[0] = ' '.join(st[0].split(' ')[1:])
                if self.states.contains(st):
                    new_states.remove(st)

        self.states = new_states
        return self

        '''
        if state[0].startswith('not'):
            state[0] = ' '.join(state[0].split(' ')[1:])
            if self.states.get(state[0]) == state[1]:
                self.states.pop(state[0])
        else:
            self.states[state[0]] = state[1]
        '''

    def get(self, stateName):
        return self.states.get(stateName)

    def contains(self, state_to_check):
        for state in self.states:
            if state[0] == state_to_check[0] and state[1] == state_to_check[1]:
                return True
        return False

    def print(self):
        print(self.states)

'''
    Represents an Action
    It has:
        - a name
        - a list of literals
        - a list of preconditions (same form as init list)
        - a list of postconditions (same form as init list)
'''
class Action:
    def __init__(self, name, literals):
        self.preconditions = []
        self.postconditions = []
        self.name = name.strip('_')
        self.literals = literals

    def apply_backward(self, state, args):
        # Check that all post-conditions are validated
        for i in self.postconditions:
            if not state.get(i):
                return False
        # Do a step backward
        for i in self.preconditions:
            state.update(i)
        return True

    def get_literals(self):
        return self.literals

    def apply_literals(self, literals):
        new_action = Action(self.name, self.literals)
        for precond in self.preconditions:
            new_lit = []
            for lit in precond[1]:
                try:
                    idx = self.literals.index(lit)
                    new_lit.append(literals[idx])
                except ValueError:
                    new_lit.append(lit)
            new_action.add_preconditions((precond[0], new_lit))

        for postcond in self.postconditions:
            new_lit = []
            for lit in postcond[1]:
                try:
                    idx = self.literals.index(lit)
                    new_lit.append(literals[idx])
                except ValueError:
                    new_lit.append(lit)
            new_action.add_postconditions((postcond[0], new_lit))

        return new_action

    def add_preconditions(self, preconds):
        self.preconditions.append(preconds)

    def add_postconditions(self, postconds):
        self.postconditions.append(postconds)

    def get_preconditions(self):
        return self.preconditions

    def get_postconditions(self):
        return self.postconditions

    def print(self):
        print(self.name, self.literals)
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

def is_compatible(cur_state, conditions):
    return True


def reverse_decision(current_state, goal, actions):
    state_queue = queue.Queue()
    state_queue.put((current_state, []))

    while True:
        try:
            #actions_to_state = (curr_state, [actions_leading_to_state])
            actions_to_state = state_queue.get(False)
            current_state = actions_to_state[0]
            good_actions = actions_that_satisfy_state_backward(actions, current_state)
            new_states = []
            for act in good_actions:
                actions_to_state[1].append(act)
                new_states.append(((copy.deepcopy(current_state)).update(act.get_preconditions()), actions_to_state[1]))

            for st in new_states:
                if is_satisfiying_state(st[0], goal):
                    return st

            for st in new_states:
                state_queue.put(st)

        except queue.Empty:
            break

def get_literals():
    res=[]
    global init
    global goal
    for i in init:
        res += (x for x in i[1])
    for i in goal:
        res += (x for x in i[1])
    return res

def is_satisfiying_state(curr_state, goal):
    for state in goal:
        if not curr_state.contains(state):
            return False
    return True

def actions_that_satisfy_state_backward(listAction, state):
    res=[]
    for a in listAction:
        for i in it.permutations(get_literals(), r=len(a.get_literals())):
            new_action = a.apply_literals(list(i))
            if is_satisfiying_state(state, new_action.get_postconditions()):
                res.append(new_action)

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

    #for i in goal:
    #    current_state[i[0]] = i[1]
    current_state = State(goal)
    #print(current_state)
    #my_actions = actions_that_satisfy_state_backward(actions, current_state)
    #print("My actions: ", my_actions)
    #current_state.clear()
    #for i in my_actions:
    #    current_state[i[0]] = i[1]
    #current_state = State(current_state)
    res = reverse_decision(current_state, init, actions)
    print(res)

    '''
    # Start the main loop
    for i in init:  # loop over all the goals (if we chain backward, inits are goals
        listPossibilities = []
        while not check_win(current_state, [i]):  # Check if we satisfy the condition
            for a in actions:
                for arg in get_variables():  # Generate an action of each type
                    listPossibilities.append((a, arg))
    '''
    print(init)
    exit(0)
