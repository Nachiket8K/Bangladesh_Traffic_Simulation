---
title: Reproducibility
nav_order: 7
---

# Reproducibility

This page explains how to trace, rerun, and understand the workflow behind the repository. Rather than focusing on submitted PDF reports, it focuses on **where the important files live**, **how the assignments connect**, and **which scripts or notebooks produce the documented outputs**.

---

## Repository structure at a glance

The project is organized around four assignment folders:

- `Lab 1/` — data cleaning and preprocessing
- `Lab 2/` — first corridor-scale model and experiments
- `Lab 3/` — network construction and graph-based experiments
- `Lab 4/` — network analysis, richer simulation outputs, and criticality/vulnerability interpretation

The documentation site in `docs/` summarizes that workflow for readers.

---

## How the project workflow fits together

The repository can be read as a pipeline:

1. **Data & Preprocessing**  
   Clean and validate roads, LRPs, and bridges.

2. **Network Construction**  
   Merge roads and bridges into a graph-ready transport network.

3. **Simulation Logic**  
   Simulate truck movement, bridge delays, and route behavior.

4. **Experiments & Results**  
   Run scenario sweeps, compare outputs, and interpret criticality and vulnerability.

5. **Visualization**  
   Communicate the model and its results through the documentation site and interactive assets.

---

## Main source files by stage

### 1. Data preprocessing
Important sources include:
- `Lab 1/TCVData.ipynb`
- `Lab 1/RoadsLRP.ipynb`
- `Lab 1/Bridges.ipynb`
- `Lab 2/dataPreProcessing.ipynb`
- `Lab 3/EPA1352-G17-A3/notebook/Data_Processing.ipynb`
- `Lab 4/EPA1352-G17-A4/notebook/data_processing.py`

### 2. Network construction
Important sources include:
- `Lab 3/EPA1352-G17-A3/notebook/ShapefileProcessing.py`
- `Lab 3/EPA1352-G17-A3/notebook/NetworkAnalysis.py`
- `Lab 3/EPA1352-G17-A3/notebook/Data_Processing.ipynb`
- `Lab 4/EPA1352-G17-A4/notebook/data_processing.py`

### 3. Simulation logic
Important sources include:
- `Lab 2/Mixmodel.py`
- `Lab 3/EPA1352-G17-A3/model/model.py`
- `Lab 3/EPA1352-G17-A3/model/components.py`
- `Lab 4/EPA1352-G17-A4/model/model.py`
- `Lab 4/EPA1352-G17-A4/model/components.py`
- `Lab 4/EPA1352-G17-A4/model/batch_run.py`

### 4. Analysis and results
Important sources include:
- `Lab 2/Analysis.ipynb`
- `Lab 3/EPA1352-G17-A3/notebook/Analysis_Assignment3.ipynb`
- `Lab 4/EPA1352-G17-A4/notebook/Data_Analysis.ipynb`

---

## Where key inputs and outputs live

### Data inputs
Examples include:
- road geometry files such as `_roads.tcv` or `_roads3.csv`
- bridge tables such as `BMMS_overview.xlsx`
- traffic HTML files used in later assignments

### Processed/model-ready outputs
Examples include:
- cleaned road and bridge files under `Lab 1/data/processed/`
- corridor or network CSVs used in the later models
- `N1_N2_plus_sideroads.csv` as a final simulation-ready network dataset in the later labs

### Experiment outputs
Examples include:
- `all_scenarios.csv`
- per-scenario CSV outputs
- generated plots in notebook or image folders

---

## How to reproduce the logic conceptually

You do not need to start from the rawest files every time. The assignments are layered, so later labs usually build on already processed outputs.

A practical order for understanding or reproducing the work is:

1. Read the documentation pages in this order:
   - `docs/overview.md`
   - `docs/method/data.md`
   - `docs/method/network.md`
   - `docs/method/simulation.md`
   - `docs/results.md`

2. Inspect the corresponding assignment sources:
   - Lab 1 for cleaning
   - Labs 3–4 for network and simulation structure
   - Labs 2–4 for experiments and analysis

3. Re-run the relevant notebook or model file for the stage you want to inspect.

---

## Reproducing specific stages

### Reproduce the preprocessing story
Read and rerun the Lab 1 notebooks first, then compare them to the later preprocessing notebooks/scripts in Labs 2–4.

### Reproduce the network model
Use the later processed CSVs and inspect the network-building scripts in Lab 3 and Lab 4.

### Reproduce simulation experiments
Use:
- `model_run.py` for a single run
- `batch_run.py` for repeated scenario sweeps

### Reproduce result analysis
Use the analysis notebooks that read the scenario CSV outputs and generate plots and summary interpretations.

---

## Documentation-first reproducibility

This documentation site is intended to make the repository easier to reproduce conceptually before reproducing it computationally.

If you are new to the project, the best approach is:
- first understand the workflow through the docs,
- then inspect the matching notebooks and scripts,
- then rerun the part of the pipeline you care about.

That approach is usually much easier than trying to execute every assignment folder from scratch without context.

---

## Notes and limitations

- Different assignment folders sometimes label files as `raw` even when they already depend on earlier processing steps in the broader project timeline.
- Some work is notebook-based and exploratory rather than packaged as a single clean command-line pipeline.
- Results are best reproduced stage by stage rather than assuming the entire repository runs as one fully automated workflow.

---

## Summary

Reproducibility in this repository means being able to follow the chain from:
- cleaned infrastructure data,
- to network construction,
- to simulation,
- to scenario analysis,
- to documented findings.

This page helps you locate the right files and understand that sequence so you can inspect or rerun the relevant stage with the right expectations.
