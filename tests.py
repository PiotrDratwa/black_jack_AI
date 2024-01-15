from BJ_AI_rewrite import deck, draw_card, croupier_draw_card, shuffle_deck, check_genes, add_genes, hit
import unittest
import numpy as np
import pandas as pd

class TestGroupByMethods(unittest.TestCase):
    
    def test_draw_card(self):
        deck = shuffle_deck()
        hand = 0
        for _ in range(2):
            draw_card(hand)
        self.assertTrue(hand < 22, "hand should be below 22 and above 0")
        self.assertTrue(hand > 0, "hand should above 0")
        self.assertEqual(deck, 50, "There should be 50 cards after 2 draws")
        
    def test_croupier_draw_card(self):
        deck = shuffle_deck()
        hand = 0
        for _ in range(2):
            draw_card(hand)
        self.assertTrue(hand < 22, "hand should be below 22 and above 0")
        self.assertTrue(hand > 0, "hand should above 0")
        self.assertEqual(deck, 50, "There should be 50 cards after 2 draws")
    
    def test_check_genes(self):
        a = np.array(['z','x','c'])
        b = np.array(['g','h','l'])
        true_gen = pd.DataFrame({'col1':[a]})
        false_gen = pd.DataFrame({'col1':[b]})
        copy = pd.DataFrame({'col1':[a.copy()]})
        self.assertTrue(check_genes(true_gen, copy), "equal genes should return true")
        self.assertTrue(check_genes(false_gen, copy), "equal genes should return true")
    
    def test_add_genes(self):
        my_hand = 2
        croupier_hand = 18
        bet = 50
        self.assertTrue(len(add_genes(my_hand,croupier_hand, bet)) == 3)
        self.assertTrue(my_hand > 2)
    #testuje funkcje która gra póki bedziesz dobierać, hit(26) testuje czy zwroci false gdy przebijesz 21
    def test_hit(self):
        self.assertFalse(hit(26))