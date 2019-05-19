# Basic program for BlackJack
import random

suits = ("Spades", "Hearts", "Clubs", "Diamonds")
ranks = ('Two', 'Three', 'Four', 'Five', 'Six', 'Seven', 'Eight', 'Nine', 'Ten', 'Jack', 'Queen', 'King', 'Ace')
values = {'Two': 2, 'Three': 3, 'Four': 4, 'Five': 5, 'Six': 6, 'Seven': 7, 'Eight': 8, 'Nine': 9, 'Ten': 10, 'Jack': 10,
          'Queen': 10, 'King': 10, 'Ace': 11}
playing = True


class Card:
    def __init__(self,suit,rank):
        self.rank = rank
        self.suit = suit

    def __str__(self):
        return self.rank + ' of ' + self.suit


class Deck:
    def __init__(self):
        self.deck = []
        for s in suits:
            for r in ranks:
                self.deck.append(Card(s, r))

    def shuffle(self):
        random.shuffle(self.deck)

    def __str__(self):
        return "Number of cards in deck are: {}".format(len(self.deck))

    def draw(self):
        single_card = self.deck.pop()
        return single_card


class Hand:
    def __init__(self):
        self.cards = []
        self.value = 0
        self.aces = 0

    def add_card(self, card):
        self.cards.append(card)
        self.value += values[card.rank]

        if card.rank == 'Ace':
            self.aces += 1

    def adjust_for_ace(self):
        while self.value > 21 and self.aces:
            self.value -= 10
            self.aces -= 1


class Chips:
    def __init__(self):
        self.total = 100
        self.bet = 0

    def win_bet(self):
        self.total += self.bet    

    def loss_bet(self):
        self.total -= self.bet    


def take_bet(chips):
    while True:
        try:
            chips.bet = int(input("How many chip would you like to bet?"))
        except TypeError:
            print("Please write an integer.")
        else:
            if chips.bet > chips.total:
                print("Sorry, you do not have enough chips: {}".format(chips.total))
            else:
                break            


def hit(decks, hand):
    hand.add_card(decks.draw())
    hand.adjust_for_ace()


def hit_or_stand(decks, hand):
    global playing
    while True:
        x = input("Hit or Stand. Enter h or s.")
        if x[0].lower() == 'h':
            hit(decks, hand)
        elif x[0].lower() == 's':
            print("Player stands. Dealer's turn.")
            playing = False
        else:
            print("Sorry, did not understand that. Please enter h or s only.")        
            continue
        break


def show_some(player, dealer):
    print("Dealer's Hand:")
    print("One card hidden")
    print(dealer.cards[1])
    print('\n')
    print("Player's Hand:")
    for card in player.cards:
        print(card)    


def show_all(player, dealer):
    print("Dealer's Hand:")
    for card in dealer.cards:
        print(card)
    print('\n')    
    print("Player's Hand:")
    for card in player.cards:
        print(card)


def player_busts(chips):
    print("Bust Player.")
    chips.loss_bet()


def player_wins(chips):
    print("Player Wins!")
    chips.win_bet()


def dealer_busts(chips):
    print("Bust Dealer.")
    chips.win_bet()


def dealer_wins(chips):
    print("Dealer Wins!")
    chips.loss_bet()


def push():
    print("Dealer and Player tied. PUSH!")    


while True:
    print("Welcome to Blackjack")
    deck = Deck()
    deck.shuffle()
    player_hand = Hand()
    player_hand.add_card(deck.draw())
    player_hand.add_card(deck.draw())
    dealer_hand = Hand()
    dealer_hand.add_card(deck.draw())
    dealer_hand.add_card(deck.draw())

    player_chips = Chips()
    take_bet(player_chips)
    show_some(player_hand, dealer_hand)

    while playing:
        hit_or_stand(deck, player_hand)
        show_some(player_hand, dealer_hand)

        if player_hand.value > 21:
            player_busts(player_chips)
            break

        if player_hand.value <= 21:
            while dealer_hand.value < 17:
                hit(deck, dealer_hand)
            show_all(player_hand, dealer_hand)

            if dealer_hand.value > 21:
                dealer_busts(player_chips)
            elif dealer_hand.value > player_hand.value:
                dealer_wins(player_chips)
            elif dealer_hand.value < player_hand.value:
                player_wins(player_chips)
            elif dealer_hand.value < 17:
                player_wins(player_chips)
            else:
                push()

    print('\n Player total chips are at: {}'.format(player_chips.total))
    new_game = input("Would you like to play again? Yes or No")
    if new_game[0].upper() == 'Y':
        playing = True
        continue
    else:
        print("Thank you for playing")
        break
