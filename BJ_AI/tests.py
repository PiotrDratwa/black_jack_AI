from Train_Test import two, player, shuffle_deck
import unittest
import numpy as np
import pandas as pd

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
    
    def test_result_check(self):
        bot = player()
        bot.hand = 2
        bot.result_check(2)
        self.assertTrue(bot.cash == 10000, 'bot should not gain or lose cash when his and croupier hands are equal')
        bot.result_check(18)
        self.assertTrue(bot.cash == 9950, 'bot should lose 50 cash after losing')
        bot.result_check(1)
        self.assertTrue(bot.cash == 10000, 'bot should gain 50 cash after winning')
    
    #testuje funkcje która gra póki bedziesz dobierać, hit(26) testuje czy zwroci false gdy przebijesz 21
    def test_hit(self):
        bot = player()
        self.assertTrue(bot.hit(False, None, 0) == 1, "bot should not hit when the answer is 0")
        self.assertTrue(bot.hit(False, 2, 0) == 1, "bot should not hit when the answer is 0")
        self.assertTrue(bot.hit(True) == 2, "function should return code 2 if croupier is hitting")
        bot.hand = 21
        self.assertTrue(bot.hit(False, None, 1) == 0, "function should return code 0 if player score is above 21")
        bot.hand = 0
        self.assertTrue(bot.hit(False, None, 1) == 3, "function should return code 3 if player has no genes (index)")
        bot.genomes = np.array([[1,12,13,0]])
        for _ in range (0,52):
            bot.hand = 1
            code = bot.hit(False, 0, bot.genomes[0][3])
            if code == 5:
                check = True
                break
        self.assertTrue(code, "if there are are according genes, then bot should listen to them")
        bot.genomes = np.array([[1,12]])
        self.assertTrue(bot.hit(False, 0, 1) == 4, "if answer is not in genes, then it should return 4")


deck = shuffle_deck()
test = TestGroupByMethods()
test.test_shuffle_deck()
test.test_draw_card()
test.test_check_genes()
test.test_result_check()
test.test_hit()
