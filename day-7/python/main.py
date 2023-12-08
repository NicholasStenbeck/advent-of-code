import sys
import time
from functools import cmp_to_key

start = time.time()

def parse_rows(input):
    hands = []

    while line := input.readline().split():
        hands.append({ "cards": line[0], "bid": int(line[1]) })

    return hands

def get_card_set_type(card_set):
    unique_cards = set(list(card_set))
    if (joker_count := card_set.count("J")) == 5:
        return "five of a kind"
    
    card_counts = [card_set.count(card) for card in unique_cards if card != "J"]
    max_card_count = card_counts.pop(card_counts.index(max(card_counts)))

    match max_card_count + joker_count:
        case 5:
            return "five of a kind"
        case 4:
            return "four of a kind"
        case 3:
            if 2 in card_counts:
                return "full house"
            return "three of a kind"
        case 2:
            if 2 in card_counts:
                return "two pairs"
            return "one pair"
        case _:
            return "high card"
        
def compare_hands(hand_1, hand_2):
    CARD_TYPES = ["J", "2", "3", "4", "5", "6", "7", "8", "9", "T", "Q", "K", "A"]
    CARD_SET_TYPES = [
        "five of a kind",
        "four of a kind",
        "full house",
        "three of a kind",
        "two pairs",
        "one pair",
        "high card"
    ]

    cards_1 = hand_1["cards"]
    cards_2 = hand_2["cards"]
    
    card_set_1_value = CARD_SET_TYPES.index(get_card_set_type(cards_1))
    card_set_2_value = CARD_SET_TYPES.index(get_card_set_type(cards_2))
    if card_set_1_value > card_set_2_value:
        return 1
    if card_set_1_value < card_set_2_value:
        return -1

    return next((comp for c1, c2 in zip(cards_1, cards_2) if ((comp := CARD_TYPES.index(c2) - CARD_TYPES.index(c1)) != 0)), 0)

def main():
    with open(sys.argv[1], "r") as file:
        hands = parse_rows(file)
        placements = sorted(hands, key=cmp_to_key(compare_hands), reverse=True)
        scores = [placement["bid"] * (i+1) for i, placement in enumerate(placements)]
        print(f"Score: {sum(scores)}")
        


if __name__ == "__main__":
    main()
    print(f"Time: {(time.time() - start) * 1000} ms")