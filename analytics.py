
import pandas as pd
import matplotlib.pyplot as plt
import re

def vpip_rate(df):
    return df["hero_vpip"].sum() / len(df)

def pfr_rate(df):
    return df["hero_pfr"].sum() / len(df)

def avg_rake(df):
    return df["rake"].mean()

def saw_flop_rate(df):
    if "saw_flop" in df.columns:
        return df["saw_flop"].sum() / len(df)
    return None

def extract_hero_investment(row):
    total_invest = 0.0

    for street in ["parsed_preflop", "parsed_flop", "parsed_turn", "parsed_river"]:
        actions = row.get(street, [])
        street_invest = 0.0
        returned = 0.0

        for act in actions:
            if act.get("player") == "Hero":
                if act.get("action") in {"call", "raise"}:
                    if "to" in act:
                        street_invest = float(act["to"])  # 覆盖为最新一次 raise 的 to 值
                    elif "amount" in act:
                        street_invest = float(act["amount"])
                elif act.get("action") == "uncalled_bet_returned":
                    returned += float(act["amount"])

        total_invest += max(street_invest - returned, 0.0)
        # print(street, street_invest, returned, total_invest)
        # 1

    return total_invest

def calculate_hero_investment(df, ifshowdown=None):
    filtered = df
    if ifshowdown is True:
        filtered = df[df["isshowdown"] == 1]
    elif ifshowdown is False:
        filtered = df[df["isshowdown"] == 0]

    return filtered.apply(extract_hero_investment, axis=1).sum()




def calculate_hero_profit(df, ifshowdown=None):
    filtered = df
    if ifshowdown is True:
        filtered = df[df["isshowdown"] == 1]
    elif ifshowdown is False:
        filtered = df[df["isshowdown"] == 0]

    profit = []
    for _, row in filtered.iterrows():
        invest = extract_hero_investment(row)
        win = row.get("hero_collected", 0.0)
        profit.append(win - invest)
    return sum(profit)



def plot_hero_profit_curve(df):
    df = calculate_hero_profit(df)
    df["cumulative_profit"] = df["hero_profit"].cumsum()
    df["hand_number"] = range(1, len(df) + 1)

    plt.figure(figsize=(10, 4))
    plt.plot(df["hand_number"], df["cumulative_profit"], marker="o", linestyle="-")
    plt.title("Hero win rate curve")
    plt.xlabel("hands")
    plt.ylabel("accumulate winning ($)")
    plt.grid(True)
    plt.tight_layout()
    plt.show()
    return df[["hand_id", "hero_invest", "hero_return", "hero_profit", "cumulative_profit"]]

