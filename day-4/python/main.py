from sys import argv
from functools import reduce

file_path = argv[1]

# Part 1
with open(file_path, "r") as file:
    total_score = 0
    for line in file.readlines():
        card_title, card_data = line.split(":")
        winning_numbers, my_numbers = [card.split() for card in card_data.strip().split(" | ")]
        winning_numbers_count = len(set(winning_numbers) & set(my_numbers))

        if winning_numbers_count:
            total_score += 2 ** (winning_numbers_count - 1)
    
    print(f"Total score: {total_score}")

# Part 2

card_copies = {}

with open(file_path, "r") as file:
    lines = file.readlines()
    for card_number, line in enumerate(lines):
        card_title, card_data = line.split(":")
        winning_numbers, my_numbers = [card.split() for card in card_data.strip().split(" | ")]
        
        copies_of_current_card = card_copies.get(card_number, 0) + 1

        winning_numbers_count = len(set(winning_numbers) & set(my_numbers))
        bonus_card_numbers = range(card_number + 1, card_number + winning_numbers_count + 1)

        card_copies = card_copies | { i: card_copies.get(i, 0) + copies_of_current_card for i in bonus_card_numbers }

    total_cards = len(lines) + sum(card_copies.values())
    print(f"Total cards: {total_cards}")