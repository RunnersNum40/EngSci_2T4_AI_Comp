from secrets import randbelow

class Deck:
    def __init__(self):
        self.cards = [('C', 2), ('C', 3), ('C', 4), ('C', 5), ('C', 6), ('C', 7), ('C', 8), ('C', 9), ('C', 10), ('C', 11), ('C', 12), ('C', 13), ('C', 14), 
                      ('D', 2), ('D', 3), ('D', 4), ('D', 5), ('D', 6), ('D', 7), ('D', 8), ('D', 9), ('D', 10), ('D', 11), ('D', 12), ('D', 13), ('D', 14), 
                      ('H', 2), ('H', 3), ('H', 4), ('H', 5), ('H', 6), ('H', 7), ('H', 8), ('H', 9), ('H', 10), ('H', 11), ('H', 12), ('H', 13), ('H', 14), 
                      ('S', 2), ('S', 3), ('S', 4), ('S', 5), ('S', 6), ('S', 7), ('S', 8), ('S', 9), ('S', 10), ('S', 11), ('S', 12), ('S', 13), ('S', 14), 
                      ('W', 0), ('W', 0), ('W', 0), ('W', 0), ('J', 0), ('J', 0), ('J', 0), ('J', 0)]

    def deal(self, n):
        """Deal out n cards from the deck"""
        return choices(self.cards, n)

    def __str__(self):
        return str(self.cards)

def winner(trick, trump=None):
    """Return the index of the winning card in a trick"""
    if ("W", 0) in trick:
        # If there is a wizard return the first one
        return trick.index(("W", 0))
    elif trick.count(("J", 0)) == min(4, len(trick)):
        # If there is a Jester and all the Jesters are played return the first one
        return trick.index(("J", 0))
    else:
        return winner_by_suit(trick, trump)

def first_non_jester(trick):
    """Return the suit of the first card in the trick that is not a Jester"""
    for card in trick:
        if card[0] != "J":
            return card[0]

def winner_by_suit(trick, trump):
    """Score a trick without a special card winner"""
    winner = (None, 0) # Declare a Null winner to beat (winner index, winner trump card value)
    for n, card in enumerate(trick):
        if card[0] == trump and card[1] > winner[1]:
            winner = (n, card[1])
    if winner[0] is not None:
        return winner[0]
    else:
        trump = first_non_jester(trick)
        return winner_by_suit(trick, trump)

def choices(l, n):
    """Pop and return n random items from l"""
    items = []
    for _ in range(n):
        items.append(l.pop(randbelow(len(l))))
    return items

class Hand:
    def __init__(self, players, n_cards):
        self.players = players
        self.deck = Deck()

class Player:
    def bid()