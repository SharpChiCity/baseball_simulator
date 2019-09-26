import innings

class Game:
    def __init__(self, home_team, away_team, inning = 1, late_inning_base_change=None):
        self.home_team = home_team
        self.away_team = away_team
        self.bottom_of_inning = True  # starting at True because program flips at the top of the inning
        self.inning = inning - 1
        self.winning_team = None
        self.late_inning_default = {1:0, 2:2, 3:0}
        self.late_inning_base_change = late_inning_base_change
    
    def _check_end_game(self):
        if self.inning > 8:
            if self.bottom_of_inning:
                if self.away_team.runs > self.home_team.runs:
                    self.winning_team = self.away_team.name
                    # print('game over! {} won!'.format(self.winning_team))
                    return False
                else:
                    return True
            else:
                if self.home_team.runs > self.away_team.runs:
                    self.winning_team = self.home_team.name
                    # print('Game Over! {} won!'.format(self.winning_team))
                    return False
                else:
                    return True
        else:
            return True
        
    def _show_score(self):
        print('{}: {} - {}: {}'.format(
            self.away_team.name, self.away_team.runs, 
            self.home_team.name, self.home_team.runs))

    def _check_if_late_inning(self):
        if self.inning >= (self.late_inning_base_change or 0) and self.late_inning_base_change:
            # print('starting with runners on ', self.late_inning_default)
            return self.late_inning_default
        
        else:
            return False
    
    def _play_half_inning(self, use_late_inning_default=None):
        pitching_team = self.away_team if self.bottom_of_inning else self.home_team
        batting_team = self.home_team if self.bottom_of_inning else self.away_team
        # print(batting_team.name, 'is up to bat!')
        

        i = innings.Inning(batting_team = batting_team, pitching_team = pitching_team, use_starting_base_state=use_late_inning_default)
        # if self.inning == 1:
        #     i.change_lg_avg_stats(1.1)
        # elif self.inning == 2:
        #     i.change_lg_avg_stats(.90)
        # elif self.inning == 8:
        #     i.change_lg_avg_stats(.95)
        # elif self.inning >= 9:
        #     i.change_lg_avg_stats(.10)

        while i.outs < 3:
            show_outcome_flag = False  ############ SWITCH TO SHOW BATTER OUTCOMES
            i.gen_at_bat_outcome(show_outcome=show_outcome_flag)
            if show_outcome_flag:
                i._show_base_out_situation()
        
        self.home_team.runs = batting_team.runs if self.bottom_of_inning else pitching_team.runs
        self.away_team.runs = pitching_team.runs if self.bottom_of_inning else batting_team.runs
        # self._show_score()
        

    def play_game(self):
        while self._check_end_game():
            # print()
            self.bottom_of_inning = not self.bottom_of_inning
            if not self.bottom_of_inning:
                self.inning += 1
            # print('bottom' if self.bottom_of_inning else 'top', 'of inning',self.inning)  ############ SWITCH TO INNING HEADERS
            self._play_half_inning(use_late_inning_default=self._check_if_late_inning())

