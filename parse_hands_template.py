
import re

class PokerHand:
    def __init__(self, hand_id, hero_cards):
        self.hand_id = hand_id
        self.hero_cards = hero_cards

    def __repr__(self):
        return f"PokerHand(hand_id={self.hand_id}, hero_cards={self.hero_cards})"


class PokerHandParser:
    def __init__(self, filepath):
        self.filepath = filepath
        self.hands = []

    def load_file(self):
        with open(self.filepath, "r", encoding="utf-8") as f:
            self.raw_text = f.read()

    def parse_hands(self):
        hand_blocks = self.raw_text.strip().split("\n\n")
        for block in hand_blocks:
            hand_id = self._extract_hand_id(block)
            hero_cards = self._extract_hero_cards(block)
            hand = PokerHand(hand_id, hero_cards)
            self.hands.append(hand)

    def _extract_hand_id(self, text):
        match = re.search(r"Poker Hand #(\w+):", text)
        return match.group(1) if match else None

    def _extract_hero_cards(self, text):
        match = re.search(r"Dealt to Hero \[(.*?)\]", text)
        return match.group(1).split() if match else []

    def get_hands(self, n=5):
        return self.hands[:n]

# 示例用法
if __name__ == "__main__":
    parser = PokerHandParser("GG20240110-0609 - RushAndCash3877746 - 0.05 - 0.1 - 6max.txt")
    parser.load_file()
    parser.parse_hands()
    for hand in parser.get_hands():
        print(hand)
