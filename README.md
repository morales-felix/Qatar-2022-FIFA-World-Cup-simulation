# Simulating the Qatar 2022 FIFA World Cup

As a fun project that can develop some code for an upcoming personal project, I undertook this simulation to fill out some World Cup bracket challenges.

It is heavily based upon Elo ratings found on https://eloratings.net as a measure of relative team strength and to update this team strength measure every time a simulated game is played.  
Code to implement the Elo rating system is based on FiveThirtyEight's NFL forecasting game (https://github.com/tulachin/nfl-elo-game).

Notes on Elo implementation:  
-Per https://eloratings.net/about, the K constant is set to 60 as this is a World Cup competition.    
-Probabilities given by the Elo rating system are binary. I came up with a workaround to convert them to ternary probabilities given that association football (a.k.a. soccer) admits three outcomes after a match (win, tie, lose).  
-I did not simulate scorelines. Rather, I simply used probabilities to decide whether a team would win, tie, or lose. As such, I did not use the goal difference multiplier specified in https://eloratings.net/about  
-I'll be happy to talk about the workaround, but I wouldn't take it as gospel. There might be ways to do this, but I did not research it. Wanted to have fun, not produce an academic-paper-worthy method, nor a sellable product.  
-In the end, results aren't that different from other more publicized methods. Brazil is a strong team... always.

LEARNINGS: I should have put my money where my model was, and bet for ARGENTINA!!! It was predicting, narrowly, that Argentina would win the World Cup. It did so when I simulated the playoffs (i.e. not at the very beginning of the competition), which I did to get points in a bracket I played at work. Dang!!!
