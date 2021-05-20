# Overview
**Hybrid Harmony** is a a Brain-Computer Interface (BCI) application that supports the simultaneous recording of multiple (neurophysiological) datastreams and the real-time visualization and sonification of inter-brain synchrony. The program a backend that handles data and performs analyses, and a Graphical User Interface (GUI) made with PyQt5 for interactively control the analyses. Refer to the super-repository [RhythmsofRelating](https://github.com/RhythmsOfRelating/RhythmsOfRelating) for other sub-modules such as [LabVisuals] for visualization and [LabRecorder](https://github.com/labstreaminglayer/App-LabRecorder/tree/c9a417f025552ad6b95aa747631dcd4f9d26f3b2) for recording data.

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
<img src="https://github.com/RhythmsOfRelating/HybridHarmony/blob/master/tutorial/freq.png" width="400"><br />
3. Modify the table **Frequency bands for analysis** based on frequency bands of interest to the user. <br />
Notes:
- The table has the following columns: 
  - **Freq. Band**: Name of the frequency band
  - **Min. Freq.**: The lower bound frequency for the ban
  - **Max. Freq.**: The upper bound frequency for the band
  - **weight**: Weighting factor of the current band. Connectivity values will be multiplied by this factor and so the factor should not exceed 1.
- The default setting has three frequency bands: theta (4-8 Hz), alpha (8-12 Hz) and beta (12-20 Hz), with weighting factors of 1. 
### Load EEG streams and select channels 
![alt text](https://github.com/RhythmsOfRelating/HybridHarmony/blob/master/tutorial/add1.png)<br />
4. Once finishing modifying the frequency bands table, click the button **1. load LSL streams**, and **Input data streams** should display the available EEG streams.<br />
Notes:
- if **play a random signal for testing** was clicked in step one, the table should display two EEG streams with 32 channels and 60 Hz sampling rate. Alternatively, if **play a sample recording for testing** was clicked in step one, then there should be 4 streams with 4 channels and 256 Hz sampling rate. <br /><img src="https://github.com/RhythmsOfRelating/HybridHarmony/blob/master/tutorial/add3.png" width="400">
- The table **Input data streams** has the following *non-editable* columns:
![alt text](https://github.com/RhythmsOfRelating/HybridHarmony/blob/master/tutorial/add3.png)<br />
  - **Stream ID**: Name of the EEG stream, corresponding to the 'Source_ID' field in the LSL stream info.
  - **channel count**: Number of channels, corresponding to the 'channel_count' field in the LSL stream info.
    - Note that depending on the EEG systems, the received channels can include non-EEG ones such as counter and/or other meta-data (e.g. HybridHarmony receives 18 channels from EMOTIV-EPOC+, but the first three and the last one channels are meta-data, leaving only 14 viable EEG channels). These channels should be excluded from analysis by modifying the cells (see later steps).
  - **sampling rate**: sampling rate of the EEG streams, corresponding to the 'nominal_srate' field in the LSL stream info.
- The table also contains the following *editable* columns, corresponding to frequency band names that users typed in table **Frequency bands for analysis**:<br /><img src="https://github.com/RhythmsOfRelating/HybridHarmony/blob/master/tutorial/freq_input.png" width="400"><br />
  - **theta channels**: channel numbers to use for computing connectivity values in the theta band.
  - **alpha channels**: channel numbers to use for computing connectivity values in the alpha band.
  - **beta channels**: channel numbers to use for computing connectivity values in the beta band.
- The channel number cells can be modified uniformly for all subjects. Channel numbers should be formatted with semicolons and comas. For example '6:10,1:3,16,31' means selecting channels 1, 2, 3, 6, 7, 8, 9, 10, 16, 31.
### Parametrize connectivity analysis
<br /><img src="https://github.com/RhythmsOfRelating/HybridHarmony/blob/master/tutorial/walkthrough4.png"><br />
5. Select **Connectivity Type**.<br /> Notes:
- **Connectivity Type** determines how the connectivity values are averaged acrosss electrode pairs. If “connectivity type” is “one-to-one”, only electrode pairs in the matching position are considered (e.g., Fp1 channel of participant A is 224 only paired with Fp1 of participant B and C, etc.); alternatively, if it’s set to “all-to-all”, all electrode pairs are considered in the averaging.
<br /><img src="https://github.com/RhythmsOfRelating/HybridHarmony/blob/master/tutorial/walkthrough5.png"><br />
6. Select **Connectivity metric**. <br />Notes:
- **Connectivity metric** determines the synchrony calculation between two signals. "PLV" stands for Phase Locking Value, "CCorr" stands for Circular Correlation Coefficients. Refer to the paper for further explanation.<br />
7. Set **Window size**, the length of data segment to compute synchrony over. This value should be between 2 and 10 seconds. Default is 3 seconds.
### Normalization
Notes: 
- Normalization of connectivity values is implemented with two options: manual normalization (labeled as “Manual”) and baselining with a pre-recorded file (labeled as “from file”). With a Min-Max normalization method, the user can use either of the options, or a mixture of both with a weighting factor adjusted by the slider “Weight”. The minimum and maximum limits are then weighted between the “Manual” and “from file” options.<br />
8. To use "manual" option: type in field "Manual Min." and "Max.". These two numbers determines the minumum and maximum of the "manual" option. Values exeeding the limits will be clamp to 0 or 1.<br /><img src="https://github.com/RhythmsOfRelating/HybridHarmony/blob/master/tutorial/add2.png"><br />
9. (optional) To use "from file" option: Click **Open...** to open a pre-recorded .xdf file (for details, refer to xxx), <br /><img src="https://github.com/RhythmsOfRelating/HybridHarmony/blob/master/tutorial/norm2.png"><br />
<br /><img src="https://github.com/RhythmsOfRelating/HybridHarmony/blob/master/tutorial/norm3.png" width="400"><br />
and then click **compute** to compute minimum and maximum of the "from file" option. <br /><img src="https://github.com/RhythmsOfRelating/HybridHarmony/blob/master/tutorial/norm4.png"><br /><br /> 
10. If successful, **Console** should display the following message specifying the connectivity marker ID, info ("RValues"), number of frequency bands, and data shape (n_freq, n_timepoint). Meanwhile, "Min." and "Max." labels in "from file" option should be updated to reflect minimum and maximum computed from the baseline file.
<br /><img src="https://github.com/RhythmsOfRelating/HybridHarmony/blob/master/tutorial/norm5.png"><br />
11. Adjust the**weight** slider to determine the overall "Min." and "Max.". The leftmost side means 100% "manual" option and 0% "from file" option; the rightmost side means 0% "manual" option and 100% "from file" option. In case where "from file" option is empty, the slider simply adjusts the "manual" minimum and maximum values. <br /><img src="https://github.com/RhythmsOfRelating/HybridHarmony/blob/master/tutorial/walkthrough6.png"><br />
### Other options
12. Checkbox **sending through OSC** determines whether connectivity values are sent through [Open Sound Control](http://opensoundcontrol.org/). **OSC IP address** and **OSC port** are used to transport data.
13. Checkbox **sending power values** determines whether individual partipants' power values are sent through LSL outlet. Refer to xxx for output details.
14. Checkbox **Display connectivity values** determines whether to display connectivity values in the box below once the analysis starts.
<br /><img src="https://github.com/RhythmsOfRelating/HybridHarmony/blob/master/tutorial/add4.png"><br />
### Start the session
15. Click **2.start analysis** to start the analysis. Refer to xxx for details on the output. **Console** should display the following message, and the right side box should start updating connectivity values. Note that when analysis is running, all fields are non-editable.
<br /><img src="https://github.com/RhythmsOfRelating/HybridHarmony/blob/master/tutorial/add5.png"><br />
### Stop the session
16. click **stop analysis** to stop the analysis. **Console** should display the following message. All fields will become editable again.
<br /><img src="https://github.com/RhythmsOfRelating/HybridHarmony/blob/master/tutorial/add7.png"><br />
17. Click **stop generating** from the **Tools** menu. This will stop the incoming test data.
<br /><img src="https://github.com/RhythmsOfRelating/HybridHarmony/blob/master/tutorial/add6.png"><br />


