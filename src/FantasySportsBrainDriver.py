import os

from AnalysisEngine.Train import Trainer
from DataCollector.DefensiveMatchup import DefensiveMatchup
from DataCollector.OffensiveStats import OffensiveStats, StatReader
from DataCollector.Weather import WeatherStats, stadiums
from src import log

logger = log.setup_custom_logger('driver')

# egg8hua3s62r : FFN kkey

master_stats = OffensiveStats(os.getcwd())
weather = WeatherStats(os.getcwd())
matchup = DefensiveMatchup(os.getcwd())


def get_stats(start: int, stop: int):

    game_count = 0
    logger.setLevel(20)

    # year starting with 2000 Completed 2016/17 on 3/13/2018 (10 am) - need to be careful about calls per day
    # for weather api

    for y in range(start, stop):
        # months
        rang = (1, 2, 9, 10, 11, 12)
        for l in rang:
            # days in a month
            for k in range(0, 33):
                # games per day
                for i in range(0, 17):
                    try:
                        id = (2000 + y) * 1000000
                        date = (2000 + y) * 10000 + l * 100 + k
                        game_id = id + l * 10000 + k * 100 + i
                        if game_id not in master_stats.non_game_days:
                            if game_id not in master_stats.games_ids:
                                stats = StatReader(game_id, master_stats)
                                if stats.haveFailed:
                                    stats.reattempt_connection()
                                if stats.haveFailed == 2:
                                    logger.error("Failed getting game stats for {}, exiting....".format(game_id))
                                    weather.store_weather()
                                    master_stats.store_stats()
                                    return
                                if stats.status == 200:
                                    game_count += 1
                                    logger.info("Game Count ({}) ID: ({})".format(game_count, game_id))
                                    stats.get_offensive_players()
                                    weather.get_new_weather_stats(game_id, stadiums[stats.stats["home"]["abbr"]]["city"],
                                                                  stadiums[stats.stats["home"]["abbr"]]["state"],
                                                                  date, 10)
                                else:
                                    master_stats.non_game_days.append(game_id)
                                    logger.info("Adding game to non game day list: ({}:{})".format(game_id, stats.status))
                                    break
                            else:
                                logger.debug("Gamestats have already been entered for game with id {}".format(game_id))
                        else:
                            logger.debug("Game in non-game list: ({})".format(game_id))
                            break
                    except KeyError as err:
                        logger.error("KeyError: {}".format(err))
                    except TypeError as err:
                        logger.error("TypeError: {}".format(err))
    weather.store_weather()
    master_stats.store_stats()

    #logger.info("Total number of players added to the database was {} with {} game stats".format(
    #    master_stats.num_players, master_stats.indv_games))


def print_options():
    print("     Options")
    print("")
    print("         (t)rain - To train the model based on input paramters")
    print("         (p)redict - Enter pairs of players for suggestions")
    print("         (e)xit - end application")
    print("")
    print("   ---------------------------------------   ")


def print_welcome():
    print("")
    print("")
    print("Welcome to Fantasy Football Brain...")
    print("What would you like to do?")
    print("")


def train():

    trainer = Trainer()
    if trainer.exit:
        return

def main():

    print_welcome()
    print_options()

    while 1:
        text = input("Please enter what you would like to do \n\n>")

        if (text == "p") | (text == "predict"):
            print("Please enter two players that are the same position (QB, RB, WR)\n")
            player_string = input("Format expected <player1> <player2>")
        elif (text == "t") | (text == "train"):
            trainer = Trainer()
            trainer.collect_data(os.getcwd())
            trainer.train(os.getcwd())
        elif (text == "e") | (text == "exit"):
            print("")
            break
        else:
            print("")
            print("  Error: please enter a valid option")
            print_options()
            print("")

    print("")
    print("Exiting....")

    # master_stats = OffensiveStats(os.getcwd())
    # weather = WeatherStats(os.getcwd())
    # matchup = DefensiveMatchup(os.getcwd())
    # master_stats.store_stats()
    # populate statistics between the parameter years (format: 20xx to 20yy where getStats(xx, yy)
    # get_stats(14, 15)

    # write analytical questions



if __name__ == '__main__':
    logger.info("Starting application")
    main()
    logger.info("Application ending")
