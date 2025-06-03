
# from pokerhand_class import PokerHand
# from poker_hand_extractors import *

# # 读取文件并选择第一局作为示例
# with open("your_files.txt", "r", encoding="utf-8") as f:
#     text = f.read()

# hands = text.strip().split("\n\n")
# first_hand = hands[0]

# # 提取信息
# ph = PokerHand(
#     hand_id=extract_hand_id(first_hand),
#     players=extract_players(first_hand),
#     hero_cards=extract_all_hole_cards(first_hand).get("Hero", []),
#     all_hole_cards=extract_all_hole_cards(first_hand),
#     preflop_actions=extract_actions(first_hand, "HOLE CARDS"),
#     flop_board=extract_board(first_hand, "FLOP"),
#     flop_actions=extract_actions(first_hand, "FLOP"),
#     turn_board=extract_board(first_hand, "TURN"),
#     turn_actions=extract_actions(first_hand, "TURN"),
#     river_board=extract_board(first_hand, "RIVER"),
#     river_actions=extract_actions(first_hand, "RIVER"),
#     showdown=extract_showdown(first_hand),
#     summary=extract_summary(first_hand)
# )

# print(ph)
from pokerhand_class import PokerHand

hand = PokerHand(
    hand_id="RC123",
    preflop_actions=[
        "Player1: calls $0.10",
        "Player2: raises $0.20 to $0.30",
        "Player1: folds"
    ]
)

print(hand.parsed_preflop)