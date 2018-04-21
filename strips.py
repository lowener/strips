import sys


# fct_parser("a(b,c, d,  e  )")
def fct_parser(line):
    name = line[:line.find('(')]
    rest_of_the_line = line[line.find(')') + 1:]
    rest_of_the_line = rest_of_the_line.strip(', ')
    line=line[line.find('(') + 1:line.find(')')]
    args=line.split(',')
    args = [a.strip(' ') for a in args]
    return name, args, rest_of_the_line

def parser(f):
    l = f.readline()
    words = l.split()
    init_state=[]
    if words[0] == "Initial" and words[1] == "state:":
        words = words[2:]
        new_line = ' '.join(words)
        while len(new_line) :
            name, args, new_line = fct_parser(new_line)
            init_state.append((name, args))

    return init_state

if __name__ == "__main__":
    if (len(sys.argv) != 2):
        print("Usage: ./strips FILE.TXT")
        exit(1)

    with open(sys.argv[1]) as f:
        print(parser(f))
    exit(0)
