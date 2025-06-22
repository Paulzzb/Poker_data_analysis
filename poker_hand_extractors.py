
import re
from datetime import datetime

def extract_hand_id(text):
    match = re.search(r"Poker Hand #(\w+):", text)
    return match.group(1) if match else None

def extract_hand_time(text):
    match = re.search(r"\- (\d{4}/\d{2}/\d{2} \d{2}:\d{2}:\d{2})", text)
    if match:
        return datetime.strptime(match.group(1), "%Y/%m/%d %H:%M:%S")
    return None

def extract_players(text):
    players = []
    for line in text.splitlines():
        if line.startswith("Seat "):
            m = re.match(r"Seat (\d+): (\S+) \(\$(\d+\.?\d*) in chips\)", line)
            if m:
                seat, name, chips = m.groups()
                players.append({"seat": int(seat), "name": name, "chips": float(chips)})
    return players


def extract_post_blinds(text):
    blinds = []
    pattern = re.compile(r"(\w+): posts (small|big) blind \$(\d+(?:\.\d+)?)")
    for match in pattern.finditer(text):
        blinds.append({
            "player": match.group(1),
            "type": f"{match.group(2)}_blind",
            "amount": float(match.group(3))
        })
    return blinds

def extract_all_hole_cards(text):
    dealt_lines = re.findall(r"Dealt to (\S+) \[(.*?)\]", text)
    return {name: cards.split() for name, cards in dealt_lines}

def extract_board(text, street):
    pattern = {
        "FLOP": r"\*\*\* FLOP \*\*\* \[(.*?)\]",
        "TURN": r"\*\*\* TURN \*\*\* \[.*?\] \[(.*?)\]",
        "RIVER": r"\*\*\* RIVER \*\*\* \[.*?\] \[(.*?)\]"
    }
    match = re.search(pattern[street], text)
    return match.group(1).split() if match else []

def extract_actions(text, street):
    # e.g. street = 'PREFLOP' for pre-flop actions
    pattern = f"*** {street} ***"
    start = text.find(pattern)
    if start == -1:
        return []
    next_street = ["FLOP", "TURN", "RIVER", "SHOWDOWN", "SUMMARY"]
    end = len(text)
    for s in next_street:
        idx = text.find(f"*** {s} ***", start + 1)
        if idx > start:
            end = idx
            break
    action_lines = text[start:end].strip().splitlines()[1:]  # skip header
    return action_lines

def extract_showdown(text):
    return re.findall(r"\*\*\* SHOWDOWN \*\*\*\n(.*?)\n\*\*\* SUMMARY", text, re.S)

def extract_summary(text):
    summary = {}
    m = re.search(r"Total pot \$(\d+\.?\d*) \| Rake \$(\d+\.?\d*) \| Jackpot \$(\d+\.?\d*)", text)
    if m:
        summary["total_pot"], summary["rake"], summary["jackpot"] = map(float, m.groups())
    return summary
