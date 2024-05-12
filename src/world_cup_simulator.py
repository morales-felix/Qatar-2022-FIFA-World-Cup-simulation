import csv
import math
import random
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt


def read_games(file):
    """
    Initializes game objects from csv
    """

    games = [item for item in csv.DictReader(open(file, encoding="latin-1"))]

    return games


def simulate_group_stage_game(game, ternary=True):
    """
    Simulates a single game in the group stage
    """

    home = game["elo_prob_home"]
    away = 1 - game["elo_prob_home"]
    tie = 0

    # Simulating game proper
    wildcard = random.uniform(0, 1)

    # Concoction to go from binary probabilities to ternary
    if ternary:
        if home > 0 and home < 1:
            home_odds = home / away
            tie_odds = 1
            away_odds = 1 - abs(home - 0.5) * 2

            home_odds1 = (home / away) / min(away_odds, tie_odds, home_odds)
            tie_odds1 = 1 / min(away_odds, tie_odds, home_odds)
            away_odds1 = (1 - abs(home - 0.5) * 2) / min(away_odds, tie_odds, home_odds)

            home = home_odds1 / (home_odds1 + tie_odds1 + away_odds1)
            tie = tie_odds1 / (home_odds1 + tie_odds1 + away_odds1)
            away = away_odds1 / (home_odds1 + tie_odds1 + away_odds1)

        elif home == 0:
            tie = 0
            away = 1

        elif home == 1:
            tie = 0
            away = 0

        else:
            raise ValueError("Probabilities must be floats between 0 and 1, inclusive")
    else:
        pass

    if wildcard >= 0 and wildcard < away:
        return 0

    if wildcard >= away and wildcard < away + tie and ternary:
        return 0.5

    if wildcard >= away + tie and wildcard <= 1:
        return 1


def simulate_playoff_game(game, ternary=True):
    """
    Simulates a single game in the knockout stage
    """

    home = game["elo_prob_home"]
    away = 1 - game["elo_prob_home"]
    tie = 0

    # Simulating game proper
    wildcard = random.uniform(0, 1)

    # Concoction to go from binary probabilities to ternary
    # 50-50% should translate into 1/3, 1/3, 1/3 (even split of probability space)
    # With increasing lopsidedness (e.g. 75-25%), the stronger team should see increased win probability,
    # and the weaker team should see decreased win probability. And in terms of ties, that also should decrease
    # as lopsidedness increases, but I assume that at a lower rate than weaker team win probability.
    if ternary:
        if home > 0 and home < 1:
            home_odds = home / away
            tie_odds = 1
            away_odds = 1 - abs(home - 0.5) * 2

            home_odds1 = (home / away) / min(away_odds, tie_odds, home_odds)
            tie_odds1 = 1 / min(away_odds, tie_odds, home_odds)
            away_odds1 = (1 - abs(home - 0.5) * 2) / min(away_odds, tie_odds, home_odds)

            home = home_odds1 / (home_odds1 + tie_odds1 + away_odds1)
            tie = tie_odds1 / (home_odds1 + tie_odds1 + away_odds1)
            away = away_odds1 / (home_odds1 + tie_odds1 + away_odds1)

        elif home == 0:
            tie = 0
            away = 1

        elif home == 1:
            tie = 0
            away = 0

        else:
            raise ValueError("Probabilities must be floats between 0 and 1, inclusive")
    else:
        pass

    if wildcard >= 0 and wildcard < away:
        return game["away_team"], game["home_team"], 0, False

    if wildcard >= away and wildcard < away + tie and ternary:
        # Simulating outcome of a penalty shootout. I assume it is a coin-toss. An advancing team is needed.
        teams = [game["away_team"], game["home_team"]]
        advances = np.random.choice(teams)
        teams.remove(advances)
        return advances, teams[0], 0.5, True

    if wildcard >= away + tie and wildcard <= 1:
        return game["home_team"], game["away_team"], 1, False


def simulate_group_stage(games, teams, ternary=True):
    """
    Simulates the entire group stage
    """

    for game in games:
        team1, team2 = teams[game["home_team"]], teams[game["away_team"]]

        # Home field advantage is BS
        elo_diff = team1["rating"] - team2["rating"]

        # This is the most important piece, where we set my_prob1 to our forecasted probability
        game["elo_prob_home"] = 1.0 / (math.pow(10.0, (-elo_diff / 400.0)) + 1.0)

        # If game was played, maintain team Elo ratings
        if game["result_home"] == "":

            game["result_home"] = simulate_group_stage_game(game, ternary)

            # Elo shift based on K
            shift = 60.0 * (game["result_home"] - game["elo_prob_home"])

            # Apply shift
            team1["rating"] += shift
            team2["rating"] -= shift

            # Apply points
            if game["result_home"] == 0:
                team1["points"] += 0
                team2["points"] += 3
            elif game["result_home"] == 0.5:
                team1["points"] += 1
                team2["points"] += 1
            else:
                team1["points"] += 3
                team2["points"] += 0


def simulate_playoffs(games, teams, ternary=True):
    """
    Simulates the entire knockout stage
    """

    for game in games:
        team1, team2 = teams[game["home_team"]], teams[game["away_team"]]

        # Home field advantage is B.S. in modern soccer
        elo_diff = team1["rating"] - team2["rating"]

        # This is the most important piece
        game["elo_prob_home"] = 1.0 / (math.pow(10.0, (-elo_diff / 400.0)) + 1.0)

        # If game was played, maintain team Elo ratings
        if game["advances"] == "" or game["loses"] == "":

            game["advances"], game["loses"], game["result_home"], game["penalties"] = (
                simulate_playoff_game(game, ternary)
            )

            # Elo shift based on K
            shift = 60.0 * (game["result_home"] - game["elo_prob_home"])

            # Apply shift
            team1["rating"] += shift
            team2["rating"] -= shift

        # This is to populate quarterfinals and the such depending on previous rounds' results
        next_stage = int(game["to_match"])

        if next_stage < 14:

            if games[next_stage]["home_team"] == "":
                games[next_stage]["home_team"] = game["advances"]
            else:
                games[next_stage]["away_team"] = game["advances"]

        elif next_stage == 14:
            if games[next_stage]["home_team"] == "":
                games[next_stage]["home_team"] = game["advances"]
            else:
                games[next_stage]["away_team"] = game["advances"]

            if games[next_stage + 1]["home_team"] == "":
                games[next_stage + 1]["home_team"] = game["loses"]
            else:
                games[next_stage + 1]["away_team"] = game["loses"]

        else:
            pass


def collect_playoff_results(team, dataframe):
    """
    Collects the results of a team in the knockout stage
    """
    
    f = dataframe["home_team"] == team
    g = dataframe["away_team"] == team

    team_pd = dataframe.loc[f | g]
    max_match_number = team_pd["match"].astype(int).max()

    if max_match_number < 8:
        result = "Round_of_16"
    elif max_match_number >= 8 and max_match_number < 12:
        result = "Quarterfinals"
    elif max_match_number == 14:
        if team_pd.loc[max_match_number, "advances"] == team:
            result = "Champion"
        else:
            result = "Second_place"
    elif max_match_number == 15:
        if team_pd.loc[max_match_number, "advances"] == team:
            result = "Third_place"
        else:
            result = "Fourth_place"

    return result
