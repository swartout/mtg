"""MTG Game Engine"""

# note: assumes creatures have .power, .toughness, .cmc, .type

class Engine:
    """The game engine"""
    def __init__(self, player1, player2):
        """Initialize a new game engine
        
        Args:
            player1: The first player (goes first)
            player2: The second player
        """
        self.player1 = player1
        self.player2 = player2
        self.phases = ['main1', 'combat', 'main2']
        self.combat_steps = ['declare_attackers', 'declare_blockers']
        self.current_phase = 0
        self.current_step = 0
        self.current_player = player1
        self.other_player = player2
        self.played_land = False
        self.attackers = []
        self.blockers = {}
        self.blocking = []

    def get_actions(self):
        """Get the actions available to the player"""
        if self.current_phase == 0 or self.current_phase == 2:
            return self.get_actions_main()
        elif self.current_phase == 1:
            return self.get_actions_combat()
        else:
            raise ValueError('Invalid phase for actions')

    def get_actions_main(self):
        """Get the actions available to the player in the main phase

        Returns:
            A list of actions
        """
        actions = ['pass']
        for i in range(len(self.current_player.hand)):
            card = self.current_player.hand[i]
            if card.type == 'land' and not self.played_land:
                actions.append('play ' + str(i))
            elif card.type == 'creature':
                if self.current_player.untapped_lands >= card.cmc:
                    actions.append('play ' + str(i))
        return actions

    def get_actions_combat(self):
        """Get the actions available to the player in the combat phase
        
        Returns:
            A list of actions
        """
        actions = ['pass']
        if self.current_step == 0:
            for i in range(len(self.current_player.battlefield)):
                card = self.current_player.battlefield[i]
                if card.type == 'creature' and card not in self.attackers:
                    actions.append(str(i))
        elif self.current_step == 1:
            pass # TODO: write blocking function
        else:
            raise ValueError('Invalid combat step')
        return actions

    def take_action(self, action):
        """Take an action
        
        Args:
            action: The action to take
        """
        if self.current_phase == 0 or self.current_phase == 2:
            self.take_action_main(action)
        elif self.current_phase == 1:
            self.take_action_combat(action)
        else:
            raise ValueError('Invalid phase for action')
                
    def take_action_main(self, action):
        """Take an action in the main phase

        Args:
            action: The action to take
        """        
        if action == 'pass':
            self.next_phase()
        elif action[:4] == 'play':
            card = self.current_player.hand[int(action[4:])]
            if card.type == 'land':
                if self.played_land: # shouldn't happen
                    raise ValueError('Already played a land this turn')
                self.played_land = True
                self.current_player.hand.remove(card)
                self.current_player.battlefield.append(card)
                self.current_player.untapped_lands += 1
            elif card.type == 'creature':
                if self.current_player.untapped_lands < card.cmc:
                    raise ValueError('Not enough mana')
                self.current_player.hand.remove(card)
                self.current_player.battlefield.append(card)
                self.current_player.untapped_lands -= card.cmc
                self.current_player.tapped_lands += card.cmc
        else:
            raise ValueError('Invalid action')

    def take_action_combat(self, action):
        """Take an action in the combat phase
        
        Args:
            action: The action to take
        """
        if action == 'pass':
            self.next_phase()
            return
        if self.current_step == 0: # declare attackers
            card = self.current_player.battlefield[int(action)]
            if card.type != 'creature': # shouldn't happen
                raise ValueError('Not a creature')
            if card in self.attackers: # shouldn't happen
                raise ValueError('Already declared as an attacker')
            self.attackers.append(card)
            self.blockers[card] = []
        elif self.current_step == 1: # declare blockers
            attacker = self.attackers[int(action.split()[0])]
            self.blockers[attacker].append(self.other_player.battlefield[int(action.split()[1])])
        else: # something went wrong
            raise ValueError('Invalid combat step')

    def get_state(self):
        """Get the state of the game
        
        Returns:
            A dictionary containing the state of the game
        """
        state = {}
        state['current_phase'] = self.phases[self.current_phase]
        state['current_player'] = self.current_player.name
        state['other_player'] = self.other_player.name
        state['current_step'] = self.combat_steps[self.current_step]
        state['played_land'] = self.played_land
        state['attackers'] = [card.name for card in self.attackers]
        state['blockers'] = {}
        for attacker in self.blockers:
            state['blockers'][attacker.name] = [card.name for card in self.blockers[attacker]]
        state['current_battlefield'] = [card.name for card in self.current_player.battlefield]
        state['other_battlefield'] = [card.name for card in self.other_player.battlefield]
        state['current_hand'] = [card.name for card in self.current_player.hand]
        state['other_hand'] = [card.name for card in self.other_player.hand]
        state['current_life'] = self.current_player.life
        state['other_life'] = self.other_player.life
        state['current_untapped_lands'] = self.current_player.untapped_lands
        state['other_untapped_lands'] = self.other_player.untapped_lands
        state['current_tapped_lands'] = self.current_player.tapped_lands
        state['other_tapped_lands'] = self.other_player.tapped_lands
        return state

    def next_phase(self):
        """Move to the next phase"""
        if self.current_phase == 0: # main1
            # move to combat
            self.current_phase = 1
            self.current_step = 0
        elif self.current_phase == 1: # combat
            if self.current_step == 0: # declare attackers
                self.current_step = 1
            elif self.current_step == 1: # declare blockers
                # deal damage and resolve combat
                self.current_step = 0
                self.current_phase = 2
                for attacker in self.attackers:
                    blockers = self.blockers.get(attacker, [])
                    if len(blockers) == 0: # unblocked
                        self.other_player.life -= attacker.power
                    else: # blocked
                        blocker_damage = 0
                        attacker_damage = attacker.power
                        for blocker in blockers:
                            blocker_damage += blocker.power
                            if attacker_damage >= blocker.toughness:
                                self.other_player.battlefield.remove(blocker)
                                attacker_damage -= blocker.toughness
                        if blocker_damage >= attacker.toughness:
                            self.current_player.battlefield.remove(attacker)
            else: # something went wrong
                raise ValueError('Invalid combat step')
        elif self.current_phase == 2: # main2
            # move to next turn
            self.other_player = self.current_player
            self.current_player = self.player1 if self.current_player == self.player2 else self.player2
            self.current_phase = 0
            self.played_land = False
            self.current_player.untapped_lands += self.current_player.tapped_lands
            self.current_player.tapped_lands = 0
            self.current_player.hand.append(self.current_player.deck.pop())
        else: # something went wrong
            raise ValueError('Invalid phase')