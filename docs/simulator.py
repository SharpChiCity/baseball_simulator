import matplotlib.pyplot as plt
import numpy as np

import teams
import games


def simulate(inning_to_start_at_second=None, n=1):
    """ Simulate a game provided an inning to start runners on 2nd base and the number of simulations desired"""
    outcomes = []
    for _ in range(1, n+1):
        cubs = teams.Team('Cubs')
        marlins = teams.Team('Marlins')
        g = games.Game(home_team=cubs, away_team=marlins, late_inning_base_change=inning_to_start_at_second)
        g.play_game()
        outcomes.append({
            'inning': g.inning, 
            'top_flag': not g.bottom_of_inning, 
            'home_team_runs': g.home_team.runs,
            'away_team_runs': g.away_team.runs,
            'total_runs': g.home_team.runs + g.away_team.runs
        })

    return outcomes


if __name__ == '__main__':
    outcomes = simulate(None, 1)
    print(outcomes)

    # all_last_innings = {'length of game': [x['inning'] for x in outcomes]}
    # all_total_runs = {'total runs per game': [x['total_runs'] for x in outcomes]}
    # home_team_runs = {'home team runs per game': [x['home_team_runs'] for x in outcomes]}
    # away_team_runs = {'away team runs per game': [x['away_team_runs'] for x in outcomes]}

    # for dataset in [all_last_innings, all_total_runs, home_team_runs, away_team_runs]:
    #     # An "interface" to matplotlib.axes.Axes.hist() method
    #     n, bins, patches = plt.hist(x=list(dataset.values())[0], bins='auto', color='#0504aa',
    #                                 alpha=0.7, rwidth=0.85)
    #     plt.grid(axis='y', alpha=0.75)
    #     plt.xlabel('Value')
    #     plt.ylabel('Frequency')
    #     plt.title(list(dataset.keys())[0])
    #     maxfreq = n.max()
    #     # Set a clean upper y-axis limit.
    #     plt.ylim(ymax=np.ceil(maxfreq / 10) * 10 if maxfreq % 10 else maxfreq + 10)
    #     plt.show()