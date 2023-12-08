from sys import argv
from re import finditer

file_path = argv[1]

SYMBOL_PATTERN = r"[^\w\.\s]"
GEAR_PATTERN = r"\*"

def get_match_positions(pattern, rows) -> int:
    match_iterables = [finditer(pattern, row) for row in rows]
    return [[m.start() for m in matches] for matches in match_iterables]  

# Part 1
def check_positions(position_range: list[list[int]], symbol_positions: list[list[int]]) -> bool:
    x_start, x_end = position_range[0]
    y_start, y_end = position_range[1]

    symbol_positions_section = symbol_positions[y_start: y_end]
    intersection = lambda a, b: set(a) & set(b)

    return any([intersection(symbol_position, range(x_start, x_end)) for symbol_position in symbol_positions_section])

with open(file_path, "r") as file:
    total_value = 0
    lines = file.readlines()
    symbol_positions = get_match_positions(SYMBOL_PATTERN, lines)

    for i, line in enumerate(lines):
        y_start = max(i - 1, 0)
        y_end = min(i + 2, len(lines))
        number_spans = [m.span() for m in finditer(r"\d+", line)]

        for span in number_spans:
            x_start, x_end = span
            position_range = [
                [max(x_start - 1, 0), min(x_end + 1, len(line))],
                [y_start, y_end]
            ]
            if check_positions(position_range, symbol_positions):
                total_value += int(lines[i][x_start: x_end])
    
    print(f"Total value: {total_value}")


# Part 2
def get_gear_value(position: list[int], number_positions: list[list[tuple[int]]], lines: list[int]) -> int:
    x, y = position
    x_start = max(x - 1, 0)
    x_end = min(x + 2, len(lines[0]))
    y_start = max(y - 1, 0)
    y_end = min(y + 2, len(lines))

    number_span_section = number_positions[y_start: y_end]
    intersection = lambda a, b: set(a) & set(b)

    matching_numbers = []
    for i, number_spans in enumerate(number_span_section):
        current_y = y_start + i
        matching_numbers += [int(lines[current_y][span[0]: span[1]]) for span in number_spans if intersection(range(span[0], span[1]), range(x_start, x_end))]

    if len(matching_numbers) == 2:
        return matching_numbers[0] * matching_numbers[1]
    
    return 0

with open(file_path, "r") as file:
    total_value = 0
    lines = file.readlines()
    gear_positions = get_match_positions(GEAR_PATTERN, lines)
    number_spans = [[m.span() for m in finditer(r"\d+", line)] for line in lines]

    for y, gear_row in enumerate(gear_positions):
        gear_values = [get_gear_value([x, y], number_spans, lines) for x in gear_row]
        total_value += sum(gear_values)
    
    print(f"Total value: {total_value}")

        