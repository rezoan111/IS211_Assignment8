import argparse
import random
import time

# use same random seed for testing
random.seed(0)


# this class is the base class for all players
# it will store player name and total score
class Player:
    def __init__(self, name):
        self.name = name
        self.score = 0


# this class is for a human player
# it will ask the user to roll or hold
class HumanPlayer(Player):
    def get_move(self, turn_score):
        return input(self.name + ": roll or hold? (r/h): ").lower()


# this class is for the computer player
# it will follow the strategy from the assignment
class ComputerPlayer(Player):
    def get_move(self, turn_score):
        hold_at = min(25, 100 - self.score)

        if turn_score >= hold_at:
            print(self.name + " chooses: h")
            return "h"
        else:
            print(self.name + " chooses: r")
            return "r"


# this class is the factory for creating players
# it will return a human player or computer player
class PlayerFactory:
    @staticmethod
    def create_player(player_type, name):
        if player_type == "human":
            return HumanPlayer(name)
        elif player_type == "computer":
            return ComputerPlayer(name)
        else:
            raise ValueError("player type must be human or computer")


# this class is for the die
# it will roll a number from 1 to 6
class Die:
    def roll(self):
        return random.randint(1, 6)


# this class is for the game
# it will create players and one die
class Game:
    def __init__(self, player1_type, player2_type):
        self.player1 = PlayerFactory.create_player(player1_type, "Player 1")
        self.player2 = PlayerFactory.create_player(player2_type, "Player 2")
        self.die = Die()

    # this function will switch the current player
    def get_other_player(self, current_player):
        if current_player == self.player1:
            return self.player2
        else:
            return self.player1

    # this function will handle one player's turn
    # it will keep track of the turn score
    def take_turn(self, player):
        turn_score = 0

        while True:
            choice = player.get_move(turn_score)

            if choice == "r":
                roll_value = self.die.roll()
                print(player.name + " rolled: " + str(roll_value))

                if roll_value == 1:
                    turn_score = 0
                    print("turn score: " + str(turn_score))
                    print("total score: " + str(player.score))
                    print(player.name + " rolled a 1. turn is over.")
                    print()
                    return
                else:
                    turn_score += roll_value
                    print("turn score: " + str(turn_score))
                    print("total score: " + str(player.score))
                    print()

            elif choice == "h":
                player.score += turn_score
                print(player.name + " holds.")
                print("turn score: " + str(turn_score))
                print("total score: " + str(player.score))
                print()
                return

            else:
                print("invalid input. enter r or h.")
                print()

    # this function will run the full game
    # it will keep going until one player gets 100 or more
    def play(self):
        current_player = self.player1

        while self.player1.score < 100 and self.player2.score < 100:
            print(current_player.name + "'s turn")
            print("current total score: " + str(current_player.score))
            print()

            self.take_turn(current_player)

            if current_player.score >= 100:
                print(current_player.name + " wins with " + str(current_player.score) + " points!")
                return

            current_player = self.get_other_player(current_player)


# this class is the proxy for the game
# it will run the same game but with a 1 minute limit
class TimedGameProxy:
    def __init__(self, game):
        self.game = game
        self.start_time = time.time()

    # this lets the proxy use the game attributes
    def __getattr__(self, name):
        return getattr(self.game, name)

    # this function will check if time is up
    def time_is_up(self):
        return time.time() - self.start_time >= 60

    # this function will print the winner when time ends
    def print_timed_winner(self):
        print("time is up.")

        if self.game.player1.score > self.game.player2.score:
            print(self.game.player1.name + " wins with " + str(self.game.player1.score) + " points!")
        elif self.game.player2.score > self.game.player1.score:
            print(self.game.player2.name + " wins with " + str(self.game.player2.score) + " points!")
        else:
            print("the game is a tie at " + str(self.game.player1.score) + " points each!")

    # this function will handle one player's turn
    # it will also check if the time is over
    def take_turn(self, player):
        turn_score = 0

        while True:
            if self.time_is_up():
                return "time"

            choice = player.get_move(turn_score)

            if self.time_is_up():
                return "time"

            if choice == "r":
                roll_value = self.game.die.roll()
                print(player.name + " rolled: " + str(roll_value))

                if roll_value == 1:
                    turn_score = 0
                    print("turn score: " + str(turn_score))
                    print("total score: " + str(player.score))
                    print(player.name + " rolled a 1. turn is over.")
                    print()
                    return "done"
                else:
                    turn_score += roll_value
                    print("turn score: " + str(turn_score))
                    print("total score: " + str(player.score))
                    print()

            elif choice == "h":
                player.score += turn_score
                print(player.name + " holds.")
                print("turn score: " + str(turn_score))
                print("total score: " + str(player.score))
                print()
                return "done"

            else:
                print("invalid input. enter r or h.")
                print()

    # this function will run the timed game
    def play(self):
        current_player = self.game.player1

        while self.game.player1.score < 100 and self.game.player2.score < 100:
            if self.time_is_up():
                self.print_timed_winner()
                return

            print(current_player.name + "'s turn")
            print("current total score: " + str(current_player.score))
            print()

            result = self.take_turn(current_player)

            if result == "time":
                self.print_timed_winner()
                return

            if current_player.score >= 100:
                print(current_player.name + " wins with " + str(current_player.score) + " points!")
                return

            current_player = self.game.get_other_player(current_player)


if __name__ == "__main__":
    parser = argparse.ArgumentParser()

    # these arguments decide if each player is human or computer
    parser.add_argument("--player1", choices=["human", "computer"], default="human")
    parser.add_argument("--player2", choices=["human", "computer"], default="human")

    # this argument turns on the timed version
    parser.add_argument("--timed", action="store_true")

    args = parser.parse_args()

    base_game = Game(args.player1, args.player2)

    if args.timed:
        game = TimedGameProxy(base_game)
    else:
        game = base_game

    game.play()
