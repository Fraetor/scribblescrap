import random

def roll(sides, num):
    total = 0

    for i in range(num):
        total += random.randint(1, sides)

    return total

def choose_stats(ranking):
    stats = {}

    for (rank, (s, n)) in zip(ranking, [(12, 12), (10, 10), (8, 8), (6, 8)]):
        stats[rank] = roll(s, n)

    return stats
