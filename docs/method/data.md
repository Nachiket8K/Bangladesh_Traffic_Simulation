---
title: Data & Preprocessing
parent: Method & Model
nav_order: 1
---

# Data & Preprocessing

This page explains the **full data preprocessing pipeline of the project**, not just the first cleaning step. Across the repository, preprocessing evolves from **raw infrastructure cleaning** in Assignment 1 to **corridor extraction**, **network assembly**, and finally **traffic-enriched simulation input generation** in later labs.

A useful way to read the repository is:
- **Lab 1 / Assignment 1:** clean and validate raw road and bridge data
- **Lab 2 / Assignment 2:** reduce the cleaned data to a modelable N1 corridor
- **Lab 3 / Assignment 3:** expand that corridor into a connected road network with side roads and intersections
- **Lab 4 / Assignment 4:** produce a more final simulation-ready network with traffic-based source/sink weights

So, preprocessing in this project is not one isolated notebook. It is a **sequence of transformations** that gradually turns messy infrastructure records into model inputs.

---

## The big picture: what preprocessing is doing

The project ultimately simulates traffic disruptions on Bangladesh’s road network, especially disruptions caused by bridge failure. To do that, the repository needs data that is:
- geographically plausible,
- structurally consistent,
- reduced to the roads relevant for the model,
- merged into one network representation,
- enriched with traffic information for source/sink generation.

That means preprocessing serves several different roles across the labs:
1. **Cleaning** raw or imperfect infrastructure data
2. **Selecting** the subset of roads and bridges needed for a scenario
3. **Merging** road and bridge information into one unified table
4. **Transforming** cumulative chainage into per-link model lengths
5. **Detecting** intersections and network relationships
6. **Enriching** the network with traffic demand information
7. **Exporting** compact processed files for simulation and analysis

---

## Main data families used across the project

According to the assignment materials and notebooks, the project relies on several recurring data families.

### 1. Road geometry and LRP data
This data comes from RMMS-style road records and describes:
- road ids such as `N1`, `N2`, `R...`, `Z...`
- location reference points (LRPs)
- latitude and longitude
- chainage values along the road
- descriptive fields such as road-side names and crossing labels

These records are the basis for drawing roads, ordering links, and locating intersections.

### 2. Bridge inventory data
This data comes from BMMS-derived bridge files and describes:
- the road a bridge belongs to
- `LRPName`
- coordinates
- condition
- length
- bridge name
- year of construction
- chainage / kilometer position

These records are needed because bridges become explicit network elements in the later simulation model.

### 3. Traffic data
By Lab 4, the preprocessing pipeline also reads traffic tables from `.traffic.htm` files to estimate source/sink demand. This is what allows the final network to support truck generation probabilities rather than just static geometry.

### 4. Derived network/model files
Later labs produce processed CSV files that are no longer raw infrastructure data. These are model-input datasets where roads, bridges, intersections, and source/sink nodes are already structured for the agent-based model.

---

## How preprocessing changes from lab to lab

The most important thing to understand is that the meaning of “preprocessing” changes over time.

### In Lab 1
Preprocessing mainly means:
- fixing types,
- handling missing values,
- removing duplicates,
- correcting spatial outliers,
- validating whether roads and bridges can be mapped consistently.

### In Lab 2
Preprocessing becomes:
- selecting only the N1 corridor,
- matching the relevant bridges to it,
- simplifying the cleaned infrastructure into a first corridor model.

### In Lab 3
Preprocessing becomes:
- expanding beyond one road,
- identifying connected side roads,
- merging roads and bridges into one network dataset,
- creating model roles such as `sourcesink`, `link`, `bridge`, and `intersection`.

### In Lab 4
Preprocessing becomes:
- parameterized network construction,
- adding traffic demand from traffic HTML files,
- normalizing inflow and outflow probabilities,
- compressing detailed link sequences into a sparser simulation-ready network.

---

## Lab 1 / Assignment 1: cleaning the raw infrastructure foundation

Assignment 1 is the base of everything that follows. It answers a simple but critical question:

> Can the infrastructure data be trusted enough to use in a model?

The main sources used here are:
- `Lab 1/README.md`
- `Lab 1/TCVData.ipynb`
- `Lab 1/RoadsLRP.ipynb`
- `Lab 1/Bridges.ipynb`
- `EPA1352 Assignment 1 - Data Quality v2.pdf`
- `Lab 1/EPA1352-G17-A1.pdf`

### Core Assignment 1 working files
The Assignment 1 report centers on three major working files:

1. **`_roads.tcv`**  
   A compact road-geometry file containing one road per line with repeated `(lrp, lat, lon)` triplets.

2. **`Roads_InfoAboutEachLRP.xlsx`**  
   A row-based road reference table with one LRP per record.

3. **`BMMS_overview.xlsx`**  
   A processed bridge overview dataset used to locate and characterize bridges.

### Raw vs processed organization
Inside `Lab 1/data/`, the folder structure distinguishes:
- `raw/`
- `processed/`

Visible examples include:
- `raw/_roads.tcv`
- `processed/_roads.tcv`
- `raw/BMMS_overview.xlsx`
- `processed/BMMS_overview.xlsx`

This separation is the repository’s first explicit statement that data should move through a cleaning pipeline rather than be overwritten in place.

### What was done to `_roads.tcv`
In `TCVData.ipynb`, the preprocessing workflow does the following:

1. Read the tab-separated file using Python’s CSV tools.
2. Expand the repeated triplet structure into a normal pandas table with:
   - `road`
   - `lrp`
   - `lat`
   - `lon`
3. Drop non-data rows and reset the index.
4. Convert latitude and longitude values from strings into floats.
5. Detect outlier coordinates road by road.
6. Repair implausible points using neighboring values or trend extension.
7. Rebuild the cleaned data back into TCV format.
8. Write the result to `data/processed/_roads.tcv`.

This is an important pattern for the whole project: the team temporarily expands a hard-to-use source format into a table, cleans it, and then exports it again in a format later tooling expects.

### What was done to `Roads_InfoAboutEachLRP.xlsx`
In `RoadsLRP.ipynb`, the preprocessing workflow does the following:

1. Load the Excel file into pandas.
2. Inspect missing values, especially missing latitude values.
3. Examine suspicious rows and row clusters.
4. Plot roads such as `N1` to visually identify coordinate spikes.
5. Try a moving-window median-based outlier filter.
6. Introduce a stricter neighbor-based correction pass for remaining spikes.
7. Compute geometry-derived travel distance and compare it with chainage.

This notebook adds a second validation layer: it is not only cleaning coordinates, but also checking whether the road’s geometry and recorded progression along the road tell a consistent story.

### What was done to `BMMS_overview.xlsx`
In `Bridges.ipynb`, the preprocessing workflow does the following:

1. Load the bridge overview file.
2. Create a location-based identifier:
   - `UniqueID = road + LRPName`
3. Check duplicate-like entries using both `UniqueID` and `structureNr`.
4. Count missing values across the most relevant columns.
5. Sort bridges by road, LRP, amount of missingness, and construction year.
6. Deduplicate by road/LRP while preferring more complete and newer-looking records.
7. Compare bridge location keys against road location keys.
8. Outline next reconciliation steps for mismatched bridge and road references.

This bridge work is explicitly useful but incomplete: it begins the process of aligning bridges with roads, but the notebook itself notes that a full reconciliation pipeline was not finished.

### Why Lab 1 matters for later labs
Lab 1 turns messy infrastructure data into a baseline that later assignments can trust more. Without this stage:
- roads would be plotted with spikes or breaks,
- bridges could drift off roads,
- chainage-based reasoning would be less reliable,
- later network building would inherit avoidable errors.

---

## Lab 2 / Assignment 2: reducing the infrastructure to the N1 corridor

By Lab 2, preprocessing is no longer only about cleaning. It becomes about **selecting and simplifying the relevant subset of the infrastructure** for a first operational model.

The clearest source here is:
- `Lab 2/dataPreProcessing.ipynb`

### Main input files in Lab 2
The notebook loads:
- `data/_roads3.csv`
- `data/BMMS_overview.xlsx`

This shows an important project transition:
- later labs do not go all the way back to the original RMMS/BMMS raw formats,
- they reuse already processed road and bridge tables,
- preprocessing now focuses on **model relevance** rather than basic cleaning only.

### Main preprocessing steps in Lab 2
The Lab 2 notebook performs the following steps:

1. **Select the N1 corridor**
   - Filter the road dataset to `road == 'N1'`
   - Filter the bridge dataset to `road == 'N1'`

2. **Reduce bridge columns to what the model needs**
   Keep fields such as:
   - `road`
   - `LRPName`
   - `condition`
   - `length`
   - `chainage`
   - `lat`
   - `lon`
   - `name`
   - `km`
   - `constructionYear`

3. **Visually compare road and bridge geometry**
   Plot road points and bridge points together to see whether they align spatially.

4. **Check LRP overlap between roads and bridges**
   Compare bridge `LRPName` values against road `lrp` values to count:
   - coinciding LRPs,
   - bridge LRPs missing from the road table.

5. **Flag duplicates**
   Detect duplicate bridge LRPs and duplicate road LRPs.

6. **Convert cumulative chainage into segment lengths**
   The notebook converts road `chainage` values into a `length` column, then backward-differences them so each row represents a segment length instead of cumulative distance from the road origin.

7. **Remove unwanted bridge duplicates**
   The notebook filters out one side of left/right bridge duplicates by inspecting bridge names and then sorts/deduplicates bridges by `road`, `km`, and `constructionYear`.

### What Lab 2 preprocessing achieves
Lab 2 produces a **corridor-scale dataset** rather than a nationwide infrastructure dataset. This is a crucial narrowing step:
- it focuses the model on the Chittagong–Dhaka route,
- it removes irrelevant roads,
- it simplifies bridge records to those needed for the assignment,
- it prepares road lengths for simulation logic.

In other words, Lab 2 turns cleaned infrastructure into a **first model-ready corridor representation**.

---

## Lab 3 / Assignment 3: building a connected road network

In Lab 3, preprocessing evolves again. It is now about building a **connected network dataset** from cleaned roads and bridges.

The most informative source is:
- `Lab 3/EPA1352-G17-A3/notebook/Data_Processing.ipynb`

### Main input files in Lab 3
The notebook loads:
- `../data/raw/_roads3.csv`
- `../data/raw/BMMS_overview.xlsx`

Even though these are placed under a `raw` folder in the Assignment 3 structure, they are already model-oriented processed inputs relative to the original Assignment 1 infrastructure cleaning stage.

### Main preprocessing steps in Lab 3

1. **Keep the main roads `N1` and `N2`**
   This widens the scope from one corridor to a larger backbone.

2. **Identify side roads**
   The notebook looks for road ids that appear inside the `name` field of the main-road records. This is used to infer crossroads and side-road connections.

3. **Filter side roads by end-point chainage**
   Only side roads whose `LRPE` chainage exceeds a threshold are kept. This removes very short or less relevant roads.

4. **Convert cumulative chainage into segment lengths**
   As in Lab 2, cumulative road progression is transformed into per-segment lengths usable in the model.

5. **Filter bridge data to relevant roads**
   Bridges are reduced to those on the selected roads and deduplicated by `road`, `km`, and `constructionYear`.

6. **Rename and merge road and bridge records**
   `LRPName` is renamed to `lrp`, and roads and bridges are merged into a single dataframe on:
   - `road`
   - `lrp`

7. **Assign model roles**
   The merged table receives a `model_type` column:
   - `sourcesink` for `LRPS` and `LRPE`
   - `link` for ordinary road points
   - `bridge` where bridge condition data is present

8. **Fill missing values after merging**
   The notebook fills missing chainage, coordinates, names, and lengths from the bridge or road side of the merge.

9. **Sort and standardize the unified network table**
   Keep and rename only the columns useful for the model, then add integer ids.

10. **Detect intersections spatially**
    The notebook compares coordinates across roads and marks near-coincident non-bridge records as `intersection` nodes.

11. **Standardize source/sink naming**
    The notebook renames source/sink nodes to a convention like `SoSi1`, `SoSi2`, etc.

12. **Keep only side roads that truly connect**
    Roads without proper intersections to `N1` or `N2` are filtered out.

### What Lab 3 preprocessing achieves
Lab 3 does something new: it creates a **network representation** rather than just a cleaned table.

That means preprocessing now includes:
- role assignment,
- topological inference,
- bridge-road merging,
- intersection creation,
- ID standardization.

This is the point where data preprocessing starts to become indistinguishable from **network construction**.

---

## Lab 4 / Assignment 4: producing a simulation-ready, traffic-enriched network

By Lab 4, preprocessing is closest to a reproducible data-engineering workflow. It combines infrastructure, topology, and demand information into the final dataset used for simulation.

The main source is:
- `Lab 4/EPA1352-G17-A4/notebook/data_processing.py`

### Main input files in Lab 4
The script loads:
- `../data/raw/_roads3.csv`
- `../data/raw/BMMS_overview.xlsx`
- traffic HTML files from `../data/raw/traffic/`

### Main preprocessing steps in Lab 4

1. **Parameterize the road-selection logic**
   The script explicitly sets:
   - main roads (`N1`, `N2`)
   - the road type to include (for example, `N`)
   - a minimum required side-road length

   This makes the preprocessing more configurable than in earlier labs.

2. **Identify and filter side roads systematically**
   As in Lab 3, side roads are inferred from the `name` field and then filtered by road type and minimum length.

3. **Convert cumulative chainage into segment lengths**
   The script creates per-segment `length` values from cumulative chainage.

4. **Filter and deduplicate bridges**
   It keeps relevant bridge columns, removes left-side duplicates based on bridge-name patterns, and deduplicates by `road`, `km`, and `constructionYear`.

5. **Merge roads and bridges into one table**
   The script merges both datasets on `road` and `lrp`, then creates `model_type` values such as:
   - `sourcesink`
   - `link`
   - `bridge`

6. **Fill missing information from either side of the merge**
   Coordinates, names, lengths, and chainage are completed from whichever dataset contains the usable value.

7. **Infer intersections by spatial proximity**
   The script compares coordinates of records on different roads and marks close-enough matches as `intersection` nodes.

8. **Standardize naming conventions**
   - source/sink names become `SoSi1`, `SoSi2`, etc.
   - bridge names are moved into a dedicated `bridge_name` column
   - placeholder bridge names are repaired if missing

9. **Read traffic demand from `.traffic.htm` files**
   For each source/sink, the script opens the corresponding road traffic HTML file and locates the closest traffic record by chainage.

10. **Create `in` and `out` demand columns**
    Traffic values are stored as incoming and outgoing flows. If a road file contains one-way entries separately, those are preserved; otherwise traffic is split evenly.

11. **Normalize traffic to probabilities**
    Total incoming and outgoing traffic is summed, and each source/sink is converted into a share of total demand. This turns raw traffic counts into simulation generation probabilities.

12. **Compress consecutive links into a sparser network**
    The script merges runs of consecutive `link` rows into larger links, keeping a representative row and accumulated length. This reduces the final network complexity while preserving its structure.

13. **Export the final processed network file**
    The result is written to:

- `../data/processed/N1_N2_plus_sideroads.csv`

### What Lab 4 preprocessing achieves
Lab 4 creates the most complete project-wide preprocessing output:
- roads, bridges, and intersections are already unified,
- segment lengths are simulation-ready,
- source/sinks are explicit,
- traffic demand has been attached,
- the network has been sparsified for efficient simulation.

This is the clearest example of preprocessing as **final model input generation**.

---

## A cross-lab preprocessing storyline

The easiest way to understand the repository is to see each lab as one stage in a larger pipeline.

### Stage 1 — Clean the infrastructure
**Lab 1** checks whether roads and bridges can be trusted at all.

Main tasks:
- convert coordinate types,
- inspect missing values,
- repair coordinate spikes,
- remove or reduce duplicates,
- compare bridge and road references.

### Stage 2 — Build a first focused model corridor
**Lab 2** narrows the infrastructure down to the N1 route.

Main tasks:
- isolate relevant roads and bridges,
- simplify fields,
- compare LRPs,
- convert cumulative chainage to segment lengths,
- produce a corridor-specific input.

### Stage 3 — Turn corridor data into a network
**Lab 3** expands to a connected network with side roads and intersections.

Main tasks:
- select N1/N2 and side roads,
- merge road and bridge tables,
- assign model roles,
- infer intersections,
- standardize ids and names.

### Stage 4 — Add traffic and export the final model dataset
**Lab 4** enriches the network with demand information and exports the simulation-ready CSV.

Main tasks:
- parameterized road filtering,
- traffic extraction from HTML,
- demand normalization,
- sparsification of links,
- final processed export.

---

## Key preprocessing techniques used across the project

Although each lab has a different objective, several preprocessing techniques keep reappearing.

### Type conversion
Coordinates and chainage values are repeatedly converted into numeric types so they can be compared, plotted, or transformed.

### Filtering and subsetting
Later labs repeatedly filter the data by:
- road id,
- road type,
- bridge relevance,
- minimum chainage/length,
- spatial proximity.

### Deduplication
Both bridges and sometimes road references are deduplicated using practical rules such as:
- keep the newest entry,
- keep the most complete entry,
- remove left/right duplicate bridge records.

### Coordinate repair and plausibility checks
The early labs rely on visual plots and neighborhood-based rules to identify impossible geometry and replace bad coordinates.

### Merge-based integration
Roads and bridges are repeatedly joined on shared keys like:
- `road`
- `lrp` / `LRPName`

### Role assignment for simulation
By Labs 3 and 4, preprocessing explicitly creates simulation semantics such as:
- `sourcesink`
- `link`
- `bridge`
- `intersection`

### Demand enrichment
Lab 4 adds traffic data and converts it into normalized generation probabilities.

---

## Main outputs produced along the way

The outputs change as preprocessing matures.

| Stage | Typical output | Purpose |
|---|---|---|
| Lab 1 | cleaned `_roads.tcv`, cleaned `BMMS_overview.xlsx` | repair and validate infrastructure data |
| Lab 2 | N1-focused corridor table(s) | run a simplified single-corridor model |
| Lab 3 | merged road-bridge network dataset | represent a connected multi-road network |
| Lab 4 | `N1_N2_plus_sideroads.csv` | final simulation-ready network with demand information |

---

## What the current `data.md` needed beyond Assignment 1

Originally, this page mainly explained the Assignment 1 cleaning work. That was useful, but incomplete for the repository as a whole.

To explain the full project preprocessing process, the page also needs to show:
- how later labs reuse cleaned road and bridge data,
- how preprocessing shifts from cleaning to model selection,
- how roads and bridges are merged into one network structure,
- how intersections are inferred,
- how traffic demand is incorporated,
- how the final simulation input file is produced.

That full progression is what makes the rest of the repository understandable.

---

## Limitations and open questions

Even across all labs, preprocessing remains partly heuristic.

### Infrastructure cleaning is not fully automatic
Many early corrections rely on visual inspection or neighborhood assumptions rather than authoritative external validation.

### Bridge-road reconciliation is only partially resolved in the early work
The notebooks clearly improve bridge placement, but they also document unfinished reconciliation logic.

### Some preprocessing rules are assignment-specific
For example:
- filtering only N1,
- keeping only certain side roads,
- using minimum road length thresholds,
- removing one side of a left/right bridge pair,
- sparsifying consecutive links.

These choices are appropriate for the model goals, but they are not universal data-cleaning rules.

### Folder naming does not always reflect the full data history
Later labs may refer to files as `raw` within the assignment folder even though those files are already the result of earlier processing steps in the broader project timeline.

---

## Summary

The preprocessing pipeline in this repository develops in stages.

- **Lab 1** cleans and validates roads, LRPs, and bridges.
- **Lab 2** extracts a usable N1 corridor model from those cleaned datasets.
- **Lab 3** merges roads, bridges, side roads, and inferred intersections into a connected network dataset.
- **Lab 4** adds traffic demand, standardizes source/sink behavior, compresses the network, and exports a final simulation-ready CSV.

So the preprocessing story of the project is not just “clean some files.” It is a multi-assignment process that gradually transforms infrastructure records into a structured network model that later experiments and simulations can actually use.
