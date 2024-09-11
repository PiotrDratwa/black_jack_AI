import numpy as np
from new_train_test import player, shuffle_deck, card

two = card(2)
three = card(3)
four = card(4)
five = card(5)
six = card(6)
seven = card(7)
eight = card(8)
nine = card(9)
ten = card(10)
jack = card(10)
queen = card(10)
king = card(10)
ace = card(11)
deck = shuffle_deck()

bot = player()

bot.check_genes(10)
bot.hit(deck)