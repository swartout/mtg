import copy
import pprint # remove this later
import random

from utils import Player, Card
from engine import Engine

# set seed
random.seed(7)

# pretty printer
pp = pprint.PrettyPrinter(indent=4)

# example runner, using for debugging
cards = [
    {'name': 'Forest', 'type': 'land', 'cmc': 0},
    {'name': 'Forest', 'type': 'land', 'cmc': 0},
    {'name': 'Forest', 'type': 'land', 'cmc': 0},
    {'name': 'Forest', 'type': 'land', 'cmc': 0},
    {'name': 'Forest', 'type': 'land', 'cmc': 0},
    {'name': 'Forest', 'type': 'land', 'cmc': 0},
    {'name': 'Elf', 'type': 'creature', 'cmc': 1, 'power': 1, 'toughness': 1},
    {'name': 'Elf', 'type': 'creature', 'cmc': 1, 'power': 1, 'toughness': 1},
    {'name': 'Grizzly Bears', 'type': 'creature', 'cmc': 2, 'power': 2, 'toughness': 2},
    {'name': 'Grizzly Bears', 'type': 'creature', 'cmc': 2, 'power': 2, 'toughness': 2},
    {'name': 'Grizzly Bears', 'type': 'creature', 'cmc': 2, 'power': 2, 'toughness': 2},
    {'name': 'Lion', 'type': 'creature', 'cmc': 3, 'power': 4, 'toughness': 2},
    {'name': 'Lion', 'type': 'creature', 'cmc': 3, 'power': 4, 'toughness': 2},
    {'name': 'Giant Spider', 'type': 'creature', 'cmc': 4, 'power': 2, 'toughness': 4},
    {'name': 'Giant Spider', 'type': 'creature', 'cmc': 4, 'power': 2, 'toughness': 4}
]

# convert to Card objects
cards = [Card(**card) for card in cards]

# four of each cards in the deck
deck = [copy.deepcopy(card) for card in cards for _ in range(4)]

# create the players
player1 = Player('p1', deck)
player2 = Player('p2', deck)

# create the engine
engine = Engine(player1, player2)

print('-' * 80)
print('starting state:')
pp.pprint(engine.get_state())

print('-' * 80)

print('actions:')
actions = engine.get_actions()
pp.pprint(actions)
print('-' * 80)
# playing land
print('taking action:')
engine.take_action(actions[-1])
print(actions[-1])
print('-' * 80)

print('new state:')
pp.pprint(engine.get_state())
print('-' * 80)

print('actions:')
actions = engine.get_actions()
pp.pprint(actions)
print('-' * 80)

# playing elf
print('taking action:')
engine.take_action(actions[-1])
print(actions[-1])
print('-' * 80)

print('new state:')
pp.pprint(engine.get_state())
print('-' * 80)

print('actions:')
actions = engine.get_actions()
pp.pprint(actions)
print('-' * 80)

# moving to combat
print('taking action:')
engine.take_action(actions[-1])
print(actions[-1])
print('-' * 80)

print('new state:')
pp.pprint(engine.get_state())
print('-' * 80)

print('actions:')
actions = engine.get_actions()
pp.pprint(actions)
print('-' * 80)

# attacking with elf
print('taking action:')
engine.take_action(actions[-1])
print(actions[-1])
print('-' * 80)

print('new state:')
pp.pprint(engine.get_state())
print('-' * 80)

print('actions:')
actions = engine.get_actions()
pp.pprint(actions)
print('-' * 80)

# declare no blockers
print('taking action:')
engine.take_action(actions[-1])
print(actions[-1])
print('-' * 80)

print('new state:')
pp.pprint(engine.get_state())
print('-' * 80)

print('actions:')
actions = engine.get_actions()
pp.pprint(actions)
print('-' * 80)

# move to main2
print('taking action:')
engine.take_action(actions[-1])
print(actions[-1])
print('-' * 80)

print('new state:')
pp.pprint(engine.get_state())
print('-' * 80)

print('actions:')
actions = engine.get_actions()
pp.pprint(actions)
print('-' * 80)

# pass turn
print('taking action:')
engine.take_action(actions[-1])
print(actions[-1])
print('-' * 80)

print('new state:')
pp.pprint(engine.get_state())
print('-' * 80)

print('actions:')
actions = engine.get_actions()
pp.pprint(actions)
print('-' * 80)