#! /bin/env python3

import sys

from strips_parser import file_parser
from state import State
from strips_planner import reverse_decision

#Init/Goal: List( (etat, [literals]) ) ex: [(At, [X]), (Blabla, [U, V])]
#Actions: List ( ActionClass )

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: ./strips FILE.TXT")

    with open(sys.argv[1]) as f:
        init, goal, actions = file_parser(f)

    print("Initial state:")
    print(init)
    print("\nGoal state:")
    print(goal)
    print("\nActions:")
    for a in actions:
        a.print()
        print()

    current_state = State(goal)
    res = reverse_decision(current_state, actions, init, goal)
    #print(res)
    for i in res[1]:
        i.print_name()
    #res[0].print()
    exit(0)
