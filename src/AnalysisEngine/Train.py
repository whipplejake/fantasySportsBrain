import json
import os

import pandas as pd
from sklearn.cross_validation import train_test_split
from sklearn.metrics import classification_report
from sklearn.neural_network import MLPClassifier
from sklearn.preprocessing import StandardScaler

from AnalysisEngine.Metrics import get_score, weights
from DataCollector.DefensiveMatchup import DefensiveMatchup
from DataCollector.OffensiveStats import OffensiveStats


class Trainer:

    def __init__(self):
        self.offensive_stats = OffensiveStats(os.getcwd())
        # self.weather_stats = WeatherStats(os.getcwd())
        self.defensiveStats = DefensiveMatchup(os.getcwd())
        self.exit = 0
        self.classifier = MLPClassifier(hidden_layer_sizes=(100), max_iter=2000)
        position = input("What position would you like to train for? (QB, RB, WR(TE))\n>")
        if (position == "QB") | (position == "WR") | (position == "RB") | (position == "TE"):
            if position == "TE":
                print("TEs are trained under WRs, continuing as such...")
                self.position = "WR"
            else:
                self.position = position
        else:
            print("Incorrect option selected, returning to main menu...\n")
            self.exit = 1
            return
        start_season = input("What is the earliest season to be reference for data? (2013-2017)")
        try:
            start_int = int(start_season)
            if 2012 < start_int < 2018:
                self.start_season = start_int
            else:
                print("Incorrect option selected, returning to main menu...\n")
                self.exit = 1
                return
        except ValueError:
            print("Please enter a number, returning to main menu...\n")
            self.exit = 1
            return

    def train(self, current_dir):

        x = pd.read_csv("training_file.csv", header=None)
        y = pd.read_csv("target_file.csv", header=None)
        scaler = StandardScaler()
        # Fit only to the training data

        x_train, x_test, y_train, y_test = train_test_split(x, y, test_size=0.3)
        scaler.fit(x_train)
        x_train = scaler.transform(x_train)
        x_test = scaler.transform(x_test)
        self.classifier.fit(x_train, y_train)

        predictions = self.classifier.predict(x_test)

        print("Classifier training results: \n{}".format(classification_report(y_test, predictions)))


    def collect_data(self, current_dir):
        stats_json = open("{}{}".format(current_dir, "\\resources\offensiveHistory.json"), "r")
        weather_json = open("{}{}".format(current_dir, "\\resources\weatherHistory.json"), "r")
        with open("training_file.csv", "w+") as temp_file:
            target_file = open("target_file.csv", "w+")
            stats = json.loads(stats_json.read())
            for player in stats["players"]:
                if self.position == stats["players"][player]["position"]:
                    if self.position == "QB":
                        for game in stats["players"][player]["games"]:
                            if game != "overall":
                                temp_stats = stats["players"][player]["games"][game]
                                true = 1
                                if get_score(temp_stats) < weights["QB"]:
                                    true = 0
                                game_stat = "{},{},{},{},{},{},{},{},{}\n".format(temp_stats["rush_attemps"],
                                                                                        temp_stats["rush_yards"],
                                                                                        temp_stats["rush_tds"],
                                                                                        temp_stats["pass_attemps"],
                                                                                        temp_stats["pass_yards"],
                                                                                        temp_stats["pass_completions"],
                                                                                        temp_stats["pass_tds"],
                                                                                        temp_stats["interceptions_thrown"],
                                                                                        temp_stats["fumbles_lost"])
                                                                                        #get_score(temp_stats)) # , true)
                                temp_file.write(game_stat)
                                target_file.write("{}\n".format(true))
                    elif self.position == "RB":
                        for game in stats["players"][player]["games"]:
                            if game != "overall":
                                temp_stats = stats["players"][player]["games"][game]
                                true = 1
                                if get_score(temp_stats) < weights["RB"]:
                                    true = 0
                                game_stat = "{},{},{},{},{},{},{},{}\n".format(temp_stats["rush_attemps"],
                                                                                  temp_stats["rush_yards"],
                                                                                  temp_stats["rush_tds"],
                                                                                  temp_stats["targets"],
                                                                                  temp_stats["receptions"],
                                                                                  temp_stats["receiving_yards"],
                                                                                  temp_stats["receiving_tds"],
                                                                                  temp_stats["fumbles_lost"])
                                                                                  #get_score(temp_stats)) # true)       ,{:.2f}                                                                             # get_score(temp_stats), true)

                                temp_file.write(game_stat)
                                target_file.write("{}\n".format(true))
                    else:
                        for game in stats["players"][player]["games"]:
                            if game != "overall":
                                temp_stats = stats["players"][player]["games"][game]
                                true = 1
                                if get_score(temp_stats) < weights["WR"]:
                                    true = 0
                                game_stat = "{},{},{},{},{},{},{},{}\n".format(temp_stats["rush_attemps"],
                                                                               temp_stats["rush_yards"],
                                                                               temp_stats["rush_tds"],
                                                                               temp_stats["targets"],
                                                                               temp_stats["receptions"],
                                                                               temp_stats["receiving_yards"],
                                                                               temp_stats["receiving_tds"],
                                                                               temp_stats["fumbles_lost"])
                                                                               # get_score(temp_stats)) #, true) {:.2f},{},
                                temp_file.write(game_stat)
                                target_file.write("{}\n".format(true))

