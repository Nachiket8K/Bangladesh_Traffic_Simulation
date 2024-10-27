# EPA1352 Advanced Simulation Project: Bangladesh Transport Network Analysis

## Project Overview

This repository contains a series of assignments from the EPA1352 course focused on simulating, modeling, and analyzing the transport network of Bangladesh. Through data quality analysis, model component building, network model generation, and network analysis, this project aims to assess the criticality and vulnerability of Bangladesh's transport infrastructure.

## Contents

The project is divided into four main stages, each represented by an assignment folder:

### Stage 1: Data Quality Issues for Data-Driven Simulation
In this stage, the goal is to identify and address data quality issues in infrastructure datasets of Bangladesh, such as road and bridge data. Using the RMMS (road) and BMMS (bridge) datasets, the assignment involves developing an understanding of data inconsistencies and implementing algorithms to clean and enhance the data for reliable simulation input.

**Key Components:**
- Data quality analysis for infrastructure datasets
- Automated data cleaning and validation algorithms
- Processed output for improved simulation input files

### Stage 2: Building Components for Data-Driven Simulation
The second stage involves building components for a basic simulation model using the Mesa framework, focusing on goods transportation across the Bangladesh road network. This simulation emphasizes bridge and ferry delays and enables dynamic model generation based on road and bridge quality data.

**Key Components:**
- Component generation in Mesa for transportation simulation
- Basic model of N1 road from Chittagong to Dhaka
- Scenario-based testing of bridge delays and travel times

### Stage 3: Network Model Generation
Expanding on the model built in Stage 2, this stage incorporates the NetworkX library to create a full network model of Bangladesh's main roads, including N1 and N2. The model integrates road intersections, two-way traffic, and shortest-path routing for vehicles, enabling a more comprehensive analysis of travel delays across the network.

**Key Components:**
- NetworkX integration for network-based routing
- Model generation for interconnected main roads (N1 and N2)
- Simulation scenarios with varying bridge conditions and vehicle travel paths

### Stage 4: Network Analysis
In the final stage, we analyze the criticality and vulnerability of road segments and bridges using traffic data and simulation results. This stage focuses on the economic importance (criticality) and structural sensitivity (vulnerability) of different network components, identifying high-traffic and at-risk areas for goods transport.

**Key Components:**
- Definition and analysis of network vulnerability and criticality
- Experimental design using simulation to assess transport disruptions
- Data-driven visualization of critical and vulnerable network segments

## File Structure

The repository is organized as follows:

EPA1352_Transport_Network_Analysis/
│
├── Stage1_DataQuality/             # Data quality analysis scripts, cleaned data files, and report
│   ├── data/                       # Raw and processed data for analysis
│   ├── scripts/                    # Scripts for data validation and cleaning
│   └── report.pdf                  # Report detailing data quality issues and solutions
│
├── Stage2_ComponentBuilding/       # Component-based simulation model for goods transport
│   ├── model/                      # Model files for component generation in Mesa
│   ├── experiments/                # Output data from different simulation scenarios
│   └── report.pdf                  # Report on model design and experimental results
│
├── Stage3_NetworkModel/            # Network model generation using NetworkX and Mesa
│   ├── model/                      # Model and simulation files integrating NetworkX
│   ├── experiments/                # Simulation results for network-based scenarios
│   └── report.pdf                  # Report on network generation and analysis
│
├── Stage4_NetworkAnalysis/         # Analysis of network criticality and vulnerability
│   ├── analysis/                   # Analysis scripts and visualizations for network analysis
│   └── report.pdf                  # Final report on criticality and vulnerability analysis
│
└── README.md                       # Project overview and setup instructions


## Getting Started

### Prerequisites
- Python 3.x
- [Mesa](https://mesa.readthedocs.io/)
- [NetworkX](https://networkx.org/)

### Installation
1. Clone this repository.
2. Install the required Python libraries:
   ```bash
   pip install mesa networkx

## Usage

Navigate to each stage folder and run the respective scripts as follows:

### Data Quality Analysis (Stage 1): 
Execute the data cleaning scripts in Stage1_DataQuality/scripts/.

### Component-Based Simulation (Stage 2): 
Run model_viz.py or model_run.py in Stage2_ComponentBuilding/model/.

### Network Model Simulation (Stage 3): 
Run model_viz.py or model_run.py in Stage3_NetworkModel/model/.

### Network Analysis (Stage 4): 
Use the scripts in Stage4_NetworkAnalysis/analysis/ to visualize and analyze results.


## License
This project is for educational purposes as part of the EPA1352 Advanced Simulation course at TU Delft.