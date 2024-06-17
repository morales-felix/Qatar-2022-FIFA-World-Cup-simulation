# Simulating the Qatar 2022 FIFA World Cup  

## Introduction

As a soccer fan, this project was both fun and a step towards a future personal project. The real reason for this simulation was a World Cup bracket challenge with my coworkers. Was I the only one who did this? Did I win? Read on 😉

This simulation uses Elo ratings from <https://eloratings.net> to measure team strength and update it after each simulated game. The Elo implementation is based on FiveThirtyEight’s NFL forecasting game (<https://github.com/morales-felix/nfl-elo-game>).  

## Do you want to use this notebook?  

### Prerequisites

Ensure you have Python and pip installed on your system. You can download Python from the official website; pip is included. Alternatively, use the Anaconda distribution, which includes pip and other tools.

### Installation

1. Clone the repository to your local machine:  

```bash
git clone https://github.com/morales-felix/Qatar-2022-FIFA-World-Cup-simulation.git
```

2. Navigate to the project directory:  

```bash
cd Qatar-2022-FIFA-World-Cup-simulation
```  

#### Using conda environments

3. Create a fresh conda environment:  

```bash
conda env create -f environment.yml
```  

4. Activate your newly-created environment:  

```bash
conda activate world_cup
```

#### Using `pyenv` or `venv` environments  

3. Create a fresh environment (Python==3.10.14 recommended):  

```bash
pyenv virtualenv 3.10.14 [name_of_env]  # For pyenv
python -m venv [name_of_env]  # For venv
```

4. Activate the environment:  

```bash
pyenv activate [name_of_env]  # For pyenv
source [name_of_env]/bin/activate  # For venv on Unix
source [name_of_env]\Scripts\activate  # For venv on Windows
```

5. Install required packages:  

```bash
pip install -r requirements.txt
```
