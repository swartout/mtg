"""Utilities for the MTG engine"""

import random
import copy

class Player:
    """A player in the game"""
    def __init__(self, name, deck):
        """Initialize a new player
        
        Args:
            name: The name of the player
            deck: The deck to use (list of cards)
        """
        self.name = name
        deck = copy.deepcopy(deck)
        random.shuffle(deck)
        self.deck = deck
        self.hand = [deck.pop() for _ in range(7)]
        self.life = 20
        self.untapped_lands = 0
        self.tapped_lands = 0
        self.battlefield = []

class Card:
    """A card in the game"""
    def __init__(self, name, type, cmc=0, power=0, toughness=0):
        """Initialize a new card
        
        Args:
            name: The name of the card
            type: The type of the card
            cmc: The converted mana cost of the card
            power: The power of the card
            toughness: The toughness of the card
        """
        self.name = name
        self.type = type
        self.cmc = cmc
        self.power = power
        self.toughness = toughness
