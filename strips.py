import sys


init = []
goal = []
actions = []

class Action():
    def __init__(self, name, params):
        self.preconditions = []
        self.postconditions = []
        self.name = name
        self.params = params

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

if __name__ == "__main__":
    if (len(sys.argv) != 2):
        print("Usage: ./strips FILE.TXT")
        exit(1)

    with open(sys.argv[1]) as f:
        file_parser(f)

    print(init)
    print(goal)
    for a in actions:
        a.print()
        print()
    exit(0)
