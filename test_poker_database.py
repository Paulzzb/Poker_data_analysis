from poker_database import PokerDatabase
import analytics
# import pdb

# pdb.set_trace()

db = PokerDatabase()
db.load_file("./your_files.txt")
df = db.to_dataframe()

# 查看 VPIP、PFR
print("VPIP:", analytics.vpip_rate(df))
print("PFR:", analytics.pfr_rate(df))

# 画 Hero 盈利曲线
analytics.plot_hero_profit_curve(df)
