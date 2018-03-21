import json
import logging
import os
import socket
from time import sleep

import requests

logger = logging.getLogger('driver')

offensive_stat_history = "\\resources\offensiveHistory.json"


class GameStats:

    def __init__(self, player_id, game_id):
        self.rush_attemps = 0
        self.rush_yards = 0
        self.rush_tds = 0
        self.targets = 0
        self.receptions = 0
        self.receiving_yards = 0
        self.receiving_tds = 0
        self.pass_attemps = 0
        self.pass_completions = 0
        self.pass_yards = 0
        self.pass_tds = 0
        self.interceptions_thrown = 0
        self.fumbles_lost = 0
        self.game_id = game_id
        self.player_id = player_id
        self.opponent = ""
        self.player_name = ""
        self.team_name = ""

    def print_JSON(self, open_file):
        open_file.write("\"{}\": {{\"rush_attemps\": {}, \"rush_yards\": {}, \"rush_tds\": {}, "
                        "\"targets\": {},\"receptions\": {}, \"receiving_yards\": {}, \"receiving_tds\": "
                        "{}, \"pass_attemps\": {},\"pass_completions\": {}, \"pass_yards\": {}, "
                        "\"pass_tds\": {}, \"interceptions_thrown\": {}, \"fumbles_lost\": {}, "
                        "\"player_id\": \"{}\", \"opponent\": \"{}\", \"player_name\": \"{}\", \"team_name\": \"{}\", "
                        "\"game_id\": \"{}\"}}".format(self.game_id, self.rush_attemps, self.rush_yards, self.rush_tds,
                                                     self.targets, self.receptions, self.receiving_yards,
                                                     self.receiving_tds, self.pass_completions, self.pass_attemps,
                                                     self.pass_yards, self.pass_tds, self.interceptions_thrown,
                                                     self.fumbles_lost, self.player_id, self.opponent, self.player_name,
                                                     self.team_name, self.game_id))

    def set_all_stats(self, rush_attemps, rush_yards, rush_tds, targets, receptions, receiving_yards, receiving_tds,
                      pass_attemps, pass_completions, pass_yards, pass_tds, interceptions_thrown, fumbles_lost, game_id,
                      opponent, player_id, player_name, team_name):
        self.rush_attemps = rush_attemps
        self.rush_yards = rush_yards
        self.rush_tds = rush_tds
        self.targets = targets
        self.receptions = receptions
        self.receiving_yards = receiving_yards
        self.receiving_tds = receiving_tds
        self.pass_attemps = pass_attemps
        self.pass_completions = pass_completions
        self.pass_yards = pass_yards
        self.pass_tds = pass_tds
        self.interceptions_thrown = interceptions_thrown
        self.fumbles_lost = fumbles_lost
        self.game_id = game_id
        self.opponent = opponent
        self.player_id = player_id
        self.player_name = player_name
        self.team_name = team_name

    def update_stats(self, game):
        self.rush_attemps += game.rush_attemps
        self.rush_yards += game.rush_yards
        self.rush_tds += game.rush_tds
        self.targets += game.targets
        self.receptions += game.receptions
        self.receiving_yards += game.receiving_yards
        self.receiving_tds += game.receiving_tds
        self.pass_attemps += game.pass_attemps
        self.pass_completions += game.pass_completions
        self.pass_yards += game.pass_yards
        self.pass_tds += game.pass_tds
        self.interceptions_thrown += game.interceptions_thrown
        self.fumbles_lost += game.fumbles_lost

    def update_stats_dict(self, game):
        self.rush_attemps += game["rush_attemps"]
        self.rush_yards += game["rush_yards"]
        self.rush_tds += game["rush_tds"]
        self.targets += game["targets"]
        self.receptions += game["receptions"]
        self.receiving_yards += game["receiving_yards"]
        self.receiving_tds += game["receiving_tds"]
        self.pass_attemps += game["pass_attemps"]
        self.pass_completions += game["pass_completions"]
        self.pass_yards += game["pass_yards"]
        self.pass_tds += game["pass_tds"]
        self.interceptions_thrown += game["interceptions_thrown"]
        self.fumbles_lost += game["fumbles_lost"]

    def print_game_stats(self):
        print("Player Name: {}".format(self.player_name))
        print("Player ID: {}".format(self.player_id))
        print("Game ID: {}".format(self.game_id))
        print("Opponent: {}".format(self.opponent))
        print("Rush Attemps: {}".format(self.rush_attemps))
        print("Rush Yards: {}".format(self.rush_yards))
        print("Rush TDs: {}".format(self.rush_tds))
        print("Targets: {}".format(self.targets))
        print("Receptions: {}".format(self.receptions))
        print("Receiving Yards: {}".format(self.receiving_yards))
        print("Receiving TDs: {}".format(self.receiving_tds))
        print("Pass Attemps: {}".format(self.pass_attemps))
        print("Pass Completions: {}".format(self.pass_completions))
        print("Pass Yards: {}".format(self.pass_yards))
        print("Pass TDs: {}".format(self.pass_tds))
        print("Interceptions Thrown: {}".format(self.interceptions_thrown))
        print("Fumbles Lost: {}".format(self.fumbles_lost))
        print("")

    # Getters
    def get_player_name(self):
        return self.player_name

    def get_team_name(self):
        return self.team_name

    def get_rush_attempts(self):
        return self.rush_attemps

    def get_rush_yards(self):
        return self.rush_yards

    def get_rush_tds(self):
        return self.rush_tds

    def get_targets(self):
        return self.targets

    def get_receptions(self):
        return self.receptions

    def get_receiving_yards(self):
        return self.receiving_yards

    def get_receiving_tds(self):
        return self.receiving_tds

    def get_pass_attemps(self):
        return self.pass_attemps

    def get_pass_completions(self):
        return self.pass_completions

    def get_pass_yards(self):
        return self.pass_yards

    def get_pass_tds(self):
        return self.pass_tds

    def get_interceptions_thrown(self):
        return self.interceptions_thrown

    def get_fumbles_lost(self):
        return self.fumbles_lost

    def get_game_id(self):
        return self.game_id

    def get_opponent(self):
        return self.opponent

    # Setters
    def set_player_name(self, player_name):
        self.player_name = player_name

    def set_team_name(self, team_name):
        self.team_name = team_name

    def set_rush_attempts(self, rush_attemps):
        self.rush_attemps = rush_attemps

    def set_rush_yards(self, rush_yards):
        self.rush_yards = rush_yards

    def set_rush_tds(self, rush_tds):
        self.rush_tds = rush_tds

    def set_targets(self, targets):
        self.targets = targets

    def set_receptions(self, receptions):
        self.receptions = receptions

    def set_receiving_yards(self, receiving_yards):
        self.receiving_yards = receiving_yards

    def set_receiving_tds(self, receiving_tds):
        self.receiving_tds = receiving_tds

    def set_pass_attemps(self, pass_attemps):
        self.pass_attemps = pass_attemps

    def set_pass_completions(self, pass_completions):
        self.pass_completions = pass_completions

    def set_pass_yards(self, pass_yards):
        self.pass_yards = pass_yards

    def set_pass_tds(self, pass_tds):
        self.pass_tds = pass_tds

    def set_interceptions_thrown(self, interceptions_thrown):
        self.interceptions_thrown = interceptions_thrown

    def set_fumbles_lost(self, fumbles_lost):
        self.fumbles_lost = fumbles_lost

    def set_game_id(self, game_id):
        self.game_id = game_id

    def set_opponent(self, opponent):
        self.opponent = opponent


class OffensiveStats:

    def __init__(self, base_path):

        self.num_players = 0
        self.indv_games = 0
        self.base_path = base_path
        self.players = dict()
        self.games_ids = []
        self.non_game_days = []
        self.player_lookup = dict()
        if os.path.isfile("{}{}".format(base_path, offensive_stat_history)):
            logger.info("Stats file exists, loading data into a dictionary")
            read_file = open("{}{}".format(base_path, offensive_stat_history), "r")
            json_file = json.loads(read_file.read())

            for player in json_file["players"]:
                cur_p = Player(player, "", "")
                for game in json_file["players"][player]["games"]:
                    if game == "overall":
                        pass
                    else:
                        if game not in self.games_ids:
                            self.games_ids.append(game)
                            logger.debug("Adding game {} to the lookup list".format(game))
                        cur_gs = GameStats(player, game)
                        cur_gs.update_stats_dict(json_file["players"][player]["games"][game])
                        cur_gs.set_player_name(json_file["players"][player]["games"][game]["player_name"])
                        cur_p.name = json_file["players"][player]["games"][game]["player_name"]
                        cur_p.add_game(cur_gs)
                self.players[cur_p.p_id] = cur_p
                self.player_lookup[cur_p.name] = cur_p.p_id

            for non_gd in json_file["non_game_days"]:
                self.non_game_days.append(non_gd)

        else:
            logger.info("Stats storage file not found. Will create one when program is closed.")

    def store_stats(self):
        write_file = open("{}{}".format(self.base_path, offensive_stat_history), "w+")
        write_file.write("{\"players\":{")

        sz = len(self.players)
        i = 1
        for player in self.players:
            self.players[player].print_JSON(write_file)
            write_file.write("}")
            if i < sz:
                i += 1
                write_file.write(",")

        write_file.write("}, \"non_game_days\": [")
        sz = len(self.non_game_days)
        i = 1
        for game in self.non_game_days:
            write_file.write("{}".format(game))
            if i < sz:
                i += 1
                write_file.write(",")
        write_file.write("]}")

    def add_stats(self, stats: GameStats):
        if stats.player_id not in self.players:
            self.players[stats.player_id] = Player(stats.player_id, "", "")
            logger.debug("Added a new player with {} to the database".format(stats.player_id))
            self.num_players += 1

        if stats.game_id not in self.players[stats.player_id].games:
            self.players[stats.player_id].games[stats.game_id] = stats
            logger.debug("Added a new game {} for {} to the database".format(stats.game_id,
                                                                             stats.player_name))
            self.indv_games += 1
        else:
            self.players[stats.player_id].games[stats.game_id].update_stats(stats)
            logger.debug("Updating game {} to player {}".format(stats.game_id, stats.player_name))


class Player:

    def __init__(self, p_id, name, position):
        self.p_id = p_id
        self.name = name
        self.position = position
        self.games = dict()

    def print_JSON(self, open_file):
        overall = GameStats(self.p_id, "overall")
        open_file.write("\"{}\": {{\"name\": \"{}\", \"games\": {{".format(self.p_id, self.name))
        sz = len(self.games.keys())
        i = 1
        for player in self.games:
            overall.update_stats(self.games[player])
            self.games[player].print_JSON(open_file)
            open_file.write(",")
        overall.print_JSON(open_file)
        if overall.pass_attemps > overall.rush_attemps and overall.pass_attemps > overall.targets:
            self.position = "QB"
        else:
            if overall.rush_attemps > overall.targets:
                self.position = "RB"
            else:
                self.position = "WR"
        open_file.write("}}, \"position\": \"{}\"".format(self.position))

    # Add a game for the specific player
    def add_game(self, game: GameStats):
        if game.game_id not in self.games:
            self.games[game.game_id] = game
        else:
            logger.debug("Attempted to add duplicate game for ({}) on {}".format(self.name, game.game_id))

    def get_key(self):
        return "%d" % self.p_id


class StatReader:

    def __init__(self, game_id, master: OffensiveStats):
        self.game_id = game_id
        self.masterStats = master
        self.haveFailed = 0
        try:
            self.haveFailed = 0
            self.request = requests.get("http://www.nfl.com/liveupdate/game-center/{}/{}_gtd.json".format(game_id,
                                                                                                          game_id))
            sleep(.5)
            self.status = self.request.status_code
            if self.request.status_code == 200:
                self.stats = json.loads(self.request.text)["{}".format(self.game_id)]
        except socket.gaierror:
            logger.error("Unable to create new connection for game stats {})".format(game_id))
            self.haveFailed = 1
            sleep(1)

    def reattempt_connection(self):
        try:
            self.request = requests.get("http://www.nfl.com/liveupdate/game-center/{}/{}_gtd.json".format(self.game_id,
                                                                                                          self.game_id))
            sleep(.5)
            self.status = self.request.status_code
            if self.request.status_code == 200:
                self.stats = json.loads(self.request.text)["{}".format(self.game_id)]
        except socket.gaierror:
            logger.error("Unable to create new connection for game stats {})".format(self.game_id))
            self.haveFailed += 1
            sleep(1)

    def get_offensive_players(self):

        home_abbr = self.stats["home"]["abbr"]
        away_abbr = self.stats["away"]["abbr"]

        home_team = "home"
        away_team = "away"

        for player_id in self.stats["home"]["stats"]["passing"]:
            game = self.get_player_stats(player_id, home_team, home_abbr, away_abbr)
            self.masterStats.add_stats(game)

        for player_id in self.stats[home_team]["stats"]["rushing"]:
            game = self.get_player_stats(player_id, home_team, home_abbr, away_abbr)
            self.masterStats.add_stats(game)

        for player_id in self.stats[home_team]["stats"]["receiving"]:
            game = self.get_player_stats(player_id, home_team, home_abbr, away_abbr)
            self.masterStats.add_stats(game)

        for player_id in self.stats[away_team]["stats"]["passing"]:
            game = self.get_player_stats(player_id, away_team, away_abbr, home_team)
            self.masterStats.add_stats(game)

        for player_id in self.stats[away_team]["stats"]["rushing"]:
            game = self.get_player_stats(player_id, away_team, away_abbr, home_team)
            self.masterStats.add_stats(game)

        for player_id in self.stats[away_team]["stats"]["receiving"]:
            game = self.get_player_stats(player_id, away_team, away_abbr, home_team)
            self.masterStats.add_stats(game)

    def get_player_stats(self, player_id, team, team_abbr, opp_team):

        game = GameStats(player_id, self.game_id)

        if player_id in self.stats[team]["stats"]["passing"]:
            passing_stats = self.stats[team]["stats"]["passing"][player_id]

            if game.get_player_name() == "":
                game.set_player_name(passing_stats["name"])

            game.set_pass_attemps(passing_stats["att"])
            game.set_pass_completions(passing_stats["cmp"])
            game.set_interceptions_thrown(passing_stats["ints"])
            game.set_pass_tds(passing_stats["tds"])
            game.set_pass_yards(passing_stats["yds"])

        if player_id in self.stats[team]["stats"]["rushing"]:
            rushing_stats = self.stats[team]["stats"]["rushing"][player_id]

            if game.get_player_name() == "":
                game.set_player_name(rushing_stats["name"])

            game.set_rush_attempts(rushing_stats["att"])
            game.set_rush_tds(rushing_stats["tds"])
            game.set_rush_yards(rushing_stats["yds"])

        if player_id in self.stats[team]["stats"]["receiving"]:
            receiving_stats = self.stats[team]["stats"]["receiving"][player_id]

            if game.get_player_name() == "":
                game.set_player_name(receiving_stats["name"])

            game.set_receptions(receiving_stats["rec"])
            game.set_receiving_tds(receiving_stats["tds"])
            game.set_receiving_yards(receiving_stats["yds"])

        if "fumbles" in self.stats[team]["stats"]:
            if player_id in self.stats[team]["stats"]["fumbles"]:

                if game.get_player_name() == "":
                    game.set_player_name(self.stats[team]["stats"]["fumbles"][player_id]["name"])

                game.set_fumbles_lost(self.stats[team]["stats"]["fumbles"][player_id]["lost"])

        if game.get_team_name() == "":
            game.set_team_name(team_abbr)

        if game.get_opponent() == "":
            game.set_opponent(opp_team)

        return game
