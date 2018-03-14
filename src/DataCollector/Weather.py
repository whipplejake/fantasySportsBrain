import json
from time import time, sleep
from pprint import pprint

import requests
import logging
import os

logger = logging.getLogger('driver')

# unique from weather underground (LIMITTED TO 500 CALLS A DAY/10 CALLS A MINUTE)
# key = "37ae4ca0f857e390"
key = "9b716298b39a6751"

weather_history_file = "\\resources\weatherHistory.json"

stadiums = {"HOU": {"city": "Houston", "state": "TX"},
            "PHI": {"city": "Philadelphia", "state": "PA"},
            "NE": {"city": "Foxborough", "state": "MA"},
            "JAC": {"city": "Jacksonville", "state": "FL"},
            "JAX": {"city": "Jacksonville", "state": "FL"},
            "ATL": {"city": "Atlanta", "state": "GA"},
            "CAR": {"city": "Charlotte", "state": "NC"},
            "BAL": {"city": "Baltimore", "state": "MD"},
            "CIN": {"city": "Cincinnati", "state": "OH"},
            "DET": {"city": "Detroit", "state": "MI"},
            "GB": {"city": "Green_Bay", "state": "WI"},
            "IND": {"city": "Indianapolis", "state": "IN"},
            "MIA": {"city": "Miami_Gardens", "state": "FL"},
            "BUF": {"city": "Orchard_Park", "state": "NY"},
            "MIN": {"city": "Minneapolis", "state": "MN"},
            "CHI": {"city": "Chicago", "state": "IL"},
            "NYJ": {"city": "East_Rutherford", "state": "NJ"},
            "NYG": {"city": "East_Rutherford", "state": "NJ"},
            "DAL": {"city": "Arlington", "state": "TX"},
            "PIT": {"city": "Pittsburgh", "state": "PA"},
            "CLE": {"city": "Cleveland", "state": "OH"},
            "TB": {"city": "Tampa", "state": "FL"},
            "NO": {"city": "New_Orleans", "state": "LA"},
            "TEN": {"city": "Nashville", "state": "TN"},
            "DEN": {"city": "Denver", "state": "CO"},
            "KC": {"city": "Kansas_City", "state": "MO"},
            "LAC": {"city": "Inglewood", "state": "CA"},
            "LA": {"city": "Inglewood", "state": "CA"},
            "SF": {"city": "Santa_Clara", "state": "CA"},
            "OAK": {"city": "Oakland", "state": "CA"},
            "SEA": {"city": "Seattle", "state": "WA"},
            "ARI": {"city": "Glendale", "state": "AZ"},
            "WAS": {"city": "Hyattsville", "state": "MD"},
            "SD": {"city": "San_Diego", "state": "CA"},
            "SAN": {"city": "San_Diego", "state": "CA"},
            "STL": {"city": "St_Louis", "state": "MO"}
            }


class WeatherStats:

    def __init__(self, base_path):
        self.base_path = base_path
        self.count_in_last_min = 10
        self.minute_start = 0
        if os.path.isfile("{}{}".format(self.base_path, weather_history_file)):
            logger.info("Weather file exists, loading data into a dictionary")
            read_file = open("{}{}".format(self.base_path, weather_history_file), "r")
            self.weather_stats = json.loads(read_file.read())
        else:
            self.weather_stats = dict()
            logger.info("Weather storage file not found. Will create one when program is closed.")

    def store_weather(self):
        write_file = open("{}{}".format(self.base_path, weather_history_file), "w+")
        json.dump(self.weather_stats, write_file, separators=(',', ':'), sort_keys=True)

    def get_weather_stats(self, game_id):

        if "{}".format(game_id) not in self.weather_stats:
            return None

        return self.weather_stats["{}".format(game_id)]

    def get_new_weather_stats(self, game_id, city, state, date, start_time):

        if"{}".format(game_id) not in self.weather_stats:

            weather = GameWeather(game_id, city, state, date, start_time)
            logger.info("Getting weather for game {} ({}, {}, {}, {})".format(game_id, city, state, date, start_time))

            now = time()

            if (self.count_in_last_min == 10) and (now - self.minute_start < 90.0):
                wait = 76 - (now - self.minute_start)
                logger.info("Waiting {} seconds to get new weather in order to satisfy API".format(wait))
                sleep(wait)
                self.count_in_last_min = 0
                self.minute_start = time()
            elif now - self.minute_start > 90.0:
                self.count_in_last_min = 0
                self.minute_start = time()

            self.count_in_last_min += 1
            request = requests.get("http://api.wunderground.com/api/{}/history_{}/q/{}/{}.json".format(key, date, state,
                                                                                                       city))
            if request.status_code == 200:
                stats = json.loads(request.text)["history"]["observations"]
                for entry in stats:
                    if entry["date"]["hour"] == "{}".format(start_time):
                        weather.info["temp1"] = float(entry["tempi"])
                        weather.info["fog"] += int(entry["fog"])
                        weather.info["rain"] += int(entry["rain"])
                        weather.info["snow"] += int(entry["snow"])
                        weather.info["hail"] += int(entry["hail"])
                    elif entry["date"]["hour"] == "{}".format(start_time + 1):
                        weather.info["temp2"] = float(entry["tempi"])
                        weather.info["fog"] += int(entry["fog"])
                        weather.info["rain"] += int(entry["rain"])
                        weather.info["snow"] += int(entry["snow"])
                        weather.info["hail"] += int(entry["hail"])
                    elif entry["date"]["hour"] == "{}".format(start_time + 2):
                        weather.info["temp3"] = float(entry["tempi"])
                        weather.info["fog"] += int(entry["fog"])
                        weather.info["rain"] += int(entry["rain"])
                        weather.info["snow"] += int(entry["snow"])
                        weather.info["hail"] += int(entry["hail"])
                    elif entry["date"]["hour"] == "{}".format(start_time + 4):
                        weather.info["temp4"] = float(entry["tempi"])
                        weather.info["fog"] += int(entry["fog"])
                        weather.info["rain"] += int(entry["rain"])
                        weather.info["snow"] += int(entry["snow"])
                        weather.info["hail"] += int(entry["hail"])
                self.weather_stats["{}".format(game_id)] = weather.info
            else:
                logger.info("Failed to get weather for game {} ({}, {}, {}, {}".format(game_id, city, state, date,
                                                                                       start_time))
                return None
        else:
            logger.info("Weather data for game {} already in database".format(game_id))


class GameWeather:

    def __init__(self, game_id, city, state, date, start_time):
        self.info = dict()
        self.info["game_id"] = game_id
        self.info["city"] = city
        self.info["state"] = state
        self.info["date"] = date
        self.info["start_time"] = start_time
        self.info["temp1"] = -100
        self.info["temp2"] = -100
        self.info["temp3"] = -100
        self.info["temp4"] = -100
        self.info["wind"] = -100
        self.info["fog"] = 0
        self.info["rain"] = 0
        self.info["snow"] = 0
        self.info["hail"] = 0
        self.info["forecast"] = ""

    def print_game_weather(self):
        print("Game ID: {}".format(self.info["game_id"]))
        print("City: {}".format(self.info["city"]))
        print("State: {}".format(self.info["state"]))
        print("Date: {}".format(self.info["date"]))
        print("Start Time: {}".format(self.info["start_time"]))
        print("Temp1: {}".format(self.info["temp1"]))
        print("Temp2: {}".format(self.info["temp2"]))
        print("Temp3: {}".format(self.info["temp3"]))
        print("Temp4: {}".format(self.info["temp4"]))
        print("Wind: {}".format(self.info["wind"]))
        print("Fog: {}".format(self.info["fog"]))
        print("Rain: {}".format(self.info["rain"]))
        print("Snow: {}".format(self.info["snow"]))
        print("Hail: {}".format(self.info["hail"]))
