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
                actions_to_state[1].append(act)
                new_states.append(((copy.deepcopy(current_state)).update(act.get_preconditions()), actions_to_state[1]))

            for st in new_states:
                if is_satisfiying_state(st[0], init):
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
