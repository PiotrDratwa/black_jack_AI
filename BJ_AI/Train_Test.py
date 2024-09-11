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
    def __init__(self, genomes = [], id = None):
        self.hand = 0
        self.aces_count = 0
        self.genomes = genomes
        self.genes = []
        self.cash = 10000
        self.id = id

    #returns true if didn't lose
    def draw_card(self):
        global deck
        if deck[-1] == ace:
            self.aces_count +=1
        self.hand += deck[-1].value
        deck = np.delete(deck, -1)
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
        if (len(self.genomes)) == 0:
            self.genes.append(self.hand)
            self.genes.append(croupier_hand)
            return False

        for gene in self.genomes:
            if self.hand != gene[0]:
                continue
            elif croupier_hand != gene[1]:
                continue
            else:
                return gene
        self.genes.append(self.hand)
        self.genes.append(croupier_hand)
        return False

    def hit(self, gene = False, answer = int(random.uniform(0,2)), answer_num = 2, is_croupier = False):
        global deck
        if is_croupier == True:
            self.draw_card()
            return 0
        check = self.draw_card()

        if check is False:
            self.genes.append(answer)
            return 2

        if gene is False:
            answer = int(random.uniform(0,2))
            self.genes.append(answer)
            self.genes.append(self.hand)
            return answer

        if answer_num > len(gene):
            #self.genes = self.genomes[index]
            #self.genes[-1] = self.hand
            answer = int(random.uniform(0,2))
            #self.append(answer)
            #self.append(self.genes)
            return answer

        #trzeba jakoś ogarnąć żeby ten answer num przesuwał się bez rekurencji
        if self.hand == gene[answer_num + 1]:
            return gene[answer_num + 2]
        return int(random.uniform(0,2))


    def old_hit(self, gene = None, answer = int(random.uniform(0,2)), answer_num = 2, is_croupier = False):
        global deck
        print('outer')
        if is_croupier == True:
            self.draw_card()
            return 2
        #(answer = 0 = false) It's int not boolean for easier accessing of genes later
        if answer == 0 and gene is None:
            self.genes.append(answer)
            return 1
        elif answer == 0:
            return 1
        check = self.draw_card()
        #if hand exceeded 21
        if check is False:
            self.genes.append(answer)
            self.cash -= 100
            return 0
        print("gene =", gene)
        print("here0")
        if gene is None:
            answer = int(random.uniform(0,2))
            self.genes.append(answer)
            self.genes.append(self.hand)
            self.hit(False, None, answer)
            return 3
        print("here1")
        #if answer is not existent within accessed genome, then create new genome with current genes and keep playing
        if answer_num > len(gene):
            #self.genes = self.genomes[index]
            #self.genes[-1] = self.hand
            answer = int(random.uniform(0,2))
            #self.append(answer)
            #self.append(self.genes)
            self.hit(False, answer, None, answer_num)
            return 4
        #do what the genes tell you to do while the genes match
        if self.hand == gene[answer_num - 2]:
            self.hit(False, gene, gene[answer_num], answer_num+2)
            return 5
        print("here2")

    def result_check(self, croupier_hand):
        if self.hand > croupier_hand:
            self.cash += 100
        if self.hand < croupier_hand:
            self.cash -= 100

    def add_genes(self):
        if len(self.genes) > 1:
            self.genomes.append(self.genes)


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

def hit_loop_random(bot):
    answer = int(random.uniform(0,2))
    while answer == 1:
        answer = bot.hit()

def hit_loop_deter(bot, gene):
    answer_num = 2
    #print(gene)
    answer == gene[answer_num]
    while answer == 1:
        try:
            answer = bot.hit(gene, gene[answer_num], answer_num)
        except IndexError:
            answer = bot.hit()

def train_test(bot:player):
    for _ in range(0,2):
        bot.draw_card()
    croupier.draw_card()

    gene = bot.check_genes(croupier.hand)
    if gene == False:
        hit_loop_random(bot)
    else:
        hit_loop_deter(bot, gene)
    if bot.hand > 21:
        bot.add_genes()
        bot.cash -= 100
        bot.hand = 0
        croupier.hand = 0
        bot.genes = []
        return bot
    while croupier.hand < 17:
        hit_loop(croupier, False, 1)
    if croupier.hand > 21:
        bot.add_genes()
        bot.cash += 100
        bot.hand = 0
        croupier.hand = 0
        bot.genes = []
        return bot

    bot.result_check(croupier.hand)
    bot.add_genes()
    bot.hand = 0
    croupier.hand = 0
    bot.genes = []
    return bot


def crossover_mutate(best_num, bots_list, kids):
    elites = np.empty(0)
    cash = np.empty(0)
    for i in range(0,99):
        cash = np.append(cash, bots_list[i].cash)
    cash_best = 0
    for _ in range(0,best_num):
        #add to elites element from bots_list with the index of maximum cash
        elites = np.append(elites ,bots_list[np.where(cash == cash.max())[0][0]])
        cash_best += cash.max()
        cash = np.delete(cash, cash == cash.max())
    print("cash = ", cash_best/5)
    genepool = []
    elite_id = 0
    elite_cash = 0
    for elite in elites:
        elite.id = elite_id
        elite_cash += elite.cash
        elite.cash = 10000
        kids = np.append(kids, elite)
        genepool.append(elite.genomes)
        elite_id += 1

    for i in range (5,100):
        shuffle(genepool)
        bot = player(genepool[:601],i)
        kids = np.append(kids, bot)
    return kids

#variables
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

bots_list = np.empty(0)
kids = np.empty(0)

bot = player([], 0)
croupier = player()
deck = shuffle_deck()
for I in range (0,100):
    for _ in range(0,600):
        train_test(bot)
        deck = shuffle_deck()
    bot = player([], I+1)
    bots_list = np.append(bots_list, bot)

kids = crossover_mutate(5, bots_list, kids)
bots_list = np.empty(0)

for _ in range (0,30):
    for I in range (0,100):
        bot = kids[I]
        for i in range(0,600):
            train_test(bot)
            deck = shuffle_deck()
        bots_list = np.append(bots_list, bot)
    kids = np.empty(0)
    kids = crossover_mutate(5, bots_list, kids)
    bots_list = np.empty(0)