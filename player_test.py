"""CS 108 Final Project testing

This module runs basic tests on the player class

@author: Ben Kosters (bak32)
@author: Tyler Bylsma (tjb65)
@date: December, 2022
"""

from player import Player

player1 = Player()
assert player1.get_lives() == 3
assert player1.get_score() == 0
assert player1.get_name() == ""

player1.remove_life()
player1.increment_score()
player1.set_name("Ben")


assert player1.get_lives() == 2
assert player1.get_score() == 1
assert player1.get_name() == "Ben"

print('pass')
