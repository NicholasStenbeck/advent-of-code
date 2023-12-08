import sys
import time
from math import sqrt, floor, ceil

start = time.time()

def parse_rows(input):
    while line := input.readline().split():
        yield int("".join(line[1:]))

def get_roots(time, distance):
    root_1 = ceil(1/2 * (time - sqrt((time**2 - (4 * distance)))))
    root_2 = floor(1/2 * (time + sqrt((time**2 - (4 * distance)))))
    return [root_1, root_2]

def main():
    with open(sys.argv[1], "r") as file:
        time, distance = parse_rows(file)
        solution_limits = get_roots(time, distance)
        solutions_count = solution_limits[1] - solution_limits[0] + 1
        print(f"Score: {solutions_count}")


if __name__ == "__main__":
    main()
    print(f"Time: {(time.time() - start) * 1000} ms")