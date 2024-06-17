# [Data Scientist - Project Portfolio](https://morales-felix.github.io/)

## Simulating the Qatar 2022 FIFA World Cup

> Want to actually play with the Jupyter notebook? Click [here](https://github.com/morales-felix/Qatar-2022-FIFA-World-Cup-simulation/tree/master) to clone the repository and run the notebook on your local machine. Otherwise, you can click on the link below my picture.

Needless to say, I am a soccer fan*. So this was a fun project which also helped me start developing code for a future personal project. Now, the real reason I did this was a World Cup bracket challenge that I played with my coworkers. As far as I can tell, I was the only one who did this sort of thing. Did I win the bracket? Read on 😉

This simulation is heavily based upon Elo ratings found on <https://eloratings.net> as a measure of relative team strength and to update this team strength measure every time a simulated game is played.
Code to implement the Elo rating system is based on FiveThirtyEight's NFL forecasting game (<https://github.com/morales-felix/nfl-elo-game>).

Notes on Elo implementation:  

- Per <https://eloratings.net/about>, the K constant is set to 60 as this is a World Cup competition.  
- Probabilities given by the Elo rating system are binary. I came up with a workaround to convert them to ternary probabilities given that association football (a.k.a. soccer) admits three outcomes after a match (win, tie, lose).  
- I did not simulate scorelines. Rather, I simply used probabilities to decide whether a team would win, tie, or lose. As such, I did not use the goal difference multiplier specified in <https://eloratings.net/about>  
- I'll be happy to talk about the workaround, but I wouldn't take it as gospel. There might be ways to do this, but I did not research it. Wanted to have fun, not produce an academic-paper-worthy method, nor a sellable product.  
- In the end, results aren't that different from other more publicized methods. Brazil is a strong team... always.  

*Not too crazy though... As I continue to live on this Earth, I realize that fandom isn't a static thing.

### Import libraries

```python
import numpy as np
import pandas as pd
import csv
from tqdm import tqdm
from joblib import Parallel, delayed

from src.world_cup_simulator import *
```

Since I want to simulate the group stage many times to generate a distribution of outcomes, I will use the `joblib` module to parallelize the simulation. This will allow me to run the simulation many times in a reasonable amount of time. That requires me to use a function to simulate the group stage and return the results.  

```python

def run_group_stage_simulation(n, j):
    """
    Run a simulation of the group stage of the World Cup
    """
    
    teams_pd = pd.read_csv("data/roster.csv")
    
    for i in range(n):
        games = read_games("data/matches.csv")
        teams = {}
    
        for row in [
            item for item in csv.DictReader(open("data/roster.csv"))
            ]:
            teams[row['team']] = {
                'name': row['team'],
                'rating': float(row['rating']),
                'points': 0
                }
    
        simulate_group_stage(
            games,
            teams,
            ternary=True
            )
    
        collector = []
        for key in teams.keys():
            collector.append(
                {"team": key,
                f"simulation{i+1}": teams[key]['points']}
            )

        temp = pd.DataFrame(collector)
        teams_pd = pd.merge(teams_pd, temp)
    
    sim_cols = [
        a for a in teams_pd.columns if "simulation" in a]
    teams_pd[
        f"avg_pts_{j+1}"
        ] = teams_pd[sim_cols].mean(axis=1)
    not_sim = [
        b for b in teams_pd.columns if "simulation" not in b]
    simulation_result = teams_pd[not_sim]
    
    return simulation_result
```

### Simulate the group stage  
The gist is to read from two files: One defining the match schedule, the other with teams and their relative strengths (given by Elo ratings prior to the start of the event).

```python
# Reads in the matches and teams as dictionaries and proceeds with that data type
n = 100 # How many simulations to run
m = 100 # How many simulation results to collect

roster_pd = Parallel(n_jobs=5)(
    delayed(run_group_stage_simulation)(
        n, j) for j in tqdm(range(m)))

for t in tqdm(range(m)):
    if t == 0:
        roster = pd.merge(
            roster_pd[t],
            roster_pd[t+1]
            )
    elif t >= 2:
        roster = pd.merge(
            roster,
            roster_pd[t]
            )
    else:
        pass

sim_cols = [i for i in roster.columns if "avg_pts" in i]

roster['avg_sim_pts'] = roster[sim_cols].mean(axis=1)
roster['99%CI_low'] = roster[sim_cols] \
    .quantile(q=0.005, axis=1)
roster['99%CI_high'] = roster[sim_cols] \
    .quantile(q=0.995, axis=1)


not_sim = [
    j for j in roster.columns if "avg_pts" not in j]
```

Simulation is done, now take a look at the results from the group stage.

```python
roster[not_sim].sort_values(
    by=[
        'group',
        'avg_sim_pts'
        ],
    ascending=False
    )
```

| group       | team         | rating | avg_sim_pts | 99%CI_low | 99%CI_high |
|:------------|:-------------|:-------|:------------|:----------|:-----------|
| H           | Portugal     | 2006   | 5.8483      | 5.43495   | 6.32020    |
| H           | Uruguay      | 1936   | 4.2981      | 3.81435   | 4.74545    |
| H           | South Korea  | 1786   | 4.0986      | 3.66465   | 4.49030    |
| H           | Ghana        | 1567   | 1.5796      | 1.37990   | 1.84515    |
| G           | Brazil       | 2169   | 6.1151      | 5.73445   | 6.52030    |
| G           | Switzerland  | 1902   | 4.2062      | 3.69000   | 4.61535    |
| G           | Serbia       | 1898   | 2.9597      | 2.56495   | 3.30020    |
| G           | Cameroon     | 1610   | 2.3326      | 2.05970   | 2.52010    |  
| F           | Belgium      | 2007   | 6.1354      | 5.60495   | 6.47515    |
| F           | Croatia      | 1927   | 4.5970      | 4.16465	| 5.04515    |
| F           | Morocco	     | 1766	  | 2.7974      | 2.41970   | 3.27040    |
| F           | Canada       | 1776   | 2.5637      | 2.14485	| 3.02010    |  
| E           | Spain        | 2048   | 5.6514      | 5.20355   | 5.99030    |
| E           | Germany      | 1936   | 4.2981      | 3.92465   | 4.88505    |
| E           | Japan        | 1787	  | 4.0986      | 2.81990	| 3.64515    |
| E           | Costa Rica   | 1743   | 1.5796      | 2.14970	| 2.84565    |  
| D           | France       | 2005   | 5.3226      | 4.83840	| 5.58515    |
| D           | Denmark      | 1971   | 4.9913      | 4.63485   | 5.42505    |
| D           | Australia    | 1719   | 2.7047      | 2.37990   | 3.16080    |
| D           | Tunisia      | 1707   | 2.7007      | 2.20375   | 3.12565    |  
| C           | Argentina    | 2143   | 6.8043      | 6.49495   | 7.11525    |
| C           | Poland       | 1814   | 4.5490      | 3.96960   | 4.98515    |
| C           | Mexico       | 1809   | 2.9092      | 2.50990   | 3.40505    |
| C           | Saudi Arabia | 1635   | 1.7660      | 1.49000   | 2.12515    |  
| B           | England      | 1920   | 5.2230      | 4.65495   | 5.70555    |
| B           | Wales        | 1790   | 3.7854      | 3.30000   | 4.20000    |
| B           | Iran         | 1797   | 3.4933      | 3.08475   | 4.11515    |
| B           | United States| 1798   | 3.4533      | 2.93475   | 3.85515    |
| A           | Netherlands  | 2040   | 6.1407      | 5.71475   | 6.51505    |
| A           | Ecuador      | 1833   | 3.7859      | 3.36475   | 4.29565    |
| A           | Senegal      | 1687   | 3.2100      | 2.65980   | 3.65030    |
| A           | Qatar        | 1680   | 2.6475      | 2.24495	| 3.01000    |

You can see that:  

- Group A was a bit of a disappointment for me, as Ecuador and Senegal ended up flipping places. I expected more from Ecuador considering the 99% confidence interval for the points they would get.  
- Group B was a very uncertain group, given how tight the lower three teams end up in the simulation. This corresponded with reality, as the group was decided on the last match date, with the United States ultimately ending second place.  
- Group C happened exactly as I expected.  
- Group D was a surprise with Denmark and Australia flipping places.  
- Group E and F were a disaster in the prediction department... But great thing that Morocco served as the surprise team in this World Cup.  
- Nailed who qualified on Group G, but the bottom two teams flipped places. This was expected since their 99% confidence intervals overlap.  
- We can conclude the same with Group H: Portugal definitely qualified, but the second place was a flip between South Korea and Uruguay. This flip was expected given the 99% confidence intervals overlap. They even tied on points and goal difference in real life, only separating due to South Korea scoring two more goals than Uruguay.  

### Knockout stage simulation  
Here is where the fun begins.  

```python
playoff_games_pd = pd.read_csv("data/playoff_matches.csv")
playoff_teams_pd = pd.read_csv("data/playoff_roster.csv")

# Now, doing the Monte Carlo simulations
n = 10000
playoff_results_teams = []
playoff_results_stage = []

for i in tqdm(range(n)):
    overall_result_teams = dict()
    overall_result_stage = dict()
    games = read_games("data/playoff_matches.csv")
    teams = {}
    
    for row in [
        item for item in csv.DictReader(open("data/playoff_roster.csv"))]:
        teams[row['team']] = {
            'name': row['team'],
            'rating': float(row['rating'])
            }
    
    simulate_playoffs(games, teams, ternary=True)
    
    playoff_pd = pd.DataFrame(games)
    
    # This is for collecting results of simulations per team
    for key in teams.keys():
        overall_result_teams[key] = collect_playoff_results(
            key,
            playoff_pd
            )
    playoff_results_teams.append(overall_result_teams)
    
    # Now, collecting results from stage-perspective
    overall_result_stage['whole_bracket'] = playoff_pd['advances'].to_list()
    overall_result_stage['Quarterfinals'] = playoff_pd.loc[playoff_pd['stage'] == 'eigths_finals', 'advances'].to_list()
    overall_result_stage['Semifinals'] = playoff_pd.loc[playoff_pd['stage'] == 'quarterfinals', 'advances'].to_list()
    overall_result_stage['Final'] = playoff_pd.loc[playoff_pd['stage'] == 'semifinals', 'advances'].to_list()
    overall_result_stage['third_place_match'] = playoff_pd.loc[playoff_pd['stage'] == 'semifinals', 'loses'].to_list()
    overall_result_stage['fourth_place'] = playoff_pd.loc[playoff_pd['stage'] == 'third_place', 'loses'].to_list()[0]
    overall_result_stage['third_place'] = playoff_pd.loc[playoff_pd['stage'] == 'third_place', 'advances'].to_list()[0]
    overall_result_stage['second_place'] = playoff_pd.loc[playoff_pd['stage'] == 'final', 'loses'].to_list()[0]
    overall_result_stage['Champion'] = playoff_pd.loc[playoff_pd['stage'] == 'final', 'advances'].to_list()[0]
    overall_result_stage['match8'] = list(playoff_pd.loc[8, ['home_team', 'away_team']])
    overall_result_stage['match9'] = list(playoff_pd.loc[9, ['home_team', 'away_team']])
    overall_result_stage['match10'] = list(playoff_pd.loc[10, ['home_team', 'away_team']])
    overall_result_stage['match11'] = list(playoff_pd.loc[11, ['home_team', 'away_team']])
    overall_result_stage['match12'] = list(playoff_pd.loc[12, ['home_team', 'away_team']])
    overall_result_stage['match13'] = list(playoff_pd.loc[13, ['home_team', 'away_team']])
    overall_result_stage['match14'] = list(playoff_pd.loc[14, ['home_team', 'away_team']])
    overall_result_stage['match15'] = list(playoff_pd.loc[15, ['home_team', 'away_team']])
    
    playoff_results_stage.append(overall_result_stage)
```

Since I ran 10k simulations, I will now take a look at which results are the most common for Argentina.  

```python
results_teams = pd.DataFrame(playoff_results_teams)
results_teams['Argentina'].value_counts()
```

| Argentina        | Simulation count |
|:-----------------|:-----------------|
| Quarterfinals    |   4317           |  
| Champion         |   2127           |  
| Third_place      |   1209           |  
| Round_of_16      |    932           |  
| Second_place     |    905           |  
| Fourth_place     |    510           | 

I'm not showing this, but very strong teams had very similar simulation counts than Argentina. For weaker teams, the most prevalent outcome was the Round of 16.  
Now, the real question is which team most frequently won the World Cup across these 10k simulations?  

```python
results_stage = pd.DataFrame(playoff_results_stage)
results_stage['Champion'].value_counts()
```

| Team          | Champion count |
|:--------------|:---------------|
| Argentina     |  2127          |
| Brazil        |  1860          |
| Netherlands   |  1547          |
| France        |   859          |
| England       |   787          |
| Portugal      |   627          |
| Spain         |   555          |
| Croatia       |   454          |
| Switzerland   |   283          |
| Japan         |   231          |
| Morocco       |   218          |
| United States |   208          |
| Poland        |    88          |
| Senegal       |    78          |
| Australia     |    46          |
| South Korea   |    32          |

### LEARNINGS  

My simulations were predicting that Argentina was the team most likely to win the World Cup right at the end of the group stage/start of the knockout stage. But it so happens that I root for Argentina since my pre-teen years, and I've been conditioned to so much disappointment that I just couldn'tbelieve Argentina could win this World Cup. Especially after that defeat against Saudi Arabia. So I ended up not following these results when filling out my bracket...  

Needless to say, seeing Argentina winning was one of the happiest moments in my life (next to my country, Panama, qualifying for the World Cup in 2018).  

BUT I SHOULD HAVE PUT MY MONEY WHERE MY SIMULATIONS WERE AND GET SOME BRAGGING POINTS TOO!!! 😭
