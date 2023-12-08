import sys
import time
from re import sub
from math import lcm

start = time.time()

def parse_rows(input):
    nodes = {}
    while line := input.readline().split(" = "):
        if not line[0]:
            break
        left, right = sub("[(),]", "", line[1]).split()
        nodes[line[0]] = {
            "value": line[0],
            "L": left,
            "R": right
        }
    return nodes

def count_steps(nodes, instructions, start="AAA"):
    current_node = nodes[start]
    
    instructions_length = len(instructions)
    steps = 0
    while instruction := instructions[steps % instructions_length]:
        steps += 1
        current_node = nodes[current_node[instruction]]
        if current_node["value"].endswith("Z"):
            return steps
            

def main():
    with open(sys.argv[1], "r") as file:
        instructions = file.readline().strip()
        file.readline()
        nodes = parse_rows(file)
        start_nodes = [node for node in nodes.values() if node["value"].endswith("A")]
        step_sets = [count_steps(nodes, instructions, node["value"]) for node in start_nodes]
        steps = lcm(*step_sets)
        print(f"Steps needed: {steps}")



if __name__ == "__main__":
    main()
    print(f"Time: {(time.time() - start) * 1000} ms")