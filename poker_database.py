
import os
import re
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
        def format_action(a):
            if not isinstance(a, dict):
                return str(a)
            parts = [a.get("player", ""), a.get("action", "")]
            if "amount" in a:
                parts.append(f"${a['amount']}")
            if "to" in a:
                parts.append(f"to ${a['to']}")
            return " ".join(parts)

        import pandas as pd
        data = []
        for h in self.hands:
            who_win = []
            collected_total = 0.0

            for line in h.showdown:
                m = re.match(r"(\w+) collected \$(\d+(?:\.\d+)?) from pot", line)
                if m:
                    who_win.append(m.group(1))
                    collected_total += float(m.group(2))


            showdown_players = []
            for line in h.showdown:
                m = re.match(r"(\w+): shows \[", line)
                if m:
                    showdown_players.append(m.group(1))
            isshowdown = "Hero" in showdown_players



            row = {
                "hand_id": h.hand_id,
                "hero_cards": " ".join(h.hero_cards),
                "flop": " ".join(h.flop_board),
                "turn": " ".join(h.turn_board),
                "river": " ".join(h.river_board),

                # 结构化字段（推荐用于分析）
                "parsed_preflop": getattr(h, "parsed_preflop", []),
                "parsed_flop": getattr(h, "parsed_flop", []),
                "parsed_turn": getattr(h, "parsed_turn", []),
                "parsed_river": getattr(h, "parsed_river", []),

                # 可视化展示用（字符串版）
                "preflop_actions_str": " | ".join(format_action(a) for a in getattr(h, "parsed_preflop", [])),
                "flop_actions_str": " | ".join(format_action(a) for a in getattr(h, "parsed_flop", [])),
                "turn_actions_str": " | ".join(format_action(a) for a in getattr(h, "parsed_turn", [])),
                "river_actions_str": " | ".join(format_action(a) for a in getattr(h, "parsed_river", [])),

                # 统计字段
                "total_pot": h.summary.get("total_pot", 0.0),
                "rake": h.summary.get("rake", 0.0),
                "jackpot": h.summary.get("jackpot", 0.0),
                "hero_vpip": int(any(a.get("player") == "Hero" and a.get("action") in ("call", "bet", "raise")
                                     for a in getattr(h, "parsed_preflop", []))),
                "hero_pfr": int(any(a.get("player") == "Hero" and a.get("action") == "raise"
                                    for a in getattr(h, "parsed_preflop", []))),
                "winner": "Hero" if who_win == ["Hero"] else "Split" if "Hero" in who_win else "Other",
                "who_win": who_win,
                "hero_collected": collected_total if who_win == ["Hero"] else (
                    collected_total / len(who_win) if "Hero" in who_win else 0.0)
            }
            data.append(row)
        return pd.DataFrame(data)

