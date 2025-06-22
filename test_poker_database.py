from poker_database2 import PokerDatabase
import analytics
# import pdb

# pdb.set_trace()

db = PokerDatabase()
# db.load_folder("F:\\扑克\\手牌NL25\\20250620")
db.load_file("./test2.txt")
df = db.to_dataframe()


print(f"共读取手牌数: {len(db.hands)}")

# 第一手牌信息



# 查看 VPIP、PFR
print("VPIP:", analytics.vpip_rate(df))
print("PFR:", analytics.pfr_rate(df))
print("Profit overall:", analytics.calculate_hero_profit(df))
print("Profit showdown:", analytics.calculate_hero_profit(df, True))
print("Profit no showdown:", analytics.calculate_hero_profit(df, False))
# 画 Hero 盈利曲线
# calculate_hero_profit(df, ifshowdown=True)
# calculate_hero_profit(df, ifshowdown=False)
# calculate_hero_profit(df)
# analytics.plot_hero_profit_curve(df)
