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
        #self.real_literals = literals

    def get_literals(self):
        return self.literals

    def apply_literals(self, literals):
        new_action = Action(self.name, literals)
        #new_action.real_literals = literals
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

    def generate_state_backward(self, state):
        for st in state.get_states():
            if st[0].startswith('not'):
                st[0] = ' '.join(st[0].split(' ')[1:])

            found = False
            for postcond in self.postconditions:
                if postcond[0] == st[0]:
                    found = True

            if not found:
                yield st

        for st in self.preconditions:
            yield st

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

    def print_name(self):
        print("{}({})".format(self.name, ', '.join(x for x in self.literals)))
