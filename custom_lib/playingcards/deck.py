import random
from . import card
from . import cardcollection

"""
playingcards.py (Custom Modified Version)
-----------------------------------------
Original Author: Blake Potvin
Original Repo: https://github.com/blakepotvin/playingcards.py
License: MIT License (see LICENSE file)

Modifications by: (your name)
Date of Modification: 

Summary of Modifications:
Change to Deck class to allow for two standard decks to be used by dealer.

The modifications are provided under the same MIT License as the original library.
"""

class Deck(cardcollection.CardCollection):

    def __init__(self, deck: list = None) -> None:
        """
        Customised version of Deck class, allows for max of 104 cards per Deck object.
        2-Deck variations of Blackjack have more equitable outcomes for player and dealer.
        Modified in accordance with MIT license.
        """
        if deck is not None and self.__validate_initial_deck(deck):
            self.cards = deck
        else:
            self.cards = self.__generate_deck()
        self.drawn = 0
        self.remaining = 104
        super().__init__(cards=self.cards, maximum=104, ordered=True)

    def __generate_deck(self) -> list:
        """
        Customised version of __generate_deck to create deck of 104 cards.
        Modified in accordance with MIT license.
        """
        deck = []
        for suit in range(4):
            deck.extend(card.Card(value=value, suit=suit, deck=self)
                        for value in range(1, 14))
            deck.extend(card.Card(value=value, suit=suit, deck=self)
                        for value in range(1, 14))
        return deck

    def __validate_initial_deck(self, deck) -> bool:
        return all(isinstance(card, card.Card) for card in deck)

    def draw_card(self) -> card.Card:
        if len(self.cards):
            drawn_card = self.cards.pop()
        else:
            raise MaxCardsDrawn
        self.drawn += 1
        self.remaining -= 1
        return drawn_card

    def draw_n(self, n) -> cardcollection.CardCollection:
        if len(self.cards) <= n-1:
            raise MaxCardsDrawn(
                f"Asked to draw {n} cards but there is only {len(self.cards)} left in deck")
        drawn_cards = self.cards[:n]
        self.cards = self.cards[n:]
        self.drawn += n
        self.remaining -= n
        return cardcollection.CardCollection(drawn_cards)

    def __len__(self) -> int:
        return len(self.cards)

    def __str__(self) -> str:
        return ", ".join(str(card) for card in self.cards)

    def __repr__(self) -> str:
        return self.__str__()


class MaxCardsDrawn(Exception):
    pass
