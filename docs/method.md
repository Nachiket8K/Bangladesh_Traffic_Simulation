---
title: Method & Model
nav_order: 4
has_children: true
---

# Method & Model

This section explains how the repository turns **transport infrastructure data into a working simulation model**. It should be read as a pipeline: first the data is cleaned and prepared, then it is transformed into a network structure, and finally that network is used inside a dynamic truck-flow simulation.

Together, the pages in this section show how the project moves from:
- messy road and bridge records,
- to a structured graph/network representation,
- to a simulation-ready model used for routing, disruption analysis, and scenario experiments.

## What this section covers

### Data & Preprocessing
This page explains how the project’s infrastructure data is prepared across the assignments.

It covers:
- cleaning road and bridge datasets,
- resolving missing values and duplicates,
- correcting coordinate issues,
- filtering the infrastructure to the roads relevant for later modeling,
- producing processed datasets that can be used for network and simulation work.

### Network Construction
This page explains how the cleaned infrastructure data becomes a graph/network.

It covers:
- selecting main roads and side roads,
- merging roads and bridges into a unified network table,
- inferring intersections,
- assigning model roles such as links, bridges, intersections, and source/sink nodes,
- building graph-ready and simulation-ready network files.

### Simulation Logic
This page explains how trucks move through the constructed network and how disruption is modeled.

It covers:
- the main Mesa agent types,
- vehicle generation and removal,
- route selection,
- movement and waiting behavior,
- bridge delay logic,
- traffic and delay metrics,
- scenario execution and comparison.

## How to read these pages

The three child pages are designed to be read in order:

1. **Data & Preprocessing** — how the infrastructure data is made usable
2. **Network Construction** — how that cleaned data becomes a connected transport network
3. **Simulation Logic** — how trucks, delays, and performance metrics are modeled on top of that network

This means the Method & Model section is not just a description of code modules. It is a description of the **end-to-end modeling workflow** used throughout the repository.
