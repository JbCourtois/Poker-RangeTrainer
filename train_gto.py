from collections import OrderedDict
import json
import random

from eval7.handrange import HandRange

from utils.cards import Hole
from utils.structures import Cycle


with open('gto_ranges.json') as file:
    RANGES = json.load(file, object_pairs_hook=OrderedDict)
POSITIONS = list(RANGES)


HERO_RANGE = HandRange(
    "22+, A2+, K5s+, K9o+, Q5s+, Q9o+, J5s+, J8o+, "
    "T7s+, T8o+, 96s+, 98o, 85s+, 87o, 75s+, 64s+, 43s+"
)
HERO_CARDS = [Hole.from_eval(evalhand) for evalhand, _ in HERO_RANGE.hands]


class Game:
    def __init__(self):
        self.hero_positions_cycle = Cycle(POSITIONS)
        self.hero_pos = None
        self.opp_pos = None
        self.last_action = None

    def run(self):
        while True:
            self.run_hand()

            print()
            print('------')
            print()

    def run_hand(self):
        self.init_hand()

        strategy = RANGES[self.hero_pos]

        while True:
            for pos in POSITIONS:
                if pos == self.opp_pos:
                    self.last_action += 1
                    action = (
                        'raises' if self.last_action == 2 else
                        f'{self.last_action}-bets'
                    )
                    print(f'{self.opp_pos} {action}.')

                if pos == self.hero_pos:
                    if self.last_action > 5:
                        return

                    action = input('Your action?  (R)aise  (C)all  (F)old  ')

                    hero_strat = (
                        strategy['RFI'] if self.last_action == 1 else
                        strategy['VS RAISE'][self.opp_pos] if self.last_action == 2 else
                        strategy[f'VS {self.last_action}BET'][self.opp_pos]
                    )
                    print('Recommended strategy', hero_strat.get(self.hero_token))

                    if action.upper() != 'R':
                        return

                    self.last_action += 1

    def init_hand(self):
        self.hero_pos = next(self.hero_positions_cycle)
        self.last_action = 1

        opp_offset = random.randint(1, len(POSITIONS) - 1)
        self.opp_pos = self.hero_positions_cycle.peek(opp_offset)

        hero_cards = random.choice(HERO_CARDS)
        self.hero_token = hero_cards.token

        print(f'You are {self.hero_pos} with {hero_cards}.')
        print()


if __name__ == '__main__':
    ggg = Game()
    ggg.run()
