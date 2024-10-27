Created by Group 17:
|Name|Student Number|
| --- | :-- |
|Ivan Temme|4955196|
|Hidde Scheuer|4607325|
|Philip Mueller|5809703|
|Madalin Simion|5838363|
|Nachiket Kondhalkar|5833884|

# EPA1352 Lab Assignment 2: Broken Bridges

## Introduction

In this assignment, we expanded on a mesa-model simulating trucks driving on a road in Bangladesh. We have adapted the model to simulate trucks driving on the N1 road from Chittagong to Dhaka, and to expand the model to allow some experimentation with bridges breaking down randomly.
This README file presents an overview of the submission folder.

## Requirements
The base model is available on the Brightspace page of the EPA1352 course under the tab "Lab Assignments/Assignment 2 Files". 

In order to run the model, you will need a python distribution (Anaconda, CPython, ...) or a development environment such as Microsoft Visual Studio as well as all requirements stated in the "requirements.txt" file.

## Folder Structure 
An overview of structure of this submission folder is shown below. It is followed by a detailed explanation of each sub-folder and file.
```
├── README.md            
├── data       
│   ├── processed     
│   ├── raw           
│   └── experiments   
│
├── notebooks
│   └── dataPreProcessing.ipynb  
│   └── Analysis.ipynb 
│
├── model
│   └── README.md 
│   └── model.py 
│   └── components.py  
│   └── model_run.py    
│   └── model_viz.py.   
│   └── batch_run.py   
│
├── report
│   └── EPA1352-G17-A2-Report.pdf   
│   └── figures 
│
├── requirements.txt  
```
 **Data**:
 - The 'raw' folder contains all data files as downloaded from Brightspace. The .csv files can be used to run demos of the model (be careful to adapt the path!). The files "_roads3.csv" and "BMMS_overview.xlsx" are the base for the "N1.csv" file we create after some data cleaning in the python file "dataPreProcessing.ipynb".  
 - The 'processed' folder contains the "N1.csv" file used to run the model. 
 - The "experiments" folder contains all .csv files created after running all scenarios consecutively as per assignment instructions with "batch_run.py"
 
**Notebooks**:  This folder contains files for the cleaning process and the analysis.
- dataPreProcessing.ipynb describes the cleaning of data and the creation of the "N1.csv" file. 
- Analysis.ipynb creates all figures present in the "report/figures" sub-folder 

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



