import numpy as np
import random
import copy

class card:
    def __init__(self, value, picture=None):
        self.value = int(value)
        self.picture = picture

class player:
    def __init__(self, genomes=None, id=None):
        self.hand = 0
        self.aces_count = 0
        self.genomes = np.empty((170, 3)) if genomes is None else copy.deepcopy(genomes)
        self.append_index = 0
        self.genes = np.empty(3)
        self.cash = 10000
        self.id = id
        self.lost_games = 0  # Track the number of lost games

    def draw_card(self, deck):
        if len(deck) < 1:
            deck.extend(shuffle_deck())

        card_drawn = deck.pop()
        if card_drawn.value == 11:
            self.aces_count += 1
        self.hand += card_drawn.value

        if self.hand <= 21:
            return True
        elif self.aces_count == 0:
            self.cash -= 100
            return False

        while self.aces_count > 0 and self.hand > 21:
            self.hand -= 10
            self.aces_count -= 1

        if self.hand <= 21:
            return True
        self.cash -= 100
        return False

    def check_genes(self, croupier_hand):
        for gene in self.genomes:
            if self.hand == gene[0] and croupier_hand == gene[1]:
                return gene
        self.genes[0] = self.hand
        self.genes[1] = croupier_hand
        return False

    def hit(self, deck, croupier_hand, gene=False):
        while isinstance(gene, np.ndarray):
            if gene[2] == 1:
                if not self.draw_card(deck):
                    return self.hand
                gene = self.check_genes(croupier_hand)
            elif gene[2] == 0:
                return self.hand
            else:
                print(f'Error: gene value is neither 0 nor 1, it is {gene[2]}')

        answer = int(random.uniform(0, 2))
        self.genes[2] = answer

        if self.append_index < len(self.genomes):
            self.genomes[self.append_index] = self.genes
            self.append_index += 1

        self.genes = np.empty(3)

        while answer == 1:
            if not self.draw_card(deck):
                return self.hand

            gene = self.check_genes(croupier_hand)
            if isinstance(gene, np.ndarray):
                return self.hit(deck, croupier_hand, gene)

            answer = int(random.uniform(0, 2))
            self.genes[2] = answer

            if self.append_index < len(self.genomes):
                self.genomes[self.append_index] = self.genes
                self.append_index += 1

            self.genes = np.empty(3)

    def result_check(self, croupier_hand):
        if self.hand > croupier_hand:
            self.cash += 100
        else:
            self.cash -= 100
            self.lost_games += 1  # Increment lost games when the player loses

def shuffle_deck():
    cards = [card(value) for value in range(2, 12)] * 4
    random.shuffle(cards)
    return cards

def train_test(deck, bot: player):
    for _ in range(2):
        bot.draw_card(deck)

    croupier = player()
    croupier.draw_card(deck)

    gene = bot.check_genes(croupier.hand)
    bot.hit(deck, croupier.hand, gene)

    if bot.hand > 21:
        bot.cash -= 100
        bot.lost_games += 1  # Count bust as a lost game
    else:
        while croupier.hand < 17:
            croupier.draw_card(deck)

        bot.result_check(croupier.hand)

    bot.hand = 0
    croupier.hand = 0

def crossover_mutate(best_num, bots_num, bots_list, kids, mutation_rate=0.1):
    # Sort players by cash to determine best and worst
    sorted_bots = sorted(bots_list, key=lambda b: b.cash, reverse=True)

    # Best 5 players
    best_players = sorted_bots[:best_num]
    avg_cash_best = np.mean([bot.cash for bot in best_players])
    avg_lost_games_best = np.mean([bot.lost_games for bot in best_players])

    # Worst 5 players
    worst_players = sorted_bots[-best_num:]
    avg_cash_worst = np.mean([bot.cash for bot in worst_players])
    avg_lost_games_worst = np.mean([bot.lost_games for bot in worst_players])

    # Print comparison
    print(f"Best 5 players -> Average cash: {avg_cash_best}, Average lost games: {avg_lost_games_best}")
    #print(f"Worst 5 players -> Average cash: {avg_cash_worst}, Average lost games: {avg_lost_games_worst}")

    # Generate new kids
    for i in range(best_num):
        # Directly copy best players into next generation
        kids[i] = copy.deepcopy(best_players[i])

    for i in range(best_num, bots_num):
        # Select two random best players for crossover
        parent1 = random.choice(best_players)
        parent2 = random.choice(best_players)

        # Crossover: Mix genes from parent1 and parent2
        split_point = np.random.randint(1, len(parent1.genomes) - 1)
        kid_genomes = np.vstack((parent1.genomes[:split_point], parent2.genomes[split_point:]))

        # Mutate the kid's genome
        for gene in kid_genomes:
            if random.random() < mutation_rate:
                gene[2] = random.randint(0, 1)  # Mutate decision to hit or stand

        # Create new bot with mutated genomes
        kids[i] = player(genomes=kid_genomes, id=i)

    return kids

bots_range = 100
bots_list = [player(id=i) for i in range(bots_range)]

for epoch in range(100):
    kids = [None] * bots_range

    for I in range(bots_range):
        deck = shuffle_deck()
        for _ in range(1000):
            train_test(deck, bots_list[I])
            if len(deck) < 10:
                deck.extend(shuffle_deck())

    crossover_mutate(5, bots_range, bots_list, kids, mutation_rate=0.20)

    bots_list = kids

    # Reset lost games for the new epoch
    for bot in bots_list:
        bot.lost_games = 0
