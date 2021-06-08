# Overview
**Hybrid Harmony** is a a Brain-Computer Interface (BCI) application that supports the simultaneous recording of multiple (neurophysiological) datastreams and the real-time visualization and sonification of inter-brain synchrony. The program a backend that handles data and performs analyses, and a Graphical User Interface (GUI) made with PyQt5 for interactively control the analyses. Refer to the super-repository [RhythmsofRelating](https://github.com/RhythmsOfRelating/RhythmsOfRelating) for other sub-modules such as [LabVisuals] for visualization and [LabRecorder](https://github.com/labstreaminglayer/App-LabRecorder/tree/c9a417f025552ad6b95aa747631dcd4f9d26f3b2) for recording data.<br />
Refer to
* [Software Manual](https://github.com/RhythmsOfRelating/HybridHarmony/wiki/Software-Manual) for instructions on how to interact with the software
* [Software Modules](https://github.com/RhythmsOfRelating/HybridHarmony/wiki/Software-Modules) for explanation of the backend

# Requirements
- [Python >= 3.6](https://www.python.org/downloads/)

# Installation

- This project uses [`pipenv`](https://docs.pipenv.org/) to manage Python dependencies.

- For Windows users, download the latest release and run the executable file titled `HybridHarmony vx.x.exe`. Here is [v1.0](https://github.com/RhythmsOfRelating/HybridHarmony/releases/tag/v1.0).

- For developers and Mac users, refer to the following steps:

1. When using git: Clone the repository.
```shell
$ git clone https://github.com/RhythmsOfRelating/HybridHarmony.git
```
2. (Old)After downloading Python3.x, open Terminal (MacOS) or Command Prompt (Windows) and direct to `LSLanalysis` directory, and install `pipenv`:
```shell
$ pip install pipenv
```
2.1 (New) If you have multiple versions of Python installed, the version needs to be specified so the OS knows the right  version of `pip` to use. For example, if you want to use Python3.7 run:
```shell
$ python37 -m pip install %package_name%
```
This command works also if you have only one version of Python, in that case there is no need to specify the version:
```shell
$ python -m pip install %package_name%
```
In addition, it is recommended to use `pipx` to install Python libraries in a clean and isolated environment:
```shell
$ python -m pip install --user pipx
```
Using `pipx` you can install `pipenv` with the command:
```shell
$ python -m pipx install pipenv
```
(Optional) If your shell is not able to find `pipenv` it means that the executable has not been added to your PATH variable. To add it you can do it manually using the standard procedure recommended for your OS (Windows, MacOS or Linux), otherwise you can run the following command to let `pipx` handle it for you. NOTE: this will add all the executables contained in the storage of the called version of `pipx` to the PATH variable, if you want to remove them you will need to do so manually:
```shell
$ python -m pipx ensurepath
```

3. Inside the `LSLanalysis` directory, install the dependencies:
```shell
$ pipenv install
```
4. Activate the virual environment:
```shell
$ pipenv shell
```
Note that after the initial setup, steps 1-3 can be omitted and users should start from step 4.

5. Run the python script:
```shell
$ python main_GUI.py
```
6. The following window should pop up:
<img src="https://github.com/RhythmsOfRelating/HybridHarmony/blob/master/tutorial/default.png" width="400">

7. Follow the manual to interact with the software.
