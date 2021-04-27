from collections import namedtuple
from random import shuffle

from termcolor import colored
from eval7.handrange import HandRange


class IndexableMixin:
    _auto_id = 0

    def __new__(cls, *args, **kwargs):
        obj = super().__new__(cls, *args, **kwargs)
        obj.__index = IndexableMixin._auto_id
        IndexableMixin._auto_id += 1

        return obj

    def __lt__(self, other):
        return self.__index < other.__index

    def __gt__(self, other):
        return self.__index > other.__index


class Rank(IndexableMixin, str):
    pass


RANKS = [Rank(rank) for rank in [
    '2', '3', '4', '5', '6', '7', '8', '9',
    'T', 'J', 'Q', 'K', 'A',
]]


class Suit(IndexableMixin, namedtuple('Suit', ['letter', 'symbol', 'color'])):
    def __str__(self):
        return self.symbol

    def __repr__(self):
        return self.letter


SUITS = [
    Suit('c', '♣', 'green'),
    Suit('d', '♦', 'yellow'),
    Suit('h', '♥', 'red'),
    Suit('s', '♠', 'white'),
]


class Card(namedtuple('Card', ['rank', 'suit'])):
    def __str__(self):
        text = ''.join(map(str, [self.rank, self.suit]))
        return colored(text, self.suit.color, attrs=['bold'])

    def __repr__(self):
        return f'{self.rank}{self.suit!r}'

    def __lt__(self, other):
        return (self.rank, self.suit) < (other.rank, other.suit)

    def __gt__(self, other):
        return (self.rank, self.suit) > (other.rank, other.suit)

    @classmethod
    def from_eval(cls, card):
        rank = RANKS[card.rank]
        suit = SUITS[card.suit]

        return cls(rank, suit)


class CardSet(list):
    def __str__(self):
        return ' '.join(map(str, self))

    def __repr__(self):
        return ''.join(map(repr, self))

    @classmethod
    def from_eval(cls, cards):
        return cls(map(Card.from_eval, cards))

    @property
    def token(self):
        if len(self) <= 1:
            return repr(self)

        ranks = ''.join(sorted((card.rank for card in self), reverse=True))
        suffix = (
            '' if self[0].rank == self[1].rank else
            's' if self[0].suit == self[1].suit else
            'o'
        )
        return ranks + suffix

    def as_eval(self):
        return HandRange(repr(self)).hands[0][0]

    def bulkpop(self, nb_cards):
        return self.__class__(self.pop() for _ in range(nb_cards))


def generate_deck():
    deck = CardSet(Card(rank, suit) for rank in RANKS for suit in SUITS)
    shuffle(deck)
    return deck
