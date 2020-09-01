# LSL Real Time analysis

## Requirements
- Python 3.7

## Set up

This project uses 
- [`pip3`](https://docs.pipenv.org/) to manage Python dependencies.

Steps to set it up `LSL analysis`:
1. When using git: Clone the repository.
2. Open Terminal an go to `LSL analysis` directory, and run
```
pip3 install -r requirements.txt
```

### Starting a dummy session with random data

1. Start generating random LSL streams
```
python support/generate_random_samples.py
```
or start generating sample data streams
```
python support/generate_xdf_samples.py
```
2. In another terminal session`, start the analysis
```
python main_GUI.py
```
3. To debug the logs you can check `log/development.log` in another session
```
tail -f ./log/development.log
```
