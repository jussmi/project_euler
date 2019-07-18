from collections import Counter
import time

class PokerHand(object):
    def __init__(self, hand_str: str):
        """Expects a string of 5 cards separated by a space.
        i.e. '8C TS KC 9H 4S'"""
        self.FACE_CARD_DICT = {
            'A': 14,
            'K': 13,
            'Q': 12,
            'J': 11,
            'T': 10
        }
        self.hand_str = hand_str.strip()
        self.suits = self.suits()
        self.numbers = self.numbers()
        self.groups = self.groups()
        
    def suits(self):
        suits = self.hand_str[1::3]
        return set(suits)
    
    def numbers(self):
        numbers = self.hand_str[::3]
        converted_numbers = [int(self.FACE_CARD_DICT.get(number, number)) for number in numbers]
        return set(converted_numbers)
    
    def groups(self):
        if len(self.numbers) == 5:
            return False
        else:
            cntr = Counter(self.hand_str[::3])
            groups = {int(self.FACE_CARD_DICT.get(card, card)): count for card, count in cntr.items()}
            return groups
    
    @property
    def counts(self):
        if self.groups:
            counts = {}
            for key, value in self.groups.items():
                counts.setdefault(value, set()).add(key)
            return counts
        else:
            return False
        
    @property
    def is_flush(self):
        return len(self.suits) == 1
    
    @property
    def is_straight(self):
        five_different = len(self.numbers) == 5
        sequential = max(self.numbers) - min(self.numbers) == 4
        return five_different and sequential
    
    @property
    def hand_rank(self):
        """Gives a hand rank, high card within rank, and high card outside of rank."""
        if self.is_straight and self.is_flush and sum(self.numbers) == 60:
            return 10, 14, None
        elif self.is_straight and self.is_flush:
            return 9, max(self.numbers), None
        elif self.is_flush:
            return 6, max(self.numbers), None
        elif self.is_straight:
            return 5, max(self.numbers), None
        else:
            if self.groups:
                if self.counts.get(4, False):
                    card = self.counts.get(4)
                    high_card = self.counts.get(1)
                    return 8, card.pop(), high_card.pop()
                elif self.counts.get(3, False) and self.counts.get(2, False):
                    three = self.counts.get(3).pop()
                    two = self.counts.get(2).pop()
                    return 7, three, two
                elif self.counts.get(3, False):
                    three_of_a_kind_card = self.counts.get(3).pop()
                    high_card = max(self.counts.get(1))
                    return 4, three_of_a_kind_card, high_card
                elif len(self.counts.get(2, False)) == 2:
                    pairs = self.counts.get(2)
                    return 3, max(pairs), min(pairs)
                elif len(self.counts.get(2, False)) == 1:
                    pair = self.counts.get(2).pop()
                    return 2, pair, max(self.counts.get(1))
            else:
                high_card = max(self.numbers)
                self.numbers.remove(high_card)
                next_high_card = max(self.numbers)
                return 1, high_card, next_high_card

def heads_up(player_1_hand: PokerHand, player_2_hand: PokerHand) -> int:
    """Returns 1 for a player 1 victory and 2 for a player 2 victory"""
    hand_rank_1 = player_1_hand.hand_rank[0]
    hand_rank_2 = player_2_hand.hand_rank[0]
    
    if hand_rank_1 == hand_rank_2:
        first_card_comp_1 = player_1_hand.hand_rank[1]
        first_card_comp_2 = player_2_hand.hand_rank[1]
        if first_card_comp_1 == first_card_comp_2:
            if player_1_hand.hand_rank[2] > player_2_hand.hand_rank[2]:
                return 1
            else:
                return 2
        elif first_card_comp_1 > first_card_comp_2:
            return 1
        else:
            return 2
    elif hand_rank_1 > hand_rank_2:
        return 1
    else:
        return 2

if __name__ == "__main__":
    with open('./poker.txt', 'r') as raw_hands:
        poker_hands = raw_hands.readlines()

    start_time = time.process_time()
    
    win_counter = Counter(
        [heads_up(PokerHand(hands[:14]), PokerHand(hands[15:-1])) for hands in poker_hands]
    )
    
    print(win_counter)
    print(f"Elapsed time: {time.process_time() - start_time}" )