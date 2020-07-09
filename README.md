# README #

*	Made with i.e. OpenFrameworks 0.10.1, Python and more
*	To use with OF, place this repository in OF/apps/
*	To use with python follow instructions in lslanalysis readme
*	To use the apps unzip all files in Resources/zip and place in the Resources folder

# Python module breakdown
## Aquisition
#### Discovery.py
* Overview: dynamically checks and connects to LSL streams.
* Stored information: sample rate, channel count, stream IDs, “stream” objects
#### Stream.py
* Overview: directly connects to one LSL stream, making it possible to pull samples.
* Stored information: LSL stream related information, timestamps, LSL stream inlet
#### Buffer.py
* Overview: creates a buffer for “stream” objects
## Analysis
#### buffer.py
* Overview: takes acquisition.discovery instance as the argument, creates a buffer to pull data samples from.
#### analysis.py
* Overview: takes acquisition.discovery instance as the argument, pulls data samples, and perform connecivity analysis by calling correlation_preFreq
#### correlation_preFreq.py
* Overview: takes data samples (from buffer) as the argument, calculate connectivity matrix, sets up LSL outlet, and pushes results to the outlet
 
  
  
  
  
 
 
  
 






 
  
  
  
  
 
 
  
  
  
  
 
 
  
 



