import numpy as np
import pandas as pd
from random import shuffle
import random
import os
import pickle
from time import sleep
import copy

class card:
    def __init__(self, value, picture = None):
        self.value = int(value)
        self.picture = picture

class player:
    def __init__(self, genomes = None, id = None):
        self.hand = 0
        self.aces_count = 0
        self.genomes = np.empty((210, 3)) if genomes is None else copy.deepcopy(genomes)
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

        answer = int(random.uniform(0, 2))
        self.genes[2] = answer

        if self.append_index < len(self.genomes):
            self.genomes[self.append_index] = self.genes
            self.append_index += 1

        self.genes = np.empty(3)

        while answer == 1:
            result = self.draw_card(deck)
            if result == False:
                return self.hand

            gene = self.check_genes(croupier.hand)
            if isinstance(gene, np.ndarray):
                return self.hit(deck, gene)

            answer = int(random.uniform(0, 2))
            self.genes[2] = answer

            if self.append_index < len(self.genomes):
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

    bot.hit(deck, gene)

    if bot.hand > 21:
        bot.cash -= 100
        bot.hand = 0
        croupier.hand = 0
        bot.genes = np.empty(3)
        return bot

    while croupier.hand < 17:
        croupier.draw_card(deck)
    '''
    if isinstance(gene, np.ndarray):
        if gene[0] == 0:
            print(f'gen ma wartosc : {gene} | reka bota {bot.hand}')
    '''

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

def crossover_mutate(best_num, bots_num, bots_list, kids):
    elites = [None] * best_num
    cash = np.empty(bots_num)
    cash_best = 0
    for i in range(bots_num):
        cash[i] = bots_list[i].cash

    for i in range(best_num):
        #add to elites element from bots_list with the index of maximum cash
        elites[i] = bots_list[np.where(cash == cash.max())[0][0]]
        cash_best += cash.max()
        cash = np.delete(cash, cash == cash.max())
    print("cash = ", cash_best/5)

    genepool = np.empty((bots_num*200, 3))
    elite_id = 0
    elite_cash = 0
    i = 0
    a = 0
    for elite in elites:
        elite.id = elite_id
        elite_cash += elite.cash
        elite.cash = 10000
        kids[i] = elite
        for gene in elite.genomes:
            genepool[a] = gene
            a+=1
        elite_id += 1
        i+=1

    #print(genepool)
    for i in range (best_num, bots_num):
        np.random.shuffle(genepool)
        bot = player(genepool[:200],i)
        kids[i] = bot

    return kids



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
kids = [None] * 50

croupier = player()

for I in range (50):
    new_player = player(id=I)
    bots_list.append(new_player)
    for i in range(200):
        train_test(deck, bot = bots_list[I])
        deck = shuffle_deck()
        if I == 1:
            print(bots_list[1].genomes[bots_list[1].append_index-1], bots_list[1].append_index-1)
        #sleep(0.1)

#print(bots_list[8].genomes)
#print(bots_list[0].genomes)



#crossover_mutate(5, 50, bots_list, kids)

#print(kids)
#print(kids[8].genomes)


#TODO
#skąd pojawiają się zera w miejscu ręki krupiera w genach
#czemu tylko 10-20 genów jest zapisywanych