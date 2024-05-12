# Simulating the Qatar 2022 FIFA World Cup  

## Introduction

Needless to say, I am a soccer fan (not too crazy though... As I continue to live on this Earth, I realize that fandom isn't a static thing). So this was a fun project which also helped me to start developing code for future personal project of mine. Full disclosure: One big motivation to do this was a World Cup bracket challenge that I played with my coworkers. As far as I can tell, I was the only one who did this sort of thing. Did I win the bracket? Read on 😉

This simulation is heavily based upon Elo ratings found on <https://eloratings.net> as a measure of relative team strength and to update this team strength measure every time a simulated game is played.
Code to implement the Elo rating system is based on FiveThirtyEight's NFL forecasting game (<https://github.com/morales-felix/nfl-elo-game>).

Notes on Elo implementation:  

- Per <https://eloratings.net/about>, the K constant is set to 60 as this is a World Cup competition.  
- Probabilities given by the Elo rating system are binary. I came up with a workaround to convert them to ternary probabilities given that association football (a.k.a. soccer) admits three outcomes after a match (win, tie, lose).  
- I did not simulate scorelines. Rather, I simply used probabilities to decide whether a team would win, tie, or lose. As such, I did not use the goal difference multiplier specified in <https://eloratings.net/about>  
- I'll be happy to talk about the workaround, but I wouldn't take it as gospel. There might be ways to do this, but I did not research it. Wanted to have fun, not produce an academic-paper-worthy method, nor a sellable product.  
- In the end, results aren't that different from other more publicized methods. Brazil is a strong team... always.  

## Do you want to use this notebook?  

### Prerequisites  

You need to have Python and pip installed on your system. You can download Python from the official website and pip is included in the Python installation. However, I recommend using the Anaconda distribution of Python which includes pip and other useful tools.  

### Installation  

1. Clone the repository to your local machine.  
2. Navigate to the project directory.  
3. Create a fresh conda environment, and run the following:  
`pip install -r requirements.txt`  

If you run into any issues with the installation, try deleting Windows-specific packages from the `requirements.txt` file.