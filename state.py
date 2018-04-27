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

