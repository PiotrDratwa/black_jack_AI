from random import shuffle
import random
import os
import pickle

#clasa karta zawiera wartość, to jest w tym momencie totalnie bez sensu, że karty to obiekty ale było mi to potrzebne do czegoś co miałem zrobic ale zrezygnowałem, finalnie nie chciało mi się tego zmieniać
class card():
    def __init__(self, value):
        self.value = int(value)

deck = []
genes = []
genoms = []
bots = []
kids_genes = []

#wczytanie potomstwa z pliku jeśli nie jest pusty
ScriptDir = os.path.dirname(__file__)
with open(f'{ScriptDir}/data.dat', 'rb') as fh:
    try:
        kids = pickle.load(fh)
    except EOFError:
        kids = []
with open(f'{ScriptDir}/data.dat', 'wb') as fh:
    fh.truncate(0)
bots = kids
#deklaracja wszystkich typów kart
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

aces = 0
count_aces = 0
croupier_count_aces = 0
croupier_aces = 0
cash_average = 0
T = 0
#funkcja dobierająca kartę dla gracza
def draw_card(hand):
    global aces
    global count_aces
    temp = deck[-1]
    #warunek, który sprawdza czy dobrana karta jest asem i dodaje 1 do licznika asów w ręce
    if temp == ace:
        count_aces += 1
        if count_aces > 1: temp.value = 1
        aces += temp.value
    hand += temp.value 
    #algorytm sprawdzający czy as ma mieć wartość 1
    if count_aces > 0:
        while (hand) > 21:
            hand -= aces
            aces = 1 * count_aces
            hand += aces 
            return hand
    deck.pop()
    return hand

#ten sam algorytm ale dla krupiera, są dwie funkcje bo muszą być osobno liczniki asów w ręce
def croupier_draw_card(hand):
    global croupier_aces
    global croupier_count_aces
    temp = deck[-1]
    if temp == ace:
        croupier_count_aces += 1
        if croupier_count_aces > 1: temp.value = 1
        croupier_aces += temp.value
    hand += temp.value 
    if croupier_count_aces > 0:
        while (hand) > 21:
            hand -= croupier_aces
            croupier_aces = 1 * croupier_count_aces
            hand += croupier_aces 
            return hand
    deck.pop()
    return hand

#algorytm dodający wszystkie karty do talii i tasujący ją
def shuffle_deck(deck):
        deck.clear
        for _ in range(4):
            deck.append(two)
            deck.append(three)
            deck.append(four)
            deck.append(five)
            deck.append(six)
            deck.append(seven)
            deck.append(eight)
            deck.append(nine)
            deck.append(ten)
            deck.append(jack)
            deck.append(queen)
            deck.append(king)
            deck.append(ace)
        shuffle(deck)

#główna pętla gry która jest za długa i powinna zostać rozbita na kilka funkcji
def main_loop():
    global cash
    global aces
    global count_aces
    global croupier_aces
    global croupier_count_aces
    global T
    my_hand = 0
    croupier_hand = 0
    global check
    check = False
    i = 0
    #dobieranie kar gracza i krupiera
    while i <= 1:
        my_hand = draw_card(my_hand)
        i+=1
    print(f'bot dobral dwie karty o wartosci razem: {my_hand}' )
    if count_aces>0: print("w tym jednego asa ")
    croupier_hand = draw_card(croupier_hand)
    print(f'krupier dobral karte o wartosci {croupier_hand}')
    if croupier_count_aces>0: print("jest to as")
    #warunek sprawdzający czy T ma jakiekolwiek geny i czy taki układ kart jest w jego genach, jeśli nie to odpowiedzi są losowane
    if 0 <= T < len(bots):
        i = 0
        n = 0
        while i < len(bots[T]) and len(bots[T][i]) > 2:
            if my_hand == bots[T][i][0] and croupier_hand == bots[T][i][1]:
                bet = 50
                print(f'bot stawil zakład o wartosci {bet}')
                n = 3
                check = True
                croupier_hand = draw_card(croupier_hand)
                break
            i += 1
        if check == False:
            bet = 50
            print(f'bot stawil zakład o wartosci {bet}')
    elif check == False:
        bet = 50
        print(f'bot stawil zakład o wartosci {bet}')
    cash -= int(bet)
    #warunek czy ta sytuacja ma odpowiadający gen odpowiedzi(czy dobierasz czy nie)
    if check == True:
        answer = bots[T][i][n]
        if answer == 0:
            print('bot pasuje')
        elif answer == 1:
            print("bot dobiera")
        n+=1
    else:
        answer = int(random.uniform(0,2))
        if answer == 0:
            print('bot pasuje')
        elif answer == 1:
            print("bot dobiera")
    #pętla która działa póki dobierasz karty, lub przebijesz
    while answer == 1:
        my_hand = draw_card(my_hand)
        print(f"bot dobral karte, jego reka ma teraz wartosc {my_hand}")
        if my_hand > 21:
            print('bot przebil')
            bet = 0
            break
        if check == True and n < len(bots[T][i]):
            if my_hand == bots[T][i][n]:
                n+=1
                answer = bots[T][i][n]
                if answer == 0:
                    print('bot pasuje')
                elif answer == 1:
                    print("bot dobiera")
                n+=1
            else:
                check = False
        else:
            answer = int(random.uniform(0,2))
            if answer == 0:
                print('bot pasuje')
            elif answer == 1:
                print("bot dobiera")
    #warunek sprawdzający czy przebiłeś
    if bet == 0:
        if check == False:
            aces = 0
            count_aces = 0
            croupier_count_aces = 0
            croupier_aces = 0
        return True
    
    #pętla, krupier dobiera jezeli wartosc kart w rece jest mniejsza od 17
    while croupier_hand < 17:
        croupier_hand = croupier_draw_card(croupier_hand)
        print(f'krupier dobral karte, jego reka ma teraz wartosc {croupier_hand}')
        #warunek sprawdza czy krupier przebił
        if croupier_hand > 21:
            print('krupier przebil')
            bet = bet*2
            cash+= bet
            bet = 0
    if bet == 0:
        if check != True:
            aces = 0
            count_aces = 0
            croupier_count_aces = 0
            croupier_aces = 0
        return True

    #warunki sprawdzające kto wygrał, czy jest remis
    if croupier_hand == my_hand:
        print('remis, bot dostaje z powrotem swoj zaklad')
        cash += bet 
    elif croupier_hand < my_hand:
        print('bot wygral, dostaje z porotem dwukrotnosc zakladu')
        bet = bet*2
        cash+= bet
    bet = 0
    if check != True:
        aces = 0
        count_aces = 0
        croupier_count_aces = 0
        croupier_aces = 0
        genes.append(genoms)

b = 0
bots_cash = []
#pętle dla botów i genów 

cash = 1000
while b < 4:
    if len(deck) > 18:
        main_loop()
        b += 1
    else:
        shuffle_deck(deck)
    genoms = []
    print('\n')

os.system("pause")