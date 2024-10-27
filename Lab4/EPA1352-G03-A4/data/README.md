# Data for Model Generation of Simple Transport Model Demo in MESA

Created by: 
Yilin HUANG 

Adapted by: group 22 \
|Anna Noteboom|4564979| \
|Auriane Tecourt|5397243| \
|Floris Boendermaker|4655605| \
|Job Onkenhout|4595769| \
|Zara-Vé van Tetterode|4577701|

Email:
y.huang@tudelft.nl

Version:
1.1

## Introduction

The simple transport model demo, see [../model/model.py](../model/model.py) for EPA1352 Advanced Simulation course Assignment 4, takes a `csv` input data file that specifies the infrastructure model components to be generated. The data format used **by the demo model** is described here. 

## Format

| Column    | Description   |
|----------:|:--------------|
| road      | On which road does the component belong to |
| id        | **Unique ID** of the component |
| model_type| Type (i.e. class) of the model component to be generated|
| condition | Condition of bridge objects |
| name      | Name of the object |
| lat       | Latitude in Decimal Degrees|
| lon       | Longitude in Decimal Degrees |
| length    | Length of the object in meters |
| bridge_name|  Name of the bridge components |
| in        | Fraction of trucks that pick this sourcesink object as its destination |
| out       | Fraction of trucks generated at this sourcesink object |

The column `road` is used by the model generation to classify model components by roads, i.e., on which road does a component belong to. The model generation assumes that the infrastructure model components of the same road is ordered sequentially. This means, e.g. in `demo-4.csv`, component `1000000` is connected to component `1000001`, that is connected to component `1000002`, that is connected to component `1000003`, etc., all of which are on road `N1`. Similarity, component `1000013` is connected to component `1000014`, that is connected to component `1000015`, etc., all of which are on road `N2`. Each model component has a unique id according to which the Mesa model is generated. Note that the same `intersection` component that connect different roads would have the same id. 

The column `model_type` is used by the model generation to identify which class of components to be generated. The `model_type` labels used in this column must be consistent with the labels in the `generate_model` routine. 

The column 'bridge_name' is used by the model to identify the name of each bridge. This is used to report on the worst performing and most critical bridges.

The columns 'in' and 'out' respectively indicate the proportion of traffic that is recorded at the end of each road. This determines the proportion of trucks in the simulation that gets generated at this sourcesink and the proportion of trucks that choose that sourcesink as its destination.

The rest of the information is used to instantiate the components (objects).

You may change the data format and structure if the model generation (`generate_model`) routine is adapted accordingly. 

All data files contained in this directory are used as demonstration for model generation. They are not based on real data. 
