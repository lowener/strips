import sys


# fct_parser("a(b,c, d,  e  )")
def fct_parser(line):
    name = line[:line.find('(')]
    rest_of_the_line = line[line.find(')') + 1:]
    line=line[line.find('(') + 1:line.find(')')]
    args=line.split(',')
    args = [a.strip(' ') for a in args]
    return name, args, line

def parser(f):
    l = f.readline()
    words = l.split()
    init_state=[]
    if words[0] == "Initial" and words[1] == "state:":
        words = words[2:]
        for i in words:
            init_state.append((i[:i.find('(')], i[(i.find('(')+1):(i.find(')'))]))

            ''' Make clean function
        init_state.clear()
        new_line = ' '.join(words)
        while len(new_line) :
            name, args, new_line = fct_parser(new_line)
        init_state.append((name, args))'''

    return init_state

if __name__ == "__main__":
    if (len(sys.argv) != 2):
        print("Usage: ./strips FILE.TXT")
        exit(1)

    with open(sys.argv[1]) as f:
        print(parser(f))
    exit(0)
