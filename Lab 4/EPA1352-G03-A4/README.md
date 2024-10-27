Created by Group 22:

|Anna Noteboom|4564979| \
|Auriane Tecourt|5397243| \
|Floris Boendermaker|4655605| \
|Job Onkenhout|4595769| \
|Zara-Vé van Tetterode|4577701|

# EPA1352 Lab Assignment 4. Network	Model Generation

Welcome to Groups 22's submission for Assignment 4! 
In this assignment, we expanded on a mesa-model simulating trucks driving on a road in Bangladesh. 
Our task was to extend the model to the point where it simulates trucks driving between ends of roads on realistic traffic data and evaluate criticality and vulnerability in the network. 
The roads considered are the N1, N2 and any national road that intersects this road with a length of at least 25 kilometers.
This README file presents an overview of the submission folder.  

## Requirements
The base model is available on the Brightspace page of the EPA1352 course under the tab "Lab Assignments/Assignment 3 Files". You will need to download the "WBSIM_Lab2.zip" file.
In order to run the model, you will need a python distribution (Anaconda, CPython, ...) or a development environment such as Microsoft Visual Studio as well as all requirements stated in the "requirements.txt" file.

## Folder Structure?
An overview of structure of this submission folder is shown below. It is followed by a detailed explanation of each sub-folder and file.
```
├── README.md                           <- you are here    
├── data       
│   └── processed                       <- files created after data cleaning
│       └── N1_N2_plus_sideroads.csv    
│   └── raw                             <- files as downloaded
│       └── _roads3.csv
│       └── BMMS_overview.xls
|       └── traffic
|           └── N1.traffic.html
|           └── N2.traffic.html
|           └── N102.traffic.html
|           └── N104.traffic.html
|           └── N204.traffic.html
|           └── N207.traffic.html
|           └── N208.traffic.html
│   └── experiments                     <- data from experiments
│       └── all_scenarios.csv
│       └── scenario0.csv
│       └── scenario1.csv
│       └── scenario2.csv
│       └── scenario3.csv
│       └── scenario4.csv
│       └── scenarios.csv
│
├── notebooks
│   └── G22-04-data_processing.ipynb                    <- used to test the data cleaning process, not necessary to run the model
│   └── G22-04-data_processing_components.py            <- definition of functions for the data cleaning process 
│   └── G22-04-data_processing.py                       <- used to create the "N1_N2_plus_sideroads.csv" file 
│   └── G22-04-network_construction_and_analysis.ipynb  <- construction and analysis of the networkx model of the network
│   └── G22-04-data_analysis.ipynb                      <- analysis of the simulation model output and figures
│
├── model
│   └── README.md           <- original README of the models, modified to fit the new model
│   └── model.py            <- modified model to account for trucks finding the shortest path between all nodes
│   └── components.py       <- included assignment 2 changes
│   └── model_run.py        <- runs the model as per assignment instructions 
│   └── model_viz.py        <- runs the visualization of the model 
│   └── batch_run.py        <- runs all scenarios consecutively   
│
├── report
│   └── EPA1352-G22-A4-Report.pdf   <- A thorough explanation of our work
│   └── figures                     <- a folder containing all figures created by the notebooks
│
├── img                 <- figures of the demo file as per the assignment
│
├── requirements.txt    <- The requirements file for reproducing the analysis environment
```
 **Data**:
 - The 'raw' folder contains all data files as downloaded from Brightspace. The files in the folder "traffic", as well as the files "_road.csv" and "BMMS_overview.xlsx" are the base for the "N1_N2_plus_sideroads.csv" file we create after some data cleaning in the python file "G22-04-data_processing.py".
 - The 'processed' folder contains the "N1_N2_plus_sideroads.csv" file used to run the model. 
 - The 'experiments' folder contains "scenarios.csv", which specifies the input for the scenario's, this indicates the probability of bridges breaking down in each scenario. the other files in the folder are all .csv files created after running all scenarios consecutively as per assignment instructions with "batch_run.py"
 - The 'network_output' folder contains the .csv file with the network analysis output. 

**Notebooks**:  This folder contains files for the cleaning process, intersection validation (bonus), and the creation of all figures for the network analysis and simulation analysis.
- G22-04-data_processing.ipynb describes the cleaning of data and the creation of the "N1_N2_plus_sideroads.csv" file. This file is actually not needed to run the model as it is the same basic code as G22-04-data_processing_components.py and G22-04-data_processing.py combined but it shows the process and logic of data cleaning for anyone interested.
- G22-04-data_processing_components.py describes all general functions needed to clean the data in the "raw" folder to a shape which is workable for the model.
- G22-04-data_processing.py loads in all functions created in the "G22-04-data_processing_components.py" and runs them on the raw data. This file can be used for any (combination of) roads.
- G22-04-network_construction_and_analysis.ipynb contains the networkx version of the road and bridges network, as well as the analysis of the network.
- G22-04-data_analysis.ipynb analyses the output of the simulation model in the different scenarios.

**Model**:  This folder contains all files regarding the model and its execution
- model.py modified model to account for trucks finding the shortest path between all nodes
- components.py contains the model as per our submission for assignment 2
- model_run.py runs the model as per assignment instructions 
- model_viz.py runs the visualization of the model and was not modified in this assignment
- batch_run.py runs all scenarios consecutively as per assignment instructions
- Readme.md contains the original README of the models, modified to fit the new model

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

