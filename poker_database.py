
import os
from pokerhand_class import PokerHand
from poker_hand_extractors import (
    extract_hand_id, extract_players, extract_all_hole_cards,
    extract_board, extract_actions, extract_showdown, extract_summary
)

class PokerDatabase:
    def __init__(self):
        self.hands = []
        self.sources = {}  # filename -> list of PokerHand

    def load_file(self, filepath):
        with open(filepath, "r", encoding="utf-8") as f:
            text = f.read()

        hand_blocks = text.strip().split("\n\n")
        file_hands = []

        for block in hand_blocks:
            hand = PokerHand(
                hand_id=extract_hand_id(block),
                players=extract_players(block),
                hero_cards=extract_all_hole_cards(block).get("Hero", []),
                all_hole_cards=extract_all_hole_cards(block),
                preflop_actions=extract_actions(block, "HOLE CARDS"),
                flop_board=extract_board(block, "FLOP"),
                flop_actions=extract_actions(block, "FLOP"),
                turn_board=extract_board(block, "TURN"),
                turn_actions=extract_actions(block, "TURN"),
                river_board=extract_board(block, "RIVER"),
                river_actions=extract_actions(block, "RIVER"),
                showdown=extract_showdown(block),
                summary=extract_summary(block)
            )
            self.hands.append(hand)
            file_hands.append(hand)

        self.sources[os.path.basename(filepath)] = file_hands

    def load_folder(self, folderpath):
        for fname in os.listdir(folderpath):
            if fname.endswith(".txt"):
                full_path = os.path.join(folderpath, fname)
                self.load_file(full_path)

    def to_dataframe(self):
        import pandas as pd
        data = []
        for h in self.hands:
            row = {
                "hand_id": h.hand_id,
                "hero_cards": " ".join(h.hero_cards),
                "flop": " ".join(h.flop_board),
                "turn": " ".join(h.turn_board),
                "river": " ".join(h.river_board),
                "total_pot": h.summary.get("total_pot", 0.0),
                "rake": h.summary.get("rake", 0.0),
                "jackpot": h.summary.get("jackpot", 0.0),
                "hero_vpip": int(any(a['player'] == "Hero" and a['action'] in ("call", "bet", "raise")
                                     for a in h.parsed_preflop)),
                "hero_pfr": int(any(a['player'] == "Hero" and a['action'] == "raise"
                                    for a in h.parsed_preflop))
            }
            data.append(row)
        return pd.DataFrame(data)

