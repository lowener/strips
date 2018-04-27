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
