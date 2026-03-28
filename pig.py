import random

# use same random seed for testing
random.seed(0)


# this class is for each player
# it will store player name and total score
class Player:
    def __init__(self, name):
        self.name = name
        self.score = 0


# this class is for the die
# it will roll a number from 1 to 6
class Die:
    def roll(self):
        return random.randint(1, 6)


# this class is for the game
# it will create 2 players and 1 die
class Game:
    def __init__(self):
        self.player1 = Player("Player 1")
        self.player2 = Player("Player 2")
        self.die = Die()

    # this function will handle one player's turn
    # it will keep track of the turn score
    def take_turn(self, player):
        turn_score = 0

        while True:
            choice = input(player.name + ": roll or hold? (r/h): ").lower()

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
                break

            if current_player == self.player1:
                current_player = self.player2
            else:
                current_player = self.player1


if __name__ == "__main__":
    game = Game()
    game.play()
