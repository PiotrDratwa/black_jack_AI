import numpy as np
import pandas as pd
from random import shuffle
import random
import os
import pickle
from time import sleep

class card:
    def __init__(self, value, picture = None):
        self.value = int(value)
        self.picture = picture

class player:
    def __init__(self, genomes = np.empty((400,3)), id = None):
        self.hand = 0
        self.aces_count = 0
        self.genomes = genomes
        self.append_index = 0
        self.genes = np.empty(3)
        self.cash = 10000
        self.id = id

    #returns true if didn't lose
    def draw_card(self, deck):
        if deck[-1] == ace:
            self.aces_count +=1
        self.hand += deck[-1].value
        if self.hand < 21:
            return True
        elif self.aces_count == 0:
            self.cash -= 100
            return False

        #if player loses and there's aces then it will turn them into 1 until he no longer loses
        while self.aces_count > 0:
            self.hand - 10
            self.aces_count -= 1
        if self.hand < 21:
            return True
        self.cash -= 100
        return False


    def check_genes(self, croupier_hand):
        if len(self.genomes) == 0:
            self.genes[0] = self.hand
            self.genes[1] = croupier_hand
            return False
        for gene in self.genomes:
            if self.hand != gene[0]:
                continue
            elif croupier_hand != gene[1]:
                continue
            else:
                return gene

        self.genes[0] = self.hand
        self.genes[1] = croupier_hand
        return False

    def hit(self, deck, gene = False):
        while isinstance(gene, np.ndarray):
            if gene[2] == 1:
                result = self.draw_card(deck)
                if result == True:
                    gene = self.check_genes(croupier.hand)
                else:
                    return self.hand
            elif gene[2] == 0:
                return self.hand
            else:
                print(f'error: answer is neither 0 or 1, it is{gene}')

        answer = int(random.uniform(0,2))
        self.genes[2] = answer
        self.genomes[self.append_index] = self.genes
        self.append_index += 1
        self.genes = np.empty(3)

        while answer == 1:
            result = self.draw_card(deck)
            if result == False:
                return self.hand

            gene = bot.check_genes(croupier.hand)
            if isinstance(gene, np.ndarray):
                return self.hit(deck, gene)

            answer = int(random.uniform(0,2))
            self.genes[2] = answer
            self.genomes[self.append_index] = self.genes
            self.append_index += 1
            self.genes = np.empty(3)

    def result_check(self, croupier_hand):
        if self.hand > croupier_hand:
            self.cash += 100
        if self.hand < croupier_hand:
            self.cash -= 100

def shuffle_deck():
    deck = np.empty(0)
    two_list = np.array([two,two,two,two])
    three_list = np.array([three,three,three,three])
    four_list = np.array([four,four,four,four])
    five_list = np.array([five,five,five,five])
    six_list = np.array([six,six,six,six])
    seven_list = np.array([seven,seven,seven,seven])
    eight_list = np.array([eight,eight,eight,eight])
    nine_list = np.array([nine,nine,nine,nine])
    ten_list = np.array([ten,ten,ten,ten])
    jack_list = np.array([jack,jack,jack,jack])
    queen_list = np.array([queen,queen,queen,queen])
    king_list = np.array([king,king,king,king])
    ace_list = np.array([ace,ace,ace,ace])

    deck = np.append(deck, two_list)
    deck = np.append(deck, three_list)
    deck = np.append(deck, four_list)
    deck = np.append(deck, five_list)
    deck = np.append(deck, six_list)
    deck = np.append(deck, seven_list)
    deck = np.append(deck, eight_list)
    deck = np.append(deck, nine_list)
    deck = np.append(deck, ten_list)
    deck = np.append(deck, jack_list)
    deck = np.append(deck, queen_list)
    deck = np.append(deck, king_list)
    deck = np.append(deck, ace_list)
    shuffle(deck)
    return deck


def train_test(deck, bot:player):
    for _ in range(0,2):
        bot.draw_card(deck)
    croupier = player()
    croupier.draw_card(deck)

    gene = bot.check_genes(croupier.hand)
    bot.hit(deck)

    if bot.hand > 21:
        bot.cash -= 100
        bot.hand = 0
        croupier.hand = 0
        bot.genes = np.empty(3)
        return bot

    while croupier.hand < 17:
        croupier.draw_card(deck)

    if croupier.hand > 21:
        bot.cash += 100
        bot.hand = 0
        croupier.hand = 0
        bot.genes = np.empty(3)
        return bot

    if bot.hand > croupier.hand:
        bot.cash += 100
    if bot.hand < croupier.hand:
        bot.cash -= 100

    bot.hand = 0
    croupier.hand = 0
    bot.genes = np.empty(3)
    return bot

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

bots_list = []
kids = []

bot = player(id=0)
croupier = player()

for I in range (0,50):
    for _ in range(0,200):
        train_test(deck, bot)
        deck = shuffle_deck()
    print(I)
    bots_list.append(bot)
    bot = player(id=(I+1))