
import re

class PokerHand:
    def __init__(self,
                 hand_id=None,
                 players=None,
                 hero_cards=None,
                 all_hole_cards=None,
                 preflop_actions=None,
                 flop_board=None,
                 flop_actions=None,
                 turn_board=None,
                 turn_actions=None,
                 river_board=None,
                 river_actions=None,
                 showdown=None,
                 summary=None):
        self.hand_id = hand_id
        self.players = players or []
        self.hero_cards = hero_cards or []
        self.all_hole_cards = all_hole_cards or {}
        self.preflop_actions = preflop_actions or []
        self.flop_board = flop_board or []
        self.flop_actions = flop_actions or []
        self.turn_board = turn_board or []
        self.turn_actions = turn_actions or []
        self.river_board = river_board or []
        self.river_actions = river_actions or []
        self.showdown = showdown or []
        self.summary = summary or {}

        # parsed versions
        self.parsed_preflop = self.parse_street_actions(self.preflop_actions)
        self.parsed_flop = self.parse_street_actions(self.flop_actions)
        self.parsed_turn = self.parse_street_actions(self.turn_actions)
        self.parsed_river = self.parse_street_actions(self.river_actions)

    def __repr__(self):
        return (f"PokerHand(hand_id={self.hand_id}, hero_cards={self.hero_cards}, "
                f"flop={self.flop_board}, turn={self.turn_board}, river={self.river_board})")

    def parse_street_actions(self, action_lines):
        def parse_action_line(line):
            patterns = [
                (r"(\w+): checks", lambda m: {'player': m.group(1), 'action': 'check'}),
                (r"(\w+): folds", lambda m: {'player': m.group(1), 'action': 'fold'}),
                (r"(\w+): calls \$(\d+(?:\.\d+)?)", lambda m: {
                    'player': m.group(1), 'action': 'call', 'amount': float(m.group(2))}),
                (r"(\w+): raises \$(\d+(?:\.\d+)?) to \$(\d+(?:\.\d+)?)", lambda m: {
                    'player': m.group(1), 'action': 'raise',
                    'amount': float(m.group(2)), 'to': float(m.group(3))}),
                (r"Uncalled bet \(\$(\d+(?:\.\d+)?)\) returned to (\w+)",
                    lambda m: {'action': 'uncalled_bet_returned', 'player': m.group(2), 'amount': float(m.group(1))}),
                (r"(\w+): shows \[(\w+ \w+)\] \(([^)]+)\)",
                    lambda m: {
                        'player': m.group(1),
                        'action': 'show',
                        'hole_cards': m.group(2).split(),
                        'hand_value': m.group(3)
                    })

            ]

            # patterns = [
            #     (r"(\w+): checks", lambda m: {'player': m.group(1), 'action': 'check'}),
            #     (r"(\w+): folds", lambda m: {'player': m.group(1), 'action': 'fold'}),
            #     (r"(\w+): calls \$(\d+\.?\d+)", lambda m: {'player': m.group(1), 'action': 'call', 'amount': float(m.group(2))}),
            #     # (r"(\w+): bets \$(\d+\.?\d+)", lambda m: {'player': m.group(1), 'action': 'bet', 'amount': float(m.group(2))}),
            #     (r"(\w+): raises \$(\d+\.?\d+) to \$(\d+\.?\d+)",
            #      lambda m: {'player': m.group(1), 'action': 'raise', 'amount': float(m.group(2)), 'to': float(m.group(3))})
            # ]
            for pattern, parser in patterns:
                m = re.match(pattern, line.strip())
                if m:
                    print(m)
                    return parser(m)
            return None

        return [parsed for line in action_lines if (parsed := parse_action_line(line))]
