#!/usr/bin/env python3

"""This program plays a game of Rock, Paper, Scissors between two Players,
and reports both Player's scores each round."""

import random
import time

try:
    from colorama import Fore, Style, init
    init(autoreset=True)
except ImportError:
    class Fore:
        RED = '\033[31m'
        GREEN = '\033[32m'
        YELLOW = '\033[33m'
        BLUE = '\033[34m'
        MAGENTA = '\033[35m'
        CYAN = '\033[36m'
        WHITE = '\033[37m'

moves = ['rock', 'paper', 'scissors']

"""The Player class is the parent class for all of the Players
in this game"""


def print_pause(message, color=Fore.WHITE):
    print(color + message)
    time.sleep(1.5)


class Player:
    def move(self):
        return 'rock'

    def learn(self, my_move, their_move):
        pass


class RockPlayer(Player):
    def move(self):
        return 'rock'


class RandomPlayer(Player):
    def move(self):
        return random.choice(moves)


class HumanPlayer(Player):
    def move(self):
        move = input(Fore.CYAN + "Enter your move "
                     "(rock, paper, scissors): ").lower()
        while move not in moves:
            move = input(Fore.RED + "Invalid move."
                         " Enter your move (rock, paper, scissors): ").lower()
        return move


class ReflectPlayer(Player):
    def __init__(self):
        self.their_move = None

    def move(self):
        if self.their_move is None:
            return random.choice(moves)
        return self.their_move

    def learn(self, my_move, their_move):
        self.their_move = their_move


class CyclePlayer(Player):
    def __init__(self):
        self.my_move = random.choice(moves)

    def move(self):
        move = self.my_move
        self.my_move = moves[(moves.index(self.my_move) + 1) % 3]
        return move


def beats(one, two):
    return ((one == 'rock' and two == 'scissors') or
            (one == 'scissors' and two == 'paper') or
            (one == 'paper' and two == 'rock'))


class Game:
    def __init__(self, p1, p2):
        self.p1 = p1
        self.p2 = p2
        self.p1_score = 0
        self.p2_score = 0

    def play_round(self):
        move1 = self.p1.move()
        move2 = self.p2.move()
        print(Fore.YELLOW + f"Player 1st: {move1}  Player 2nd: {move2}")
        if beats(move1, move2):
            print(Fore.GREEN + "Player 1st wins this round!")
            self.p1_score += 1
        elif beats(move2, move1):
            print(Fore.BLUE + "Player 2nd wins this round!")
            self.p2_score += 1
        else:
            print(Fore.MAGENTA + "It's a tie!")
        self.p1.learn(move1, move2)
        self.p2.learn(move2, move1)
        print(Fore.CYAN + f"Score: Player 1st = {self.p1_score},"
              f" Player 2nd = {self.p2_score}")

    def play_game(self):
        print(Fore.YELLOW + "Game start!")
        rounds = self.get_valid_rounds()
        for round in range(rounds):
            print(Fore.YELLOW + f"Round {round + 1}:")
            self.play_round()
        print(Fore.YELLOW + "Game over!")
        print(Fore.CYAN + f"Final Score: Player 1st = {self.p1_score}, "
              f"Player 2nd = {self.p2_score}")
        if self.p1_score > self.p2_score:
            print(Fore.GREEN + "Player 1st wins the game!")
        elif self.p2_score > self.p1_score:
            print(Fore.BLUE + "Player 2nd wins the game!")
        else:
            print(Fore.MAGENTA + "The game is a tie!")

    def get_valid_rounds(self):
        while True:
            try:
                rounds = int(input(Fore.CYAN + "Enter "
                                   "number of rounds to play: "))
                if rounds > 0:
                    return rounds
                else:
                    print(Fore.RED + "Please enter a positive integer.")
            except ValueError:
                print(Fore.RED + "Invalid input. "
                      "Please enter a positive integer.")


if __name__ == '__main__':
    players = {
        "1": RockPlayer,
        "2": RandomPlayer,
        "3": ReflectPlayer,
        "4": CyclePlayer,
        "5": HumanPlayer
    }

    print(Fore.YELLOW + "Player type: ")
    print_pause("(1) Rock Player: Always plays 'rock'", Fore.YELLOW)
    print_pause("(2) Random Player: This player relies purely "
                "on randomness for its moves.", Fore.YELLOW)
    print_pause("(3) Reflect Player: This player remembers the"
                " opponent's move from the previous round and plays "
                "that move in the next round.", Fore.YELLOW)
    print_pause("(4) Cycle Player: This player cycles through "
                "the three moves in order"
                " (rock, paper, scissors).", Fore.YELLOW)
    print_pause("(5) Human Player: This player represents a "
                "human user who inputs their move via the "
                "keyboard.", Fore.YELLOW)

    p1_choice = input(Fore.CYAN + "Enter choice for Player 1st (1-5): ")
    while p1_choice not in players:
        p1_choice = input(Fore.RED + "Invalid choice. "
                          "Enter choice for Player 1st: ")

    p2_choice = input(Fore.CYAN + "Enter choice for Player 2nd (1-5): ")
    while p2_choice not in players:
        p2_choice = input(Fore.RED + "Invalid choice."
                          " Enter choice for Player 2nd: ")

    p1 = players[p1_choice]()
    p2 = players[p2_choice]()

    game = Game(p1, p2)
    game.play_game()
