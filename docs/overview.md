---
title: Project Overview
nav_order: 3
---

# Project Overview

This project explores how **truck flows on Bangladesh’s road network** are affected by the condition and disruption of bridges. The repository combines infrastructure data preparation, network modeling, simulation, and scenario analysis to study which roads and bridges matter most for transport performance.

At its core, the project asks two connected questions:
- how can road and bridge data be made usable enough for modeling,
- and once that is done, what can simulation and network analysis reveal about delay, bottlenecks, criticality, and vulnerability?

---

## Problem statement

Bangladesh’s transport system depends heavily on road freight movement, while bridges act as critical connection points within that system. If a bridge is damaged, delayed, or fails, the effect can spread beyond the bridge itself by increasing travel time, reducing throughput, and weakening connectivity across the road network.

This project demonstrates how to move from messy infrastructure records to a model that can explore those effects. It combines cleaned road and bridge data with a network representation and a truck-flow simulation so that the impact of bridge disruption can be studied systematically.

---

## System boundary

### What is included
The project includes:
- roads and road reference points,
- bridges and bridge-condition information,
- a constructed transport network,
- truck generation and movement,
- bridge-delay logic,
- scenario experiments,
- network-analysis and result interpretation.

### What is excluded or simplified
The project simplifies or leaves out:
- full congestion dynamics,
- detailed driver behavior,
- complete empirical calibration of disruption probabilities,
- many transport modes other than the freight-focused road model,
- hard closure or rerouting logic in every version of the simulation.

So the model is best understood as a structured experimental representation of freight-network behavior rather than a full operational traffic forecast.

---

## End-to-end pipeline

The repository follows a consistent modeling pipeline:

**Data preprocessing → Network construction → Simulation logic → Experiments & results → Visualization / reproducibility**

### 1. Data preprocessing
The project begins by cleaning and validating the infrastructure data:
- correcting coordinate issues,
- reducing duplicates,
- checking missing values,
- preparing road and bridge datasets for later use.

### 2. Network construction
The cleaned roads and bridges are then transformed into a connected transport network:
- roads and bridges are merged,
- intersections are inferred,
- model roles are assigned,
- graph-ready datasets are produced.

### 3. Simulation logic
That network is then used inside a Mesa-based simulation:
- trucks are generated at source/source-sink nodes,
- routes are assigned,
- vehicles move through links and bridges,
- broken or degraded bridges cause stochastic delay.

### 4. Experiments and results
The simulation is run under multiple scenarios to compare:
- average driving time,
- worst bridge delay,
- traffic distribution,
- bridge/link importance,
- vulnerability and criticality patterns.

### 5. Visualization and reproducibility
Finally, the repository documents and presents the work through:
- the documentation site in `docs/`,
- analysis plots and scenario outputs,
- an interactive visualization,
- reproducibility guidance for tracing the workflow.

---

## Main project outputs

The project produces several kinds of outputs:

- **Documentation pages** explaining the method, model, and results
- **Processed datasets** used for network and simulation stages
- **Graph/network structures** derived from cleaned infrastructure data
- **Simulation outputs** from scenario runs
- **Plots and analytical summaries** for experiments and network interpretation
- **Interactive visualization assets** for communicating the system and scenarios

---

## What this documentation site contains

The documentation site is organized around the same workflow as the repository itself:

- **Project Overview** — problem, scope, and workflow
- **Method & Model** — preprocessing, network construction, and simulation logic
- **Experiments & Results** — scenario design, metrics, and findings
- **Visualization** — interactive or communicative representation of the project
- **Reproducibility** — how to follow and rerun the workflow

---

## Summary

This project is an end-to-end modeling workflow for understanding bridge disruption in Bangladesh’s freight road network.

It starts with imperfect infrastructure data, turns that data into a connected network, uses that network in a truck simulation, and then interprets the resulting delays and traffic patterns in terms of infrastructure importance and vulnerability.

The documentation pages are designed to explain that workflow step by step so that someone new to the repository can understand not only **what files exist**, but also **how the pieces fit together into one coherent project**.
