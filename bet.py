import pandas as pd
import json
from pprint import pprint
import matplotlib.pyplot as plt

import names


def calculate_probs(w_elo, l_elo):
    return 1 / (1 + 10**((w_elo - l_elo) / 400))

# def calculate_probs(w_elo, l_elo):
#     return w_elo / (w_elo + l_elo)


def prob_to_odd(prob):
    return prob / (1 - prob) + 1


def sim_tournament(filename, jsonname, money):
    elo_ratings_file = open(jsonname)
    elo_ratings_dict = json.load(elo_ratings_file)

    tour = pd.read_csv(filename)
    year = tour["Date"].iloc[0].split("/")[2]

    stats = {
        "Total games": tour.shape[0],
        "Number of bets": 0,
        "Number of winning bets": 0,
        "Number of losing bets": 0,
        "Percentage of success": 0,
        "Percentage of fails": 0,
        "Money": 0
    }

    money_list = [money]

    for _, game in tour.iterrows():
        winner_name = game["Winner"]
        loser_name = game["Loser"]

        winner_odd = game["B365W"]
        loser_odd = game["B365L"]

        winner_elo = -1
        loser_elo = -1
        find_winner = False
        find_loser = False

        for player_name in elo_ratings_dict.keys():
            if find_winner and find_loser:
                break

            elif names.names_compare(player_name, winner_name):
                winner_elo = elo_ratings_dict[player_name][year]["Elo"]
                find_winner = True

            elif names.names_compare(player_name, loser_name):
                loser_elo = elo_ratings_dict[player_name][year]["Elo"]
                find_loser = True

        if (winner_elo > 0) and (loser_elo > 0):
            winner_prob = calculate_probs(winner_elo, loser_elo)
            loser_prob = 1 - winner_prob

            winner_true_odd = prob_to_odd(winner_prob)
            loser_true_odd = prob_to_odd(loser_prob)

            print("Loser odds: {} - {}".format(loser_odd, loser_true_odd))
            print("Winner odds: {} - {}".format(winner_odd, winner_true_odd))

            if winner_odd > winner_true_odd:
                money += money * 0.1 * (winner_odd - 1)
                stats["Number of winning bets"] += 1
                stats["Number of bets"] += 1
            elif loser_odd > loser_true_odd:
                money *= 0.9
                stats["Number of losing bets"] += 1
                stats["Number of bets"] += 1

            money_list.append(money)

    stats["Percentage of success"] = (stats["Number of winning bets"] / stats["Number of bets"]) * 100
    stats["Percentage of fails"] = (stats["Number of losing bets"] / stats["Number of bets"]) * 100
    stats["Money"] = money

    pprint(stats)

    plt.plot(money_list)
    plt.show()


sim_tournament("ausopen2019.csv", "wta_elo_ratings.json", 40)
