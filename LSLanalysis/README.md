# LSL Real Time analysis

## Requirements
- [`pipenv`](https://docs.pipenv.org/)
- Python 3.7
  + The code assumes a dict's order is non-random

## Set up

This project uses 

- [`homebrew`](https://brew.sh/) 
- [`pipenv`](https://docs.pipenv.org/) to manage Python dependencies.

# install homebrew & pipenv
1. open Terminal 
2. to install homebrew type `/usr/bin/ruby -e "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/master/install)"`
3. to install pipenv & python type `brew install pipenv python`


Steps to set it up `LSL analysis`:
1. When using git: Clone the repository.
2. Open Terminal an go to `LSL analysis` directory, for instance `cd /Developer/OF/of_v0.10.1/apps/HD/LSLanalysis`
2. Execute `pipenv install`. This will handle the business of setting up `virtualenv` for you, with all the required dependencies.
3. Execute `pipenv shell`. This will make sure that the `virtualenv` is up and running.


### Starting a dummy session with random data

1. Start generating random LSL streams
```
pipenv shell
python support/generate_random_samples.py
```
2. In another terminal session`, start the analysis
```
pipenv shell
python main.py
```
3. To debug the logs you can check `log/development.log` in another session
```
tail -f ./log/development.log
```
