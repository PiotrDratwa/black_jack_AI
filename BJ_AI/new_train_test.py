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

    def draw_card(self, deck):
        # Automatically reshuffle the deck if it's about to run out of cards
        if len(deck) < 1:
            deck.extend(shuffle_deck())

        card_drawn = deck.pop()  # Safely pop the top card
        if card_drawn.value == 11:  # Handling ace
            self.aces_count += 1
        self.hand += card_drawn.value

        if self.hand <= 21:
            return True
        elif self.aces_count == 0:
            self.cash -= 100
            return False

        # Adjusting for aces
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

        # Random decision for hit (1) or stand (0)
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

def shuffle_deck():
    cards = [card(value) for value in range(2, 12)] * 4  # Generate cards (values 2-11)
    random.shuffle(cards)
    return cards

# Main game logic
def train_test(deck, bot: player):
    for _ in range(2):  # Draw two initial cards
        bot.draw_card(deck)

    croupier = player()
    croupier.draw_card(deck)

    gene = bot.check_genes(croupier.hand)
    bot.hit(deck, croupier.hand, gene)

    if bot.hand > 21:
        bot.cash -= 100  # Bust penalty
    else:
        while croupier.hand < 17:
            croupier.draw_card(deck)

        bot.result_check(croupier.hand)

    # Reset hands after each round
    bot.hand = 0
    croupier.hand = 0

# Crossover and Mutation
def crossover_mutate(best_num, bots_num, bots_list, kids, mutation_rate=0.1):
    elites = sorted(bots_list, key=lambda b: b.cash, reverse=True)[:best_num]
    print("Average cash of best players:", np.mean([bot.cash for bot in elites]))

    genepool = np.concatenate([elite.genomes for elite in elites])
    np.random.shuffle(genepool)

    for i in range(bots_num):
        # Create kids by copying top genomes with some mutation
        kid_genomes = genepool[:200].copy()  # Take the first 200 genes

        # Apply mutation with a probability
        if random.uniform(0, 1) < mutation_rate:
            mutate_index = random.randint(0, len(kid_genomes) - 1)
            kid_genomes[mutate_index, 2] = 1 if kid_genomes[mutate_index, 2] == 0 else 0

        kids[i] = player(genomes=kid_genomes, id=i)

    return kids

# Game setup and simulation
bots_list = [player(id=i) for i in range(100)]

for epoch in range(40):  # Evolution loop
    kids = [None] * 100

    for I in range(100):
        deck = shuffle_deck()
        for _ in range(2000):  # Each bot plays 2000 rounds
            train_test(deck, bots_list[I])
            if len(deck) < 10:  # Reshuffle deck if low on cards
                deck.extend(shuffle_deck())  # Extend the current deck with a fresh shuffled deck

    # Perform crossover and mutation after each round of play
    crossover_mutate(5, 100, bots_list, kids, mutation_rate=0.05)

    # Replace old bots with new generation
    bots_list = kids