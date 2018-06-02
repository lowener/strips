from state import State
import queue
import copy
import itertools as it

def reverse_decision(current_state, actions, init, goal):
    state_queue = queue.Queue()
    state_queue.put((current_state, []))

    while True:
        try:
            #actions_to_state = (curr_state, [actions_leading_to_state])
            actions_to_state = state_queue.get(False)
            current_state = actions_to_state[0]
            good_actions = actions_that_satisfy_state_backward(actions, current_state, init, goal)
            new_states = []
            for act in good_actions:
                chain_ac = copy.deepcopy(actions_to_state[1])
                chain_ac.insert(0, act)

                new_st = State(list(act.generate_state_backward(current_state)))
                new_st.print()
                new_states.append((new_st, chain_ac))

            for st in new_states:
                for ac in st[1]:
                    ac.print_name()
                st[0].print()

                if is_satisfiying_state(st[0], init):
                    return st

            for st in new_states:
                state_queue.put(st)

        except queue.Empty:
            break

def forward_decision(current_state, actions, init, goal):
    state_queue = queue.Queue()
    state_queue.put((current_state, []))

    while True:
        try:
            actions_to_state = state_queue.get(False)
            current_state = actions_to_state[0]

            print("-------------------------------")
            for a in actions_to_state[1]:
                a.print_name()
            print("-------------------------------")

            good_actions = actions_that_satisfy_state_forward(actions, current_state, init, goal)
            new_states = []
            for act in good_actions:
                chain_ac = copy.deepcopy(actions_to_state[1])
                chain_ac.append(act)
                new_st = act.generate_state_forward(current_state)
                new_states.append((new_st, chain_ac))

            for st in new_states:
                if is_satisfiying_state(st[0], goal):
                    return st

            for st in new_states:
                state_queue.put(st)

        except queue.Empty:
            break

def get_literals(init, goal):
    res=[]
    for i in init:
        res += (x for x in i[1])
    for i in goal:
        res += (x for x in i[1])
    return res

def is_satisfiying_state(curr_state, goal):
    for state in goal:
        if state[0].startswith('not'):
            cp_state = list(state)
            cp_state[0] = ' '.join(state[0].split(' ')[1:])
            if curr_state.contains(tuple(cp_state)):
                return False
        else:
            if not curr_state.contains(state):
                return False
    return True

def actions_that_satisfy_state_backward(listAction, state, init, goal):
    res=[]
    for a in listAction:
        for i in it.permutations(get_literals(init, goal), r=len(a.get_literals())):
            new_action = a.apply_literals(list(i))
            if is_satisfiying_state(state, new_action.get_postconditions()):
                res.append(new_action)

    return res

def actions_that_satisfy_state_forward(listAction, state, init, goal):
    res=[]
    for a in listAction:
        for i in it.permutations(get_literals(init, goal), r=len(a.get_literals())):
            new_action = a.apply_literals(list(i))
            if is_satisfiying_state(state, new_action.get_preconditions()):
                res.append(new_action)

    return res
