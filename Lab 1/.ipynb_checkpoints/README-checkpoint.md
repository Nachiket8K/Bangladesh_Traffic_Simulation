Created by Group 17:
|Name|Student Number|
| --- | :-- |
|Ivan Temme|4955196|
|Hidde Scheuer|4607325|
|Philip Mueller|5809703|
|Madalin Simion|5838363|
|Nachiket Kondhalkar|5833884|

# EPA1352 Lab Assignment 1: Data Cleaning

## Introduction

In this assignment, we were presented with a dataset of data on the Bangladeshi transportation network including roads, railways, waterways, rivers and bridges. Our task was to clean the data to the best of our abilities.
This README file presents an overview of the submission folder. The details of the cleaning process are split between three jupyter notebooks (‘TCVData.ipynb’ , ’RoadsLRP.ipynb’ and, ’Bridges.ipynb’) and the report ('EPA1352-G17-A1-Report.pdf').
## Requirements
The files necessary for the java visualization are available on the Brightspace page of the EPA1352 course under the tab "Lab Assignments/Assignment 1 Files". You will need to download the "WBSIM_Lab1.zip" file. 
In order to read the jupyter notebook, you will need a python distribution (Anaconda, CPython, ...) or a development environment such as Microsoft Visual Studio. The requirements to reproduce the analysis environment can be found in the "requirements.txt" file.
## Folder Structure 
An overview of structure of this submission folder is shown below. It is followed by a detailed explanation of each sub-folder and file.
```
├── README.md    
├── data       
│   ├── processed     <- cleaned files 
│   └── raw           <- files copied from the original "WBSIM_Lab1.zip" file that need to be cleaned
│
├── G17-A1-TCVData.ipynb       <- The notebook used to clean the data from _roads.tcv. 
├── G17-A1-RoadsLRP.ipynb      <- The notebook used to clean the data from Roads_InfoAboutEachLRP.xlsx file.
├── G17-A1-Bridges.ipynb        <- The notebook used to clean the data from BMMS_overview.xlsx.
│
├── EPA1352-G17-A1-Report.pdf   <- The complete report of our cleaning process    
│
├── requirements.txt  <- The requirements file for reproducing the analysis environment
```
 **data**: This folder contains the files that we decided to clean as well as the cleaned version of those files. This folder contains those files as found in the Brightspace folder, the 'processed' folder contains the cleaned version of those files. 
