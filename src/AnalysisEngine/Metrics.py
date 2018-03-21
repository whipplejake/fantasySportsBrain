

weights = {"std": 0,  # Season to Date
           "prv": 0,  # previous results against opponent
           "head": 0,  # head to head matchup
           "wth": 0,  # Weather factor
           "def": 0,  # Defensive Factor
           "depth": 0,  # Depth Chart
           "inj": 0,  # Injury report
           "QB": 16.0,
           "RB": 12.0,
           "WR": 11.0
           }

# yahoo sports default
scoring = {"rush_attemps": 0,
           "rush_yards": 0.1,
           "rush_tds": 6.0,
           "targets": 0.0,
           "receptions": 1.0,
           "receiving_yards": 0.1,
           "receiving_tds": 6.0,
           "pass_attemps": 0.0,
           "pass_completions": 0.0,
           "pass_yards": 0.04,
           "pass_tds": 4.0,
           "interceptions_thrown": -1.0,
           "fumbles_lost": -2.0
}


def get_score(game):

    return game["rush_attemps"] * scoring["rush_attemps"] + game["rush_yards"] * scoring["rush_yards"] + \
           game["rush_tds"] * scoring["rush_tds"] + game["targets"] * scoring["targets"] + game["receptions"] * \
           scoring["receptions"] + game["receiving_yards"] * scoring["receiving_yards"] + game["receiving_tds"] * \
           scoring["receiving_tds"] + game["pass_attemps"] * scoring["pass_attemps"] + game["pass_completions"] * \
           scoring["pass_completions"] + game["pass_yards"] * scoring["pass_yards"] + game["pass_tds"] * \
           scoring["pass_tds"] + game["interceptions_thrown"] * scoring["interceptions_thrown"] + game["fumbles_lost"] * \
           scoring["fumbles_lost"]