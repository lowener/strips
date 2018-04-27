from action import Action

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
    init = []
    goal = []
    actions = []

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
    return init, goal, actions
