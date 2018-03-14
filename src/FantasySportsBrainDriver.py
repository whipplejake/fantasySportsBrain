import os

import sys

from DataCollector.OffensiveStats import OffensiveStats, StatReader
from DataCollector.Weather import WeatherStats, stadiums
from src import log

logger = log.setup_custom_logger('driver')
sys.setrecursionlimit(5000)

def get_stats():

    game_count = 0
    master_stats = OffensiveStats(os.getcwd())
    weather = WeatherStats(os.getcwd())
    logger.setLevel(10)

    # year starting with 2000 Completed 2016/17 on 3/13/2018 (10 am) - need to be careful about calls per day
    # for weather api

    for y in range(16, 18):
        # months
        for l in range(1, 13):
            # days in a month
            for k in range(0, 33):
                # games per day
                for i in range(0, 17):
                    try:
                        id = (2000 + y) * 1000000
                        date = (2000 + y) * 10000 + l * 100 + k
                        game_id = id + l * 10000 + k * 100 + i
                        if game_id not in master_stats.games_ids and game_id not in master_stats.non_game_days:
                            stats = StatReader(game_id, master_stats)
                            if stats.status == 200:
                                game_count += 1
                                logger.info("Game Count ({}) ID: ({})".format(game_count, game_id))
                                stats.get_offensive_players()
                                weather.get_new_weather_stats(game_id, stadiums[stats.stats["home"]["abbr"]]["city"],
                                                              stadiums[stats.stats["home"]["abbr"]]["state"],
                                                              date, 10)
                            else:
                                master_stats.non_game_days.append(game_id)
                                logger.info("Adding game to non game day list: ({})".format(stats.status))
                                break
                        else:
                            logger.debug("Gamestats have already been entered for game with id {}".format(game_id))
                    except KeyError as err:
                        logger.info("{}".format(err))
                    except TypeError as err:
                        logger.info("{}".format(err))
    weather.store_weather()
    master_stats.store_stats()

    #logger.info("Total number of players added to the database was {} with {} game stats".format(
    #    master_stats.num_players, master_stats.indv_games))


if __name__ == '__main__':
    logger.info("Starting application")
    get_stats()

    logger.info("Application ending")
