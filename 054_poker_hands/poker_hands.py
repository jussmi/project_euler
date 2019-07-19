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
        self.hand_str = hand_str
        self.suits = self.suits()
        self.numbers = self.numbers()
        self.groups = self.groups()
        
    def suits(self):
        # the double colon indicates every third item
        suits = self.hand_str[1::3]
        return list(set(suits))
    
    def numbers(self):
        numbers = self.hand_str[::3]
        converted_numbers = [int(self.FACE_CARD_DICT.get(number, number)) for number in numbers]
        return list(set(converted_numbers))
    
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
        # check for a straight flush using cards sums and properties
        if self.is_straight and self.is_flush and sum(self.numbers) == 60:
            return 10, 14, None
        # check for straight_flush
        elif self.is_straight and self.is_flush:
            return 9, max(self.numbers), None
        elif self.is_flush:
            return 6, max(self.numbers), None
        elif self.is_straight:
            return 5, max(self.numbers), None
        else:
            # we only enter the next cadence if there are pairings within the group
            if self.groups:
                # 4 of a kind if there is a group of 4
                if self.counts.get(4, False):
                    card = self.counts.get(4)
                    high_card = self.counts.get(1)
                    return 8, card.pop(), high_card.pop()
                # full house if you have a group of 3 and of 2
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
                junk_numbers = self.numbers
                high_card = max(self.numbers)
                junk_numbers.remove(high_card)
                next_high_card = max(junk_numbers)
                return 1, high_card, next_high_card

def heads_up(player_1_hand: PokerHand, player_2_hand: PokerHand) -> int:
    """Returns 1 for a player 1 victory and 2 for a player 2 victory"""
    p1_rank1, p1_rank2, p1_rank3 = player_1_hand.hand_rank
    p2_rank1, p2_rank2, p2_rank3 = player_2_hand.hand_rank
    
    if p1_rank1 > p2_rank1:
        winner = 1
    elif p2_rank1 > p1_rank1:
        winner = 2
    else:
        if p1_rank2 > p2_rank2:
            winner = 1
        elif p2_rank2 > p1_rank2:
            winner = 2
        else:
            if p1_rank3 > p2_rank3:
                winner = 1
            elif p2_rank3 > p1_rank3:
                winner = 2
            else:
                winner = 0
    return winner

if __name__ == "__main__":
    with open('./poker.txt', 'r') as raw_hands:
        poker_hands = raw_hands.readlines()

    start_time = time.process_time()
    
    win_counter = Counter(
        [heads_up(PokerHand(hands[:14]), PokerHand(hands[15:-1])) for hands in poker_hands]
    )
    
    print(win_counter)
    print(f"Elapsed time: {time.process_time() - start_time}" )