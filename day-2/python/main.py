from sys import argv
from functools import reduce

file_path = argv[1]
red_limit, green_limit, blue_limit = argv[2:5]

limits = {
    "red": int(red_limit),
    "green": int(green_limit),
    "blue": int(blue_limit)
}

def is_game_possible(game_data: list[str]) -> bool:
    for hand in game_data:
        colors = [color.strip().split(' ') for color in hand.split(",")]
        game_failed = any([limits.get(name) < int(count) for count, name in colors])
        if game_failed:
            return False
    return True

def get_cube_power(game_data: list[str]) -> int:
    max_of_color_counts = {
        "red": 0,
        "green": 0,
        "blue": 0
    }
    for hand in game_data:
        colors = [color.strip().split(' ') for color in hand.split(",")]
        for color_count, color_name in colors:
            max_of_color_counts[color_name] = max(max_of_color_counts.get(color_name, 0), int(color_count))

    return reduce(lambda acc, color_score: acc * color_score, max_of_color_counts.values(), 1)
    
possible_games = []

with open(file_path, "r") as file:
    total_cube_power = 0
    for line in file.readlines():
        game_title, game_data = line.split(": ")
        game_data = [hand.strip() for hand in game_data.split(';')]
        total_cube_power += get_cube_power(game_data)
        if is_game_possible(game_data):
            game_number = int(game_title.split(" ")[1])
            possible_games.append(game_number)

result = sum(possible_games)
print(f"Result: {result}")
print(f"Total cube power: {total_cube_power}")
        