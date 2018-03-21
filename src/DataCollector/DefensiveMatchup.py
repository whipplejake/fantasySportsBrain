import json
import logging
import os
import socket
from time import sleep

import requests

from DataCollector.Weather import stadiums

logger = logging.getLogger('driver')


class DefensiveMatchup:

    def __init__(self, base_path):
        self.rankings = dict()
        self.base_path = base_path
        if os.path.isfile("{}{}".format(base_path, "\\resources\defensiveHistory.json")):
            read_file = open("{}{}".format(base_path, "\\resources\defensiveHistory.json"), "r")
            self.rankings = json.loads(read_file.read())
        else:
            for team in stadiums:
                self.rankings[team] = dict()

    # need to fix
    def get_rankings(self):
        for i in range(1, 17):
            try:
                request = requests.get(
                    "https://www.fantasyfootballnerd.com/service/weekly-rankings/json/egg8hua3s62r/DEF/{}/0/".format(i))
                sleep(.5)
                logger.info("getting Rankings for week {}".format(i))
                if request.status_code == 200:
                    def_rankings = json.loads(request.text)["Rankings"]
                    for rank in def_rankings:
                        logger.info("Rank: {}".format(rank))
                        for team in stadiums:
                            if i not in self.rankings[team]:
                                self.rankings[team]["{}".format(i)] = -1
                            if team == self.rankings[rank["team"]]:
                                self.rankings[team]["{}".format(i)] = 1
            except socket.gaierror:
                logger.error("Unable to get DEF rankings for week {}".format(i))
                return
            except requests.exceptions.ConnectionError:
                logger.error("Unable to get DEF rankings for week {}".format(i))
        write_file = open("{}{}".format(self.base_path, "\\resources\defensiveHistory.json"), "w+")
        write_file.write("{}".format(json.dumps(self.rankings)))

