
import pandas as pd
import matplotlib.pyplot as plt

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
    # 初始化投资总额为0
    total = 0.0
    # 遍历四个阶段
    for street in ["preflop_actions", "flop_actions", "turn_actions", "river_actions"]:
        # 获取当前阶段的动作列表
        actions = row.get(street, [])
        # 遍历动作列表
        for act in actions:
            # 匹配动作中的投资信息
            m = re.match(r"Hero: (bets|calls|raises) \$(\d+(\.\d+)?)", act)
            if m:
                # 如果匹配成功，将投资金额转换为浮点数并累加到总投资额中
                total += float(m.group(2))
            else:
                # 如果匹配失败，则匹配其他类型的投资信息
                m2 = re.match(r"Hero: raises \$\d+(\.\d+)? to \$(\d+(\.\d+)?)", act)
                if m2:
                    # 如果匹配成功，将投资金额转换为浮点数并累加到总投资额中
                    total += float(m2.group(2))
    # 返回总投资额
    return total

def extract_hero_return(row):
    # 找到 SHOWDOWN 中 Hero 所获金额
    for line in row.get("showdown", []):
        m = re.match(r"Hero collected \$(\d+(\.\d+)?) from pot", line)
        if m:
            return float(m.group(1))
    return 0.0

def calculate_hero_profit(df):
    # 复制数据框
    df = df.copy()
    # 对数据框中的每一行应用extract_hero_investment函数，并将结果存储在hero_invest列中
    df["hero_invest"] = df.apply(extract_hero_investment, axis=1)
    # 对数据框中的每一行应用extract_hero_return函数，并将结果存储在hero_return列中
    df["hero_return"] = df.apply(extract_hero_return, axis=1)
    # 计算hero_profit列，即hero_return减去hero_invest
    df["hero_profit"] = df["hero_return"] - df["hero_invest"]
    # 返回数据框
    return df

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

