import pytest
import poker_hands as ph

@pytest.fixture(scope="function")
def royal_flush():
    return ph.PokerHand("TC JC QC KC AC")

@pytest.fixture(scope="function")
def straight_flush():
    return ph.PokerHand("8H 6H 7H 9H TH")

@pytest.fixture(scope="function")
def four_of_a_kind():
    return ph.PokerHand("JH JC JS JD 8H")

@pytest.fixture(scope="function")
def full_house():
    return ph.PokerHand("6H 6C 6S 9D 9H")

@pytest.fixture(scope="function")
def straight():
    return ph.PokerHand("2H 3C 4S 5D 6H")

@pytest.fixture(scope="function")
def flush():
    return ph.PokerHand("8H 6H 2H 3H TH")

@pytest.fixture(scope="function")
def three_of_a_kind():
    return ph.PokerHand("TH TS TD JC 9H")

@pytest.fixture(scope="function")
def two_pair():
    return ph.PokerHand("QH QS TC TD 7H")

@pytest.fixture(scope="function")
def one_pair():
    return ph.PokerHand("QH JS TC TD 7H")

@pytest.fixture(scope="function")
def junk_hand():
    return ph.PokerHand("2H 4C 6S 9D JH")

def test_is_straight(royal_flush, straight_flush, junk_hand):
    assert royal_flush.is_straight
    assert straight_flush.is_straight
    assert not junk_hand.is_straight
    
def test_is_flush(royal_flush, straight_flush, junk_hand):
    assert royal_flush.is_flush
    assert straight_flush.is_flush
    assert not junk_hand.is_flush

def test_groups(straight_flush, junk_hand, four_of_a_kind, two_pair):
    assert not straight_flush.groups
    assert not junk_hand.groups
    assert four_of_a_kind.groups == {11: 4, 8: 1}
    assert two_pair.groups == {10: 2, 12: 2, 7: 1}

def test_hand_rank(royal_flush, straight_flush, four_of_a_kind, full_house, straight, flush, three_of_a_kind, two_pair, one_pair, junk_hand):
    assert royal_flush.hand_rank == (10, 14, None)
    assert straight_flush.hand_rank == (9, 10, None)
    assert four_of_a_kind.hand_rank == (8, 11, 8)
    assert full_house.hand_rank == (7, 6, 9)
    assert flush.hand_rank == (6, 10, None)
    assert straight.hand_rank == (5, 6, None)
    assert three_of_a_kind.hand_rank == (4, 10, 11)
    assert two_pair.hand_rank == (3, 12, 10)
    assert one_pair.hand_rank == (2, 10, 12)
    assert junk_hand.hand_rank == (1, 11, 9)

def test_heads_up():
    #given
    high_card_jack = ph.PokerHand("JH 9D 5C 3S 7H")
    high_card_jack_2 = ph.PokerHand("JD TC 8D 6C 3C")    
    # when
    result = ph.heads_up(high_card_jack, high_card_jack_2)    
    # then
    assert result == 2
    
    #given
    high_card_jack = ph.PokerHand("JH 6D 5C 3S 7H")
    one_pair = ph.PokerHand("TH TC 7D 6C 3C")
    # when
    result = ph.heads_up(one_pair, high_card_jack)    
    # then
    assert result == 1
    
    #given
    pair_of_jacks = ph.PokerHand("JH JD 5C 3S 7H")
    pair_of_jacks_ace_high = ph.PokerHand("JC JS AD 6C 3C")
    # when
    result = ph.heads_up(pair_of_jacks, pair_of_jacks_ace_high)    
    # then
    assert result == 2
    
    # given
    sixes_over_nines = ph.PokerHand("6H 6C 6D 9H 9S")
    sevens_over_tens = ph.PokerHand("TH TD 7C 7H 7S")
    # when
    result = ph.heads_up(sixes_over_nines, sevens_over_tens)
    # then
    assert result == 2