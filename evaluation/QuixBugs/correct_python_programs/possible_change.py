
def possible_change(coins, total):
    if total == 0:
        return 1
    if total < 0 or not coins:
        return 0

    first, *rest = coins
    return possible_change(coins, total - first) + possible_change(rest, total)

"""
def possible_change(coins, total):
    if total == 0:
        return 1
    if not coins or total < 0:
        return 0

    first, *rest = coins
    return possible_change(coins, total - first) + possible_change(rest, total)

def possible_change(coins, total):
    if total == 0:
        return 1
    if total < 0 or len(coins) == 0:
        return 0

    first, *rest = coins
    return possible_change(coins, total - first) + possible_change(rest, total)

def possible_change(coins, total):
    if total == 0:
        return 1
    if len(coins) == 0 or total < 0:
        return 0

    first, *rest = coins
    return possible_change(coins, total - first) + possible_change(rest, total)

def possible_change(coins, total):
    if total == 0:
        return 1
    if not coins: return 0
    if total < 0:
        return 0

    first, *rest = coins
    return possible_change(coins, total - first) + possible_change(rest, total)

def possible_change(coins, total):
    if total == 0:
        return 1
    if len(coins) == 0: return 0
    if total < 0:
        return 0

    first, *rest = coins
    return possible_change(coins, total - first) + possible_change(rest, total)

"""
