class State:
    def __init__(self, stateslist=list()):
        self.states=stateslist
    '''
     not BoxAt(X)
     peut poser probleme si deux états sont possibles: at(A) & at(B)
     '''
    def update_backward(self, action):
        preconds = action.get_postconditions()
        postconds = action.get_postconditions()
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

    def remove_state(self, state):
        self.states.remove(state)

    def add_state(self, state):
        self.states.append(state)

    def get_states(self):
        return self.states

    def contains(self, state_to_check):
        for state in self.states:
            if state == state_to_check:
                return True
        return False

    def print(self):
        print(self.states)

