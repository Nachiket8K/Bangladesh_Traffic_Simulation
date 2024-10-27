Created by Group 22:
|Name|Student Number|
| --- | :-- |
|Anna Noteboom|4564979|
|Auriane Tecourt|5397243|
|Floris Boendermaker|4655605|
|Job Onkenhout|4595769|
|Zara-Vé van Tetterode|4577701|

# EPA1352 Lab Assignment 1: Cleaning Data

## Introduction



Welcome to Groups 22's submission for Assignment 1! In this assignment, we improved a java visualisation of a set of data on the Bangladeshi transportation network including roads, railways, waterways, rivers and bridges. Our task was to clean the data as much as possible.
This README file presents an overview of the submission folder. The details of the cleaning process are in the jupyter notebook ('cleaning.ipynb') and the report ('EPA1352-G22-A1-Report.pdf').

## Requirements
The files necessary for the java visualisation are available on the Brightspace page of the EPA1352 course under the tab "Lab Assignments/Assignment 1 Files". You will need to download the "WBSIM_Lab1.zip" file. 

In order to run the visualisation, you will need Java 8. The visualisation does not run under Java 9. 

In order to read the jupyter notebook, you will need a python distribution (Anaconda, CPython, ...) or a development environment such as Microsoft Visual Studio. The requirements to reproduce the analysis environment can be found in the "requirements.txt" file.


## Folder Structure 
An overview of structure of this submission folder is shown below. It is followed by a detailed explanation of each sub-folder and file.
```
├── README.md         <- you are here    
├── data       
│   ├── processed     <- cleaned files 
│   └── raw           <- files copied from the original "WBSIM_Lab1.zip" file that need to be cleaned
│
├── G22-A1-cleaning.ipynb       <- The notebook used to clean the data. 
│
├── EPA1352-G22-A1-Report.pdf   <- The complete report of our cleaning process    
│
├── requirements.txt  <- The requirements file for reproducing the analysis environment
```
 **Data**: This folder contains the files that we decided to clean as well as the cleaned version of those files. The 'raw' folder contains those files as found in the Brightspace folder, the 'processed' folder contains the cleaned version of those files. The cleaning process is explained in the jupyter notebook ('EPA1352-G22-A1-Report.pdf').


**G22-A1-cleaning.ipynb**: This is the jupyter notebook that was used to clean the data. It contains a step-by-step description of the process.

**EPA1352-G22-A1-Report.pdf**: This is our report on this assignment. It contains an overview of our work as well as some reflections on the process and the results. 

**requirements.txt**: This file contains all of the requirements your python environment should fulfil in order to reproduce the analysis environment.

## How to run the visualisation
### Running the original visualisation (not cleaned)
Download the visualisation files as explained in the _Requirements_ section and unzip the file. To run the visualisation, you will need to open the "wbsim.jar" file, either by clicking on it or through your terminal. 
### Running the visualisation with the cleaned files
Download the visualisation files as explained in the _Requirements_ section and unzip the file. In the WBSIM folder, under "infrastructure", you will need to replace the "\_roads.tcv" and "BMMS_overview.xlsx" files by their cleaned counterparts, which you will find in our submission folder under "data/processed". To run the visualisation, you will need to open the "wbsim.jar" file, either by clicking on it or through your terminal. 