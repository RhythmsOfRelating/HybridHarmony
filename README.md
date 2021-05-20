# Overview
**Hybrid Harmony** is a a Brain-Computer Interface (BCI) application that supports the simultaneous recording of multiple (neurophysiological) datastreams and the real-time visualization and sonification of inter-brain synchrony. The program a backend that handles data and performs analyses, and a Graphical User Interface (GUI) made with PyQt5 for interactively control the analyses. Refer to the super-repository [RhythmsofRelating] (https://github.com/RhythmsOfRelating/RhythmsOfRelating) for other sub-modules such as [LabVisuals] for visualization and [LabRecorder] (https://github.com/labstreaminglayer/App-LabRecorder/tree/c9a417f025552ad6b95aa747631dcd4f9d26f3b2) for recording data.

# Quick Start
## Requirements
- [Python >= 3.6](https://www.python.org/downloads/)

## Installation

- This project uses [`pipenv`](https://docs.pipenv.org/) to manage Python dependencies.

- For Windows users, download the latest release and run the executable file titled `HybridHarmony vx.x.exe`. Here is [v1.0](https://github.com/RhythmsOfRelating/RhythmsOfRelating/releases/tag/v1.0).

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
![alt text](https://github.com/RhythmsOfRelating/HybridHarmony/blob/master/tutorial/default.png)

7. Follow the manual to interact with the software.

## Test Session
The following steps describe a test session using randomly generated data or pre-recorded test data. in the Test Session, users can explore HybridHarmony without connecting to headsets. Users have the option to use the default setting of HybridHarmony, by simply following steps 1,2,4,11 (**Play test data, Load EEG streams and select channels, Start the session**). Users can also customize the settings, and we provide details on the parameters below in the walkthrough. 
### Play test data
1. Click **play a random signal for testing** from the **Tools** menu.![alt text](https://github.com/RhythmsOfRelating/HybridHarmony/blob/master/tutorial/walkthrough1.png)
2. **Console** will display the following message.![alt text](https://github.com/RhythmsOfRelating/HybridHarmony/blob/master/tutorial/walkthrough2.png)
### Determine frequency bands
<br /><img src="https://github.com/RhythmsOfRelating/HybridHarmony/blob/master/tutorial/freq.png" width="400">
3. Modify the table **Frequency bands for analysis** based on frequency bands of interest to the user. The table has the following columns: <br />**Freq. Band**: Name of the frequency band  <br />**Min. Freq.**: The lower bound frequency for the band  <br />**Max. Freq.**: The upper bound frequency for the band  <br />**weight**: Weighting factor of the current band. Connectivity values will be multiplied by this factor and so the factor should not exceed 1. <br /><br />The default setting has three frequency bands: theta (4-8 Hz), alpha (8-12 Hz) and beta (12-20 Hz), with weighting factors of 1. 
### Load EEG streams and select channels 
![alt text](https://github.com/RhythmsOfRelating/HybridHarmony/blob/master/tutorial/walkthrough3.png)
4. Once finishing modifying the frequency bands table, click the button **1. load LSL streams**, and **Input data streams** should display the available EEG streams. The table has the following fixed columns: <br />**Stream ID**: Name of the EEG stream, corresponding to the 'Source_ID' field in the LSL stream info.<br />**channel count**: Number of channels, corresponding to the 'channel_count' field in the LSL stream info. Note that depending on the EEG systems, the received channels can include non-EEG ones such as counter and/or other meta-data (e.g. HybridHarmony receives 18 channels from EMOTIV-EPOC+, but the first three and the last one channels are meta-data, leaving only 14 viable EEG channels). These channels should be excluded from analysis by modifying the cells. Refer to Notes for details. <br />**sampling rate**: sampling rate of the EEG streams, corresponding to the 'nominal_srate' field in the LSL stream info.<br /><br /> The table also contains the following dynamic columns, corresponding to information the user typed in table **Frequency bands for analysis**:<br /><img src="https://github.com/RhythmsOfRelating/HybridHarmony/blob/master/tutorial/freq_input.png" width="400"><br /> <br />**theta channels**: channel numbers to use for computing connectivity values in the theta band. <br />**alpha channels**: channel numbers to use for computing connectivity values in the alpha band. <br />**beta channels**: channel numbers to use for computing connectivity values in the beta band. <br /> Format of the channel numbers For example, '6:10,1:3,16,31'  --> channels [1, 2, 3, 6, 7, 8, 9, 10, 15, 30] two EEG streams with 32 channels and 60 Hz sampling rate.  Alternatively, if **play a sample recording for testing** was clicked in step one, then there should be 4 streams with 4 channels and 256 Hz sampling rate. <br /><img src="https://github.com/RhythmsOfRelating/HybridHarmony/blob/master/tutorial/input2.png" width="400"><br />Note that the frequency bands
### Parametrize connectivity analysis
5. Select **Connectivity Type**
6. Select **Connectivity metric**
### Normalization
7. Normalization
### Other options
8. OSC
9. Power value
10. conne
### Start the session
11. Click **Start**
### Stop the session
12. click **Stop**
13. in the menu click **stop generating**

