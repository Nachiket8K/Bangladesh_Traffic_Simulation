Created by Group 22:
|Name|Student Number|
| --- | :-- |
|Anna Noteboom|4564979|
|Auriane Tecourt|5397243|
|Floris Boendermaker|4655605|
|Job Onkenhout|4595769|
|Zara-Vé van Tetterode|4577701|

# EPA1352 Lab Assignment 2: Broken Bridges

## Introduction

Welcome to Groups 22's submission for Assignment 2! In this assignment, we expanded on a mesa-model simulating trucks driving on a road in Bangladesh. Our task was to adapt the model to be able to simulate trucks driving up the N1 road from Chittagong to Dhaka, and to expand the model to allow some experimentation with bridges breaking down randomly.
This README file presents an overview of the submission folder.  (INCLUDE PROPER DESCRIPTION HERE)

## Requirements
The base model is available on the Brightspace page of the EPA1352 course under the tab "Lab Assignments/Assignment 2 Files". You will need to download the "WBSIM_Lab2.zip" file.
In order to run the model, you will need a python distribution (Anaconda, CPython, ...) or a development environment such as Microsoft Visual Studio as well as all requirements stated in the "requirements.txt" file.

## Folder Structure IS THE STRUCTURE CORRECT?
An overview of structure of this submission folder is shown below. It is followed by a detailed explanation of each sub-folder and file.
```
├── README.md         <- you are here    
├── data       
│   ├── processed     <-  files created after data cleaning
│   ├── raw           <- files as downloaded
│   └── experiments   <- data from experiments
│
├── notebooks
│   └── G22-01-data_processing.py  <- used to create the "N1.csv" file
│   └── G22-02-data_analysis.ipynb <- analysis and figures
│
├── model
│   └── README.md <- original README of the models, modified to fit the new model
│   └── model.py <-  modified model
│   └── components.py  <-  modified agent classes used by the modified model
│   └── model_run.py   <- runs the model as per assignment instructions 
│   └── model_viz.py.  <- runs the visualization of the model 
│   └── batch_run.py   <- runs all scenarios consecutively 
|   └── verification.py  <- verification test (not required by the assignment)
│
├── report
│   └── EPA1352-G22-A2-Report.pdf   <- A thorough explanation of our work
│   └── figures <- a folder containing all figures created by the notebooks
│
├── requirements.txt  <- The requirements file for reproducing the analysis environment
```
 **Data**:
 - The 'raw' folder contains all data files as downloaded from Brightspace. The .csv files can be used to run demos of the model (be careful to adapt the path!). The files "_road.csv" and "BMMS_overview.xlsx" are the base for the "N1.csv" file we create after some data cleaning in the python file "G22-02-data_processing.py".  
 - The 'processed' folder contains the "N1.csv" file used to run the model. 
 - The "experiments" folder contains all .csv files created after running all scenarios consecutively as per assignment instructions with "batch_run.py"
 
**Notebooks**:  This folder contains files for the cleaning process, verification test (not required by the assignment) and the creation of all figures.
- G22-01-verification.py is the verification test of whether the bridge delays are properly calculated according to assignment instructions
- G22-02-data_processing.py describes the cleaning of data and the creation of the "N1.csv" file. 
- G22-03-figures.py creates all figures present in the "report/figures" sub-folder (except for the one from the verification test)

**Model**:  This folder contains all files regarding the model and its execution
- model.py is the modified model
- components.py contains the modified agent classes used by the modified model
- model_run.py runs the model as per assignment instructions 
- model_viz.py runs the visualization of the model and was not modified in this assignment
- batch_run.py runs all scenarios consecutively as per assignment instructions

**Report**: This folder contains our report on this assignment as well all figures created by the files in the "notebooks" folder.

**requirements.txt**: This file contains all of the requirements your python environment should fulfil in order to reproduce the analysis environment.

## How to run the model
There are three main ways to run the model, whereby all necessary files are in the "model" folder:

* Launch the simulation model with visualization
```
    $ python model_viz.py
```
This configuration spins up the model for the N1 road with a dynamic visualization in the browser. Using this way to run the model is recommended for exploring the working of the model and the layout of the road.

* Launch the simulation model without visualization
```
    $ python model_run.py
```
This configuration runs the model for a duration of 5 days with a zero chance of bridges breaking down. The average driving time and the name and delay of the worst bridge will be printed to the console.

* Launch the simulation model without visualization and run all 8 scenarios
```
    $ python batch_run.py
```
This configuration runs the model for a duration of 5 days for each scenario with 10 iterations each. Average driving times, names and delays of worst bridges will be collected for each model run. Results are saved in the ../experiment folder with a .csv file for each scenario together with a file including all results.



