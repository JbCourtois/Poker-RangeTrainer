from collections import OrderedDict, defaultdict

from eval7.handrange import HandRange
from utils.cards import generate_deck


RANGES = OrderedDict([
    ('8', "77+, ATs+, A5s, AQo+, KJs+, QJs, J9s+, T9s, 98s, 87s"),
    ('7', "66, A4s, KTs, QTs, 76s"),
    ('LJ', "55, A9s, A3s, AJo, KQo"),
    ('HJ', "44-22, A8s-A7s, A2s, ATo, K9s, KJo, QJo, 65s"),
    ('CO', "A6s, A9o, KTo, Q9s, QTo, JTo, 54s"),
    ('BU', (
        "A8o-A2o, K8s-K5s, K9o, Q8s-Q7s, Q9o, J8s-J7s, J9o, "
        "T8s-T7s, T9o, 97s-96s, 86s-85s, 75s, 64s, 43s"
    )),
])


HAND_MAP = {}
for pos, rrr in RANGES.items():
    evalrrr = HandRange(rrr)
    for hand in evalrrr.hands:
        HAND_MAP[hand[0]] = pos

POS_MAP = defaultdict(set)
for hand, pos in HAND_MAP.items():
    POS_MAP[pos].add(hand)


deck = generate_deck()
to_raise = set()

for pos, rrr in RANGES.items():
    print()
    to_raise.update(POS_MAP[pos])

    hand = deck.bulkpop(2)
    hhh_eval = hand.as_eval()
    should_raise = hhh_eval in to_raise

    print(f'You are {pos} with {hand}.')
    action_is_raise = input('Your action?  (R)aise  (F)old  ').upper() == 'R'

    if action_is_raise == should_raise:
        print('Correct')
        continue

    correct_position = HAND_MAP.get(hhh_eval)
    if correct_position is None:
        print('Wrong! This hand should not be opened from any position.')
        continue

    print(f'Wrong! This hand should be opened from {correct_position} or later.')
