import numpy as np
import random

import helper_functions


class Inning:
    lg_avg_stats, lg_avg_stats_extra = helper_functions.gen_offensive_outcome_probabilities()
    
    def __init__(self, pitching_team, batting_team, use_starting_base_state=False):
        self.pitching_team = pitching_team
        self.batting_team = batting_team
        if use_starting_base_state:
            self.base_state = use_starting_base_state
        else:
            self.base_state = {1: 0, 2: 0, 3: 0}
        self.outs = 0
        

        self.hit_mapping = {i:0 for i in self.lg_avg_stats}
        self.hit_mapping["BB"] = 0
        # NEED TO ADD LOGIC FOR HOW RUNNERS ADVANCE ON A WALK
        self.hit_mapping["1B"] = 1
        self.hit_mapping["2B"] = 2
        self.hit_mapping["3B"] = 3
        self.hit_mapping["HR"] = 4

        self.out_mapping = {i:0 for i in self.lg_avg_stats}
        self.out_mapping["K"] = 1
        self.out_mapping["FO"] = 1
        self.out_mapping["GO"] = 1
                
    @staticmethod
    def clean_base_state(list_of_base_state):
        """ Return a more easily digestible version of the base state. Convert a map to string"""
        bases = {1:0,2:0,3:0}
        for i in list_of_base_state:
            if i in bases.keys():
                bases[i] = i
        return bases

    def _change_lg_avg_stats(self, dampening):
        """ Change default statistics by +/-dampening% """
        self.lg_avg_stats, self.lg_avg_stats_extra = gen_offensive_outcome_probabilities(dampening)


    def _show_base_out_situation(self):
        """ Helper function if user wants to see baseout state during simulation"""
        b = ''.join([str(i) for i in self.base_state.values()])
        print(b, ' '*5, {i:j for ij in self.__dict__.items() if i in ['outs']},
             ' and the score is ', 
              '{}:'.format(self.batting_team.name), self.batting_team.runs, '-', 
              '{}:'.format(self.pitching_team.name), self.pitching_team.runs)
    
    def _update_base_state(self, outcome):
        """ Change base state based on the outcome of an at bat """
        # TODO: This is an overly complex method of updating base states. This can be similified in future
        outcome_raw = outcome
        outcome = self.hit_mapping[outcome]
        
        end_state = [outcome]
        end_state_walk = []

        ### SAC FLY
        if outcome_raw == 'FO':
            if self.base_state[3] > 0:
                random_number = random.random() 
                if (random_number > self.lg_avg_stats_extra['_SF3']['out'] and 
                    random_number < self.lg_avg_stats_extra['_SF3']['safe']):
                    self._score_runs(self.batting_team)
                self.base_state[3] = 0

                        
        ### WALK / HBP
        if outcome_raw in ['BB', 'HBP']:
            if self.base_state[1] > 0:
                if self.base_state[2] > 0:
                    if self.base_state[3] > 0:
                        # '123'
                        self._score_runs(self.batting_team)
                        self.base_state = {1:1, 2:2, 3:3}
                    else:
                        # '12'
                        self.base_state = {1:1, 2:2, 3:3}
                else:
                    # '1_?'
                    self.base_state[1] = 1
                    self.base_state[2] = 2
            else:
                self.base_state[1] = 1

        ### HOME RUN
        if outcome == 4:
            self._score_runs(self.batting_team)        
        ### ANYTHING
        self.base_state.values()
        for b in self.base_state.values():
            val = 0
            potential_val = 0
            
            if outcome == 0:
                potention_val = b
                if b == 0:
                    val = 0
                else:
                    potential_val = b + outcome 
                    if potential_val > 3:
                        val = 0
                        self._score_runs(self.batting_team)
                    else:
                        val = potential_val

                
            else:
                if b == 0:
                    val = 0
                else:
                    potential_val = b + outcome 
                    if potential_val > 3:
                        val = 0
                        self._score_runs(self.batting_team)
                    else:
                        val = potential_val

            end_state.append(val)
            
        end_state = self.clean_base_state(end_state)
        self.base_state = end_state

    def _score_runs(self, team):
        """ Add a run to a teams score """
        team.runs += 1

    def _update_out_state(self, outcome):
        """ Update the number of outs in an inning """
        self.outs = self.outs + self.out_mapping[outcome]

    def gen_at_bat_outcome(self, show_outcome=False):
        # return the outcome of a plate apperance based on weighted probabilities of each event
        outcome = np.random.choice(list(self.lg_avg_stats.keys()), 1, replace=True, p=list(self.lg_avg_stats.values()))[0]
        if show_outcome:
            print('ab:', outcome)
        self._update_base_state(outcome)
        self._update_out_state(outcome)
        
        return outcome