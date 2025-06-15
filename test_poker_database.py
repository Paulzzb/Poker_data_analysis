from poker_database import PokerDatabase
import analytics
# import pdb

# pdb.set_trace()

db = PokerDatabase()
db.load_file("./your_files.txt")
df = db.to_dataframe()


# print(f"共读取手牌数: {len(db.hands)}")
# for i, h in enumerate(db.hands[:3]):
#     print(f"Hand {i+1}: ID = {h.hand_id}, Hero cards = {h.hero_cards}")

# 第一手牌信息
for i, h in enumerate(db.hands[:1]):  
    print(f"Hand ID: {h.hand_id}")
    print("Players:", h.players)
    print("Hero hole cards:", h.hero_cards)
    print("Preflop actions:", h.preflop_actions)
    print("Parsed Preflop:", h.parsed_preflop)
    print("Flop board:", h.flop_board)
    print("Turn:", h.turn_board)
    print("Showdown:", h.showdown)
    print("Summary:", h.summary)


# 查看 VPIP、PFR
print("VPIP:", analytics.vpip_rate(df))
print("PFR:", analytics.pfr_rate(df))
print("Profit:", analytics.calculate_hero_profit(df))
# 画 Hero 盈利曲线
analytics.plot_hero_profit_curve(df)
