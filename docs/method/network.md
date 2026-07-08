---
title: Network Construction
parent: Method & Model
nav_order: 2
---

# Network Construction

This page explains how the project turns cleaned infrastructure data into a **network that can be analyzed and simulated**. In the repository, network construction is the stage where roads, bridges, intersections, and source/sink points stop being just rows in tables and become part of a graph-like structure.

So network construction in this repository is not one single algorithm. It is a staged process that depends on earlier preprocessing and prepares the structure used by later simulation and analysis.

---

## What “network construction” means here

In transport modeling, a network is usually represented as:
- **nodes** — important locations such as origins, destinations, bridges, or intersections
- **edges** — the road segments that connect those locations
- **weights** — values such as segment length or travel cost used for routing

In this repository, network construction means converting cleaned road and bridge records into that kind of representation.

This includes:
1. selecting the roads that belong in the model,
2. attaching bridges to those roads,
3. identifying where roads intersect,
4. converting cumulative chainage into link lengths,
5. assigning simulation roles to each row,
6. exporting a structured network file,
7. building a graph for connectivity and centrality analysis.

---

## How network construction depends on preprocessing

The network-building stages do not start from the original messy infrastructure files. They rely on the earlier data-preprocessing work described in `data.md`.

That means the network stages assume:
- road coordinates are already reasonably cleaned,
- bridge duplicates are already reduced,
- LRPs and chainage values are usable,
- roads and bridges can be joined meaningfully.

In other words:
- **data preprocessing** makes the infrastructure usable,
- **network construction** organizes that infrastructure into model structure.

---

## Main inputs used for network construction

The most important network-construction inputs are:

- processed road tables such as `_roads3.csv`
- processed bridge tables such as `BMMS_overview.xlsx`
- merged/derived network tables such as `N1_N2_plus_sideroads.csv`
- GIS shapefiles such as `roads.dbf` for spatial validation and intersection discovery
- traffic HTML files in Lab 4 for turning network endpoints into demand-weighted source/sink nodes

These inputs show that network construction sits between two worlds:
- tabular infrastructure data,
- graph-based simulation and network analysis.

---

## N1 corridor as a transition step

The project narrows the problem to the **N1 corridor**. This matters because it introduces several network-oriented ideas even before a full graph is built:
- selecting one operational corridor,
- converting chainage into segment lengths,
- aligning bridges with the selected road,
- reducing the cleaned infrastructure to only the rows required for a model.

So, this stage is best understood as a **corridor-model preparation stage** rather than a full graph-construction stage.

---

## Building the first connected network

The next stage is where network construction becomes explicit.

### Goal of the this network stage
The goal is no longer just to model one linear road. Instead, the project starts building a **connected multi-road network** centered on the `N1` and `N2` roads plus the side roads that connect to them.

### Step 1: Select the main roads
The Lab 3 processing starts by filtering the road table to:
- `N1`
- `N2`

These become the network backbone.

### Step 2: Discover side roads
The notebook then identifies side roads by checking whether road ids appear inside the descriptive `name` fields of the main-road records. This is a practical heuristic for discovering roads referenced at crossroads or side-road links.

This is important because it shows that network construction is not only based on explicit topology in the raw data. Some connectivity has to be inferred from descriptive fields.

### Step 3: Filter side roads by usefulness
Not every discovered side road is kept. The notebook filters roads by whether their `LRPE` chainage exceeds a threshold. This removes very short or insignificant side roads from the network model.

This means the network is not intended to be a complete national road graph. It is a **study network** focused on roads relevant to the modeling goals.

### Step 4: Convert cumulative chainage into link lengths
The road data provides cumulative chainage values. For graph construction, the model needs segment lengths between successive rows.

The notebook therefore:
- creates a `length` column from chainage,
- subtracts previous cumulative values from later rows,
- turns each row into something closer to a link-length record.

This is one of the most important transformations in the whole network-building process, because edge weights later depend on these segment lengths.

### Step 5: Filter and prepare bridges
Relevant bridge records are selected and reduced to the columns needed for network use. The notebook removes left/right duplicate-style records and deduplicates by:
- `road`
- `km`
- `constructionYear`

At this stage, bridges stop being just descriptive inventory entries and start becoming network objects that will later matter for routing and disruption.

### Step 6: Merge roads and bridges into one network table
The bridge field `LRPName` is renamed to `lrp`, and then roads and bridges are merged on:
- `road`
- `lrp`

This is the crucial integration step that turns two separate infrastructure datasets into one joint network-oriented dataset.

### Step 7: Assign network roles with `model_type`
The Lab 3 notebook introduces a very important modeling abstraction:
- `sourcesink` for `LRPS` and `LRPE`
- `link` for ordinary road records
- `bridge` where bridge attributes are present

Later, some nodes are also reclassified as:
- `intersection`

This classification makes the dataset behave like a graph-ready network model rather than a plain table.

### Step 8: Fill missing values after merging
Because roads and bridges do not always carry identical information, the merged table fills missing values from the other side when possible.

Examples include filling:
- chainage,
- coordinates,
- names,
- segment lengths.

This helps ensure that each network row has the fields needed for graph construction.

### Step 9: Add ids and standardize the dataset
The notebook assigns integer ids to the merged rows and keeps only the most useful columns. This prepares the file for consistent graph-building and simulation use.

### Step 10: Infer intersections from spatial proximity
Lab 3 then compares coordinates across rows on different roads. If two non-bridge rows are very close in space, they are treated as an intersection and their ids/roles are updated accordingly. This is a major step in network construction because it turns separate road lines into a connected graph. Without this step, roads might exist near each other geometrically but still remain disconnected in graph form.

---

## Shapefile-assisted network interpretation 

The script:
- loads a roads shapefile (`roads.dbf`),
- loads the processed network frame,
- computes the bounding box of the modeled road area,
- clips the shapefile to that study area,
- checks which geometries touch each other,
- extracts the resulting point intersections,
- saves those points to `points_shapefile_new.csv`.

### Why this matters
This script shows that network construction is not only table-based. The team also used GIS geometry to understand where roads physically intersect.

That matters because network connectivity can be approached in at least two ways:
1. through LRP and row ordering in the tabular data,
2. through geometry relationships in the shapefile data.

So Lab 3 combines **attribute-based** and **spatial** reasoning about the network.

---

## Graph construction and network analysis

The file `NetworkAnalysis.py` shows the clearest explicit graph construction step.

### Step 1: Build a `networkx` graph
The script creates a `networkx.Graph()` and adds a node for each row in the processed CSV.

Each node stores attributes such as:
- `road`
- `length`
- `pos` = `[lon, lat]`

This means the processed table is now interpreted directly as a graph node list.

### Step 2: Add edges along each road
The script iterates through the processed rows and connects consecutive rows when they belong to the same road.

The edge weight is set to:
- `row['length']`

So graph edges represent adjacency along a road, and the weight represents the physical or modeled length of that segment.

### Step 3: Check path existence between source/sinks
The script attempts shortest-path computations between source/sink nodes. This is a very practical network-validation step: if paths cannot be found between many source/sinks, the graph is not connected enough for the intended simulations.

### Step 4: Compute centrality measures
Lab 3 computes:
- closeness centrality,
- betweenness centrality,
- degree centrality.

These metrics are then exported for bridges and intersections.

### Why this matters
This shows that network construction is not complete when a CSV is written. The next step is verifying whether the dataset behaves as a real graph:
- Are routes possible?
- Which bridges are central?
- Which intersections are structurally important?

So network analysis acts as a quality check on the constructed network.

---

## Refining the simulation-ready network

The next stage continues network construction, but in a more operational and configurable form.

### Main improvements
Nopw, the project takes the same general idea as the previous stage and makes it more explicit and simulation-ready by:
- adding configurable selection parameters,
- carrying the merge/role/intersection logic forward,
- attaching traffic demand,
- compressing the network into a more efficient representation.

### Step 1: Parameterize the road selection
The script explicitly defines:
- main roads (`N1`, `N2`)
- road type to include
- minimum side-road length

This makes the network-construction logic less hard-coded and easier to tune for model scope.

### Step 2: Keep only relevant side roads
As in Lab 3, side roads are identified from descriptive name fields, but the selection is then further restricted by:
- minimum length,
- road type.

This keeps the network interpretable and computationally manageable.

### Step 3: Create segment lengths
The script again converts cumulative chainage into per-segment `length` values. This continuity across labs shows that chainage-to-link transformation is a core network-construction operation.

### Step 4: Merge bridges and roads into one network table
Lab 4 uses the same central merge on:
- `road`
- `lrp`

and again derives `model_type` values for:
- `sourcesink`
- `link`
- `bridge`

### Step 5: Infer intersections
The script compares rows on different roads and marks sufficiently close coordinates as `intersection` nodes. This repeats and formalizes the connectivity inference introduced in Lab 3.

### Step 6: Standardize bridge and source/sink naming
Bridge names are moved into a dedicated `bridge_name` field, while source/sink nodes receive standardized names such as `SoSi1`, `SoSi2`, and so on.

This helps later simulation logic distinguish infrastructure roles more clearly.

### Step 7: Add demand information to the network
This is one of Lab 4’s most important additions.

For each source/sink node, the script:
- reads the corresponding road’s traffic HTML file,
- extracts traffic records,
- finds the row closest in chainage,
- stores inbound and outbound traffic values.

This transforms the network from a purely structural object into a **demand-carrying network**.

### Step 8: Normalize source/sink weights
The script sums total incoming and outgoing traffic and converts each source/sink’s traffic into a fraction of the total. These normalized values become the basis for truck generation probabilities in the simulation.

### Step 9: Sparsify the network
The script merges runs of consecutive `link` rows into larger representative links, accumulating their lengths. This reduces the network size while keeping its functional structure.

This is important because the simulation does not always need every tiny intermediate point if a coarser representation preserves routing behavior.

### Step 10: Export the final network file
The final processed output is written to:
- `../data/processed/N1_N2_plus_sideroads.csv`

This file is best understood as the final network-construction product before runtime simulation logic takes over.

---

## How the graph is represented in practice

The repository uses a hybrid representation.

### Table representation
The processed CSV acts as a structured network table where each row is a network element with fields such as:
- road id,
- unique id,
- model type,
- coordinates,
- segment length,
- bridge metadata,
- eventually traffic demand values.

### Graph representation
When analyzed with `networkx`, these rows become graph nodes, while adjacency between rows on the same road becomes edges.

### Weights
Edge weights are typically based on segment length. Later simulation stages can reinterpret or extend those weights into travel time or delay.

### Special node types
The project distinguishes node/function types using `model_type`:
- `sourcesink`
- `link`
- `bridge`
- `intersection`

This allows one processed dataset to support multiple later purposes:
- routing,
- agent movement,
- failure modeling,
- centrality analysis.

---

## Validation and quality checks

A network is only useful if it behaves like a network.

The repository checks this in several ways.

### Connectivity checks
Lab 3 attempts shortest-path searches between source/sink nodes. This tests whether the graph is sufficiently connected.

### Structural metrics
Centrality measures are computed for bridges and intersections. These metrics help identify critical infrastructure and also provide confidence that the graph captures meaningful topology.

### Spatial validation
The shapefile-processing step checks touching road geometries and extracts candidate intersection points. This helps compare graph logic against physical road geometry.

### Sanity of weights and paths
Because edge weights come from segment lengths derived from chainage, the network implicitly depends on the earlier preprocessing being sensible. If chainage or row ordering were broken, graph path lengths would also become unreliable.

---

## Cross-lab network construction storyline

The network story of the project can be summarized in four stages.

### Stage 1 — Clean the infrastructure
Lab 1 ensures the roads and bridges are usable enough to be modeled.

### Stage 2 — Prepare a corridor model
Lab 2 narrows the dataset to a road corridor and begins organizing it in a model-oriented way.

### Stage 3 — Build a connected graph structure
Lab 3 merges roads and bridges, infers intersections, and constructs a graph that can be analyzed with network methods.

### Stage 4 — Finalize the simulation network
Lab 4 adds demand information, makes road selection configurable, sparsifies the network, and exports the final simulation-ready dataset.

This progression is important because it shows that network construction is not separate from the rest of the project. It is the bridge between cleaned infrastructure data and the agent-based traffic simulation.

---

## Limitations and modeling choices

The network-construction process includes several assumptions and heuristics.

### Intersection inference is heuristic
Intersections are often inferred by coordinate proximity rather than from a fully authoritative topological dataset.

### The network is selective, not complete
The project intentionally keeps only roads relevant to the assignments, especially roads near `N1` and `N2` and side roads above a chosen threshold.

### Segment definitions depend on chainage logic
Because segment lengths are derived from cumulative chainage, the quality of the final graph depends on the quality of earlier preprocessing.

### Sparsification changes representation
In Lab 4, consecutive links are merged into a coarser representation. This improves simulation efficiency, but it also means the final network is an abstraction rather than a one-point-per-LRP map.

### Different files labeled “raw” may already be project-internal derivatives
As with preprocessing, later assignment folders may use “raw” to mean “input to this assignment,” even if those files already depend on earlier project cleaning stages.

---

## Summary

Network construction in this repository is the process that turns cleaned roads and bridges into a graph-compatible transport structure.
We start by preparing a corridor-scale model. Then we constructs a connected network by selecting main roads and side roads, merging road and bridge records, inferring intersections, and building a `networkx` graph. The next stage refines that network by adding traffic weights, standardizing node roles, and exporting a final simulation-ready network file.

So, while preprocessing makes the infrastructure data usable, network construction makes it **navigable, analyzable, and simulatable**.
