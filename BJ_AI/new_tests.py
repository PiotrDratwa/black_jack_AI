from new_train_test import player, two, shuffle_deck
import unittest
import numpy as np
import pandas as pd
import time

class TestGroupByMethods(unittest.TestCase):

    def test_shuffle_deck(self):
        deck = shuffle_deck()
        self.assertEqual(len(deck), 52, f'There should be 52 cards in a deck and there is:{len(deck)}')
        if np.all(deck[:4] == two) == True:
            deck = shuffle_deck()
            self.assertEqual(deck[:4] == [two,two,two,two], 'The deck probably is not shuffled')

    def test_draw_card(self):
        global deck
        deck = shuffle_deck()
        bot = player()
        for _ in range(2):
            bot.draw_card()
        self.assertTrue(bot.hand < 22, f'player hand should be below 22 and above 0 after two draws. hand = {bot.hand}')
        self.assertTrue(bot.hand > 0, "hand should be above 0")

    def test_check_genes(self):
        bot = player()
        self.assertFalse(bot.check_genes(18), 'check genes should return false, if there are not any genes')
        bot.hand = 5
        bot.genomes = [[18, 21],[5,17]]
        self.assertTrue(bot.check_genes(17) == 1, "check genes should return index = 1")
        self.assertFalse(bot.check_genes(18), "check genes should return false, if there are not any according genes")

    def test_new_hit(self):
        deck = shuffle_deck()
        bot = player()
        croupier = player()
        croupier.hand = 10
        bot.hand = 13
        bot.check_genes(croupier.hand)
        new_hands = np.empty(10)
        for i in range(10):
            bot.hit(deck)
            new_hands[i] = bot.hand
            bot.hand = 13
        self.assertTrue(bot.genomes[0][0]%1 == 0, f'bot did not add new genes:{bot.genomes[0]}')

        deck = shuffle_deck()
        bot = player()
        croupier = player()
        croupier.hand = 10
        bot.hand = 13
        bot.check_genes(croupier.hand)
        new_hands = np.empty(10)
        for i in range(10):
            bot.hit(deck)
            new_hands[i] = bot.hand
            bot.hand = 13
        self.assertTrue(bot.genomes[0][2]%1 == 0, f'bot did not add new genes:{bot.genomes[0]}')

        bot.genomes[0] = [1,10,0]
        bot.genomes[1] = [13,10,1]
        gene = bot.check_genes(croupier.hand)
        bot.hit(deck, gene)
        self.assertTrue(bot.hand > 13, f'bot did not hit when genes told him so: {bot.hand}')
        bot.hand = 13
        bot.genomes[1] = [13,10,0]
        gene = bot.check_genes(croupier.hand)
        bot.hit(deck, gene)
        self.assertTrue(bot.hand == 13, f'bot did not stay when genes told him so: {bot.hand}')
        bot = player()
        bot.hand = 13
        bot.genomes[0] = [13,10,1]
        gene = bot.check_genes(croupier.hand)
        bot.hit(deck, gene)
        self.assertTrue(bot.genomes[1][0]%1 == 0, f'bot did not add new genes after hitting:{bot.genomes[0]}')

deck = shuffle_deck()
test = TestGroupByMethods()
test.test_new_hit()
#time.sleep(0.00000001
test.test_shuffle_deck()