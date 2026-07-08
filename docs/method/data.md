---
title: Data & Preprocessing
parent: Method & Model
nav_order: 1
---

# Data & Preprocessing

This page explains the **data foundation of the project** for readers who are new to the repository. It focuses on data inspection, cleaning, and preparing the infrastructure data that later stages of this project build on.

The short version is:
- the project depends on **road geometry data** and **bridge inventory data**,
- those datasets contain missing values, duplicate records, and location errors,
- the notebooks apply a mix of **type conversion**, **missing-value filtering**, **duplicate resolution**, **visual inspection**, and **neighbor-based coordinate correction**,
- the cleaned outputs are then intended to support later work on network construction, simulation, and disruption analysis.

---

## Why data preprocessing and cleaning matters

Later parts of the repository assume that roads and bridges can be placed on a map with reasonable accuracy. That only works if the underlying coordinates and identifiers are trustworthy.

The goal is not just to "load some files," but to answer questions such as:
- What data is available?
- Which files represent raw inputs versus processed outputs?
- What kinds of quality problems appear in the data?
- Which cleaning steps were actually implemented?
- Which issues were still unresolved after the assignment?


---

## Where the data comes from

According to the assignment brief, the project relies primarily on two transport-infrastructure data families:

### 1. RMMS road data
RMMS is the road dataset for Bangladesh’s:
- **N roads** (National)
- **R roads** (Regional)
- **Z roads** (Zila)

This road data is used to determine:
- where roads are located,
- how roads are connected,
- where location reference points (LRPs) lie along each road.

### 2. BMMS bridge data
BMMS is the bridge dataset. It describes bridges in terms of:
- which road they belong to,
- their LRP reference,
- their coordinates,
- their condition,
- physical characteristics such as length, width, spans, and construction year.

The bridge data matters because later simulations treat bridges as vulnerable assets whose failure can disrupt traffic flow.

---

## Core files used in the Project

The Assignment 1 report narrows the broad raw datasets down to **three main working files**:

1. **`_roads.tcv`**  
   A processed road-geometry file derived from RMMS.

2. **`Roads_InfoAboutEachLRP.xlsx`**  
   A row-based table with one LRP per record.

3. **`BMMS_overview.xlsx`**  
   A processed bridge overview table derived from BMMS.

These three files are the backbone of the cleaning work described in the notebooks.

---

## Raw vs processed data layout



From the repository contents, the most visible stored artifacts are:
- `raw/_roads.tcv`
- `processed/_roads.tcv`
- `raw/BMMS_overview.xlsx`
- `processed/BMMS_overview.xlsx`

This split communicates an important project convention:
- **raw** files represent source data or provided baseline processed files,
- **processed** files represent cleaned or rewritten outputs produced by the notebooks.

The road-LRP spreadsheet `Roads_InfoAboutEachLRP.xlsx` is referenced heavily in the notebooks and report as a core road table.

---

## Dataset 1: Road geometry in `_roads.tcv`

### What the file contains
`_roads.tcv` stores road geometry in a compact tab-separated format.

Instead of storing one row per point, it stores **one road per line**, followed by repeated groups of:
- `lrp`
- `lat`
- `lon`

Conceptually, a row looks like this:

```text
road_name   lrp1 lat1 lon1 lrp2 lat2 lon2 ... lrpN latN lonN
```

This means the file is efficient for storage, but inconvenient for analysis. Most data-cleaning operations are easier in a normal table with one point per row.

### Why it matters
This file controls the **shape of the road network**. If one LRP has the wrong coordinates, the plotted road can suddenly jump hundreds of kilometers away, creating spikes or broken geometry.

### Problems identified
From the notebooks and report, the main issues with `_roads.tcv` are:
- coordinates initially being treated as strings,
- coordinate outliers that create large spikes in the map,
- some roads having suspicious or incomplete geometry,
- downstream bridge placement being affected if the road coordinates are wrong.

---

## Dataset 2: Road LRP table in `Roads_InfoAboutEachLRP.xlsx`

### What the file contains
This spreadsheet stores **one LRP per row**. Based on the report and notebook usage, the important columns include:
- `road`
- `lrp`
- `lat`
- `lon`
- `chainage`
- `name`

### Why it matters
This file is much easier to inspect than `_roads.tcv` because each LRP is already a separate row. It acts as a detailed road reference table and is useful for:
- plotting roads,
- checking missing values,
- comparing coordinate continuity,
- comparing geometric distance against chainage.

### Problems identified
The report and notebooks mention several issues:
- rows with missing latitude values,
- road-name anomalies that should not represent real roads,
- coordinate spikes and local outliers,
- inconsistencies between geometric distance and chainage,
- varying decimal precision in coordinates,
- a noisy `name` field with typos that limit its usefulness.

---

## Dataset 3: Bridge inventory in `BMMS_overview.xlsx`

### What the file contains
This file is the bridge dataset used for later modeling. Important fields called out in the report and assignment brief include:
- `road`
- `km`
- `type`
- `LRPName`
- `name`
- `length`
- `condition`
- `structureNr`
- `chainage`
- `width`
- `constructionYear`
- `spans`
- `lat`
- `lon`

### Why it matters
Bridges are later treated as critical network elements. To simulate bridge failure meaningfully, the model needs bridges to be:
- attached to the correct road,
- located at plausible coordinates,
- represented once rather than duplicated many times.

### Problems identified
The report highlights several bridge-data issues:
- duplicate bridge-like entries,
- missing spans and construction years,
- some bridges with no coordinates,
- bridge LRPs that do not map cleanly to road LRPs,
- bridge coordinates that can differ from road coordinates for the same location.

---

## Cleaning workflow implemented in the notebooks

The cleaning work is split across multiple notebooks. Each notebook has a different focus.

---

### Notebook: `TCVData.ipynb`

This notebook cleans the `_roads.tcv` road-geometry file.

#### Step 1: Read the tab-separated TCV file
The notebook opens the file with Python’s `csv` reader and uses a tab delimiter.

#### Step 2: Reshape the file into a DataFrame
Because `_roads.tcv` stores one road per line with repeated triplets, the notebook expands it into a row-based table with columns:
- `road`
- `lrp`
- `lat`
- `lon`

This is a key preprocessing step because it converts a compact storage format into something pandas can work with.

#### Step 3: Drop non-data rows
The notebook explicitly drops the first two rows and resets the index. This suggests the imported structure contains header-like or otherwise non-usable entries that interfere with analysis.

#### Step 4: Convert coordinate types
The notebook checks for nulls and then converts latitude and longitude values into floats. This is necessary because the raw read treats values as strings, but plotting and distance logic require numeric coordinates.

#### Step 5: Detect and correct coordinate outliers
The central cleaning logic is road-by-road neighbor comparison. The notebook loops over each road and compares each point to surrounding points. When a point is far from its neighbors, it is treated as an outlier and corrected using local interpolation or trend extension.

The implemented logic includes several cases:
- **point far from both neighbors** → replace with the average of surrounding points,
- **point far from previous points only** → extend the earlier local trend,
- **last point is implausible** → extrapolate from previous points,
- **first point is implausible** → extrapolate from later points.

This is a heuristic method, not a formal GIS correction pipeline. Its strength is that it preserves most of the road while repairing obvious spikes.

#### Step 6: Rebuild and write the cleaned TCV file
After correction, the notebook reconstructs the TCV-style string format and writes a cleaned file to:

- `data/processed/_roads.tcv`

So the notebook not only analyzes the road data but also recreates the output in the same format expected by downstream tooling.

---

### Notebook: `RoadsLRP.ipynb`

This notebook cleans the row-based road LRP spreadsheet.

#### Step 1: Load the Excel file
The notebook reads:

- `data/Roads_InfoAboutEachLRP.xlsx`

into a pandas DataFrame.

#### Step 2: Inspect missing values
It checks `isnull().sum()` and then specifically examines rows where `lat` is missing. The notebook comments indicate that missing values often occur in row clusters and that many such rows can be dropped because they do not carry useful point-location information.

#### Step 3: Visualize roads to find spikes
The notebook uses scatter plots, such as plotting road `N1`, to inspect whether coordinates follow a sensible spatial pattern. This visual step is important because many of the problems are geometric rather than purely tabular.

#### Step 4: Apply a moving-window outlier filter
An early cleaning attempt computes rolling median-based bounds over neighboring points and checks whether the current point falls outside a tight tolerance. If it does, the point is repositioned between adjacent points.

The notebook tracks whether longitude (`Xchanged`) and/or latitude (`Ychanged`) were altered. This is useful both for debugging and for understanding how aggressive the cleaning was.

#### Step 5: Apply a stricter neighbor-based correction pass
The notebook then introduces a stronger algorithm, again marked as long-running, that handles several special cases similarly to `TCVData.ipynb`:
- internal spikes,
- start-of-road anomalies,
- end-of-road anomalies,
- points inconsistent with local trends.

This second pass reflects a practical insight from the notebook itself: the first method did not catch enough bad values.

#### Step 6: Compare geometry-derived distance to chainage
The notebook defines a `haversine` helper and also computes cumulative distance across successive points. It then compares that derived distance to the provided `chainage` column.

This serves two purposes:
- it checks whether the cleaned geometry behaves more realistically,
- it reveals remaining disagreement between mapped coordinates and recorded road progression.

#### What this notebook contributes
This notebook is not just about fixing coordinates. It also helps interpret what the road data means structurally by comparing:
- spatial position,
- sequential LRPs,
- cumulative travel distance,
- official chainage values.

---

### Notebook: `Bridges.ipynb`

This notebook focuses on cleaning and reconciling the bridge inventory.

#### Step 1: Load the bridge overview file
The notebook reads:

- `data/BMMS_overview.xlsx`

into pandas.

#### Step 2: Build a location-based bridge identifier
It creates:

```python
UniqueID = road + LRPName
```

This is used as a practical location key so bridges can be compared by their reported road/LRP combination.

#### Step 3: Check duplicates
The notebook checks duplicates in two ways:
- duplicate `UniqueID` values,
- duplicate `structureNr` values.

This matters because the data may include multiple records for the same apparent location, while `structureNr` remains unique.

#### Step 4: Rank rows by completeness
The notebook creates a `count_NaN` column over the most relevant bridge attributes. It then sorts rows by:
- `road`
- `LRPName`
- `count_NaN`
- `constructionYear` (descending)

This is a very practical deduplication strategy:
- prefer rows with **fewer missing fields**,
- among similar rows, prefer the one that appears **newer**.

#### Step 5: Drop duplicates by road/LRP combination
After sorting, the notebook removes duplicates on:
- `road`
- `LRPName`

keeping the first record in the sorted order.

#### Step 6: Compare bridge LRPs to road LRPs
The notebook then loads the road-LRP data and constructs similar `UniqueID` values on the road side. It compares the set of bridge location keys against road location keys to estimate how many bridges can be mapped directly onto road LRPs.

This is an important integration step because bridges are only useful for later simulation if they can be attached to the road network.

#### Step 7: Record unfinished next steps
The notebook explicitly says the cleaning was not fully completed. It proposes the next reconciliation logic:
- if a bridge LRP exists in road LRPs and coordinates match, keep it,
- if the LRP exists but coordinates differ slightly, decide which coordinate source to trust,
- if the LRP does not exist, inspect naming or mapping inconsistencies and repair them.

#### Output
The cleaned bridge table is written out as an Excel file in processed form.

---

## What kinds of cleaning were required?

Across the notebooks, the required cleaning falls into a few recurring categories.

### 1. Data-type correction
Some coordinates were not initially usable as numbers. They had to be converted from strings into floats before any plotting or distance logic could work.

### 2. Missing-value handling
Rows with missing critical coordinates had to be identified and, in some cases, removed or deprioritized.

### 3. Duplicate resolution
Bridge records were not always unique at the road/LRP level, so deduplication rules were needed.

### 4. Geometric outlier correction
Some road points produced obvious spatial spikes. These were corrected using neighboring points and local trend assumptions.

### 5. Cross-dataset consistency checking
Road and bridge datasets had to be compared through shared identifiers such as road name and LRP name.

### 6. Plausibility checking with derived measures
For roads, cumulative distance was compared with chainage to see whether geometry and progression along the road were telling a consistent story.

---

## Known data quality issues

The report and notebooks make it clear that the data is usable, but not clean by default.

### Road-related issues
- coordinates imported in an inconvenient type format,
- outlier LRPs creating long visual spikes,
- missing coordinate rows,
- chainage values that may not align perfectly with geometry,
- name-field inconsistencies and typos,
- possible cases where road updates changed geometry more than identifiers.

### Bridge-related issues
- duplicate bridge-like records at the same apparent location,
- missing spans, years, or coordinates,
- LRPs that do not map neatly onto the road dataset,
- coordinate disagreement between bridge and road sources.

---

## Outputs passed to later stages

The purpose of data preprocessing is to prepare inputs for the next phases of the project.

The cleaned outputs support later work by providing:
- a cleaner `_roads.tcv` for road geometry,
- a cleaner bridge overview table,
- better confidence that roads and bridges can be mapped into a network,
- a basis for later network generation and traffic simulation.

In practical terms, later assignments depend on Assignment 1 to reduce the risk that:
- roads are drawn in the wrong place,
- bridges float away from their roads,
- disruptions are simulated on incorrect assets.

---

## Limitations and open questions

### Heuristic methods
Much of the road cleaning is based on local-neighbor heuristics. These are effective for obvious spikes, but they are not guaranteed to reconstruct the true geometry in every case.

### Partial bridge reconciliation
The bridge notebook begins the road-bridge matching process but does not fully complete it. The notebook itself documents intended next steps rather than a fully finished reconciliation pipeline.

### Not every field was equally important
The team prioritized fields most relevant to later simulation work, especially:
- road placement,
- bridge placement,
- bridge condition,
- mapping consistency.

Other attributes were less central if they did not directly affect network structure or disruption behavior.

### Later assignments may rely on cleaned outputs without replaying every step
The repository contains the notebooks and processed files, but later parts of the project may consume the cleaned data as an established baseline rather than rerunning Assignment 1 from scratch each time.

---

## Summary

Data preprocessing and Cleaning establishes the project’s data foundation.

It introduces three main infrastructure datasets:
- `_roads.tcv` for road geometry,
- `Roads_InfoAboutEachLRP.xlsx` for detailed road reference points,
- `BMMS_overview.xlsx` for bridge inventory data.

The preprocessing work then:
- converts coordinates into usable numeric types,
- removes or deprioritizes incomplete records,
- resolves bridge duplicates,
- corrects obvious road-coordinate spikes,
- compares spatial data against chainage and cross-dataset identifiers,
- writes cleaned outputs for later modeling stages.

If you are trying to understand how the rest of the repository works, this is the best place to start: later network and simulation work only makes sense because this earlier step turns messy infrastructure data into something that can be analyzed more reliably.
