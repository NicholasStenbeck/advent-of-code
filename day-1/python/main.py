from sys import argv
from re import findall, IGNORECASE
from functools import reduce

file_path = argv[1]

spelled_number_to_digit = {
    "one": "1",
    "two": "2",
    "three": "3",
    "four": "4",
    "five": "5",
    "six": "6",
    "seven": "7",
    "eight": "8",
    "nine": "9"
}

def get_line_value(line: str) -> int:
    # Use lookahead with a contained capture group to find matches without
    # consuming the characters (example "oneight" should result in "one" and "eight")
    digits_pattern = r"(?=(\d|(one)|(two)|(three)|(four)|(five)|(six)|(seven)|(eight)|(nine)))"
    digits = findall(digits_pattern, line, flags=IGNORECASE)

    if len(digits) == 0:
        return 0

    if digits[0][0].isdigit():
        first_digit = digits[0][0]
    else:
        first_digit = spelled_number_to_digit[digits[0][0].lower()]

    if digits[-1][0].isdigit():
        last_digit = digits[-1][0]
    else:
        last_digit = spelled_number_to_digit[digits[-1][0].lower()]
    
    return int(f"{first_digit}{last_digit}")

    



with open(file_path, "r") as file:
    calibration_value = reduce(lambda acc, line: acc + get_line_value(line), file.readlines(), 0)

with open("output.txt", "w") as file:
    file.write(f"{calibration_value}\n")
    print("Wrote output to output.txt")