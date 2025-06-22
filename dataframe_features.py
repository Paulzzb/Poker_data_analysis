import pandas as pd
import re
def extract_investment_by_player(hand):
    players = hand.get("players", [])
    investment_dict = {p: 0.0 for p in players}

    # 先添加 posts small/big blind 的投入
    for blind in hand.get("post_blinds", []):
        player = blind.get("player")
        amount = blind.get("amount", 0.0)
        if player in investment_dict:
            investment_dict[player] += float(amount)


    for street in ["parsed_preflop", "parsed_flop", "parsed_turn", "parsed_river"]:
        actions = hand.get(street, [])
        street_invest = {p: 0.0 for p in players}
        returned = {p: 0.0 for p in players}

        for act in actions:
            player = act.get("player")
            if player not in players:
                continue

            if act.get("action") in {"call", "raise"}:
                if "to" in act:
                    street_invest[player] = float(act["to"])
                elif "amount" in act:
                    street_invest[player] = float(act["amount"])
            elif act.get("action") == "uncalled_bet_returned":
                returned[player] += float(act["amount"])

        for p in players:
            investment_dict[p] += max(street_invest[p] - returned[p], 0.0)

    return [investment_dict[p] for p in players]


def extract_profit_by_players(hand):
    players = hand.get("players", [])
    profit_dict = {p: 0.0 for p in players}
    collected_dict = {p: 0.0 for p in players}
    
    # Find whowin
    for line in hand.get("showdown", []):
        m = re.match(r"(\w+) collected \$(\d+(?:\.\d+)?) from pot", line)
        if m:
            player = m.group(1)
            amount = float(m.group(2))
            collected_dict[player] += amount
    
    investments = extract_investment_by_player(hand)

    # 计算净盈利
    for i, p in enumerate(players):
        profit_dict[p] = collected_dict[p] - investments[i]

    return profit_dict


def extract_winflag(hand):
    players = hand.get("players", [])
    winflag_dict = {p: False for p in players}
    
    # Find whowin
    for line in hand.get("showdown", []):
        m = re.match(r"(\w+) collected \$(\d+(?:\.\d+)?) from pot", line)
        if m:
            player = m.group(1)
            winflag_dict[player] = True

    return winflag_dict

# # def extract_showdown(hand):
    
#     return isshowdown

