---
title: Simulation Logic
parent: Method & Model
nav_order: 3
---

# Simulation Logic

This page explains how the **behavioral model** works once the data has been cleaned and the network has been constructed. In this repository, simulation logic is the layer that turns a processed network into a living system of generated trucks, moving vehicles, bridge delays, and recorded performance metrics.

A useful way to understand the progression is:
- **Lab 2 / Assignment 2:** build the first operational truck simulation on a simplified corridor
- **Lab 3 / Assignment 3:** move from corridor logic to graph-based routing on a connected network
- **Lab 4 / Assignment 4:** enrich the model with traffic-weighted sources and sinks, richer metrics, and scenario-oriented logic

So, simulation logic here is not just “run a model.” It is a staged development of how vehicles are created, routed, delayed, removed, and measured.

---

## What “simulation logic” means in this project

The previous documentation pages explain:
- how infrastructure data is cleaned (`data.md`),
- how that cleaned data becomes a usable network (`network.md`).

Simulation logic starts after those steps. It answers questions such as:
- How are trucks generated?
- How do they choose destinations?
- How do they move across links and bridges?
- What happens when a bridge is damaged or broken?
- How is delay measured?
- How are scenario results compared?

In practical terms, the simulation model is built with **Mesa**, so the logic is organized around:
- a top-level `Model`,
- infrastructure and vehicle `Agent` classes,
- a time-stepped scheduler,
- and reporting functions that summarize results.

---

## Core agent types and their roles

Across Labs 2–4, the simulation logic uses a consistent family of agent classes.

### `Infra`
`Infra` is the base class for all infrastructure components.

It provides shared fields such as:
- `length`
- `name`
- `road_name`
- `vehicle_count`

Everything the truck can occupy or traverse inherits from this base class.

### `Link`
A `Link` represents an ordinary road segment.

In later labs, links also track how many trucks passed them, which makes them useful for post-simulation traffic analysis.

### `Bridge`
A `Bridge` is a special infrastructure element that can introduce delay.

It stores:
- bridge condition,
- whether the bridge is delayed/broken in the current run,
- accumulated total delay time,
- number of trucks passed.

The bridge is central to the project because it is the place where disruption is modeled explicitly.

### `Source`
A `Source` generates trucks.

In early versions, generation is periodic. In later versions, it becomes probability-based and weighted by traffic-demand data.

### `Sink`
A `Sink` removes trucks from the system once they reach their destination.

It also records:
- travel time,
- removed traffic counts,
- toggle states used in visualization.

### `SourceSink`
A `SourceSink` can do both jobs:
- generate vehicles,
- remove arriving vehicles.

This is important because road endpoints may serve as both origins and destinations in the network.

### `Intersection`
`Intersection` appears in the more advanced network versions. It represents a node where roads connect.

It does not have complex behavior of its own, but it is essential for routing across a network rather than only along a single corridor.

### `Vehicle`
The `Vehicle` class is the truck agent.

This is the main moving entity in the simulation. Each truck stores:
- where it was generated,
- its current location,
- its route as a sequence of infrastructure ids,
- its index along that route,
- its offset within the current infrastructure object,
- its current state (`DRIVE` or `WAIT`),
- the time it was generated,
- the time it was removed.

In Lab 4, vehicles also contribute to trajectory logging and waiting statistics.

---

## The basic simulation pattern

Across all labs, the simulation follows the same high-level cycle:

1. build the model from a processed infrastructure/network file,
2. create infrastructure agents,
3. generate trucks at source/source-sink nodes,
4. assign each truck a route,
5. advance the schedule one tick at a time,
6. move each truck along its route,
7. apply bridge waiting if needed,
8. remove trucks at sinks,
9. accumulate performance metrics,
10. repeat until the run length is complete.

This shared pattern is what makes the later labs feel like extensions of the same modeling framework rather than unrelated models.

---

## Lab 2 / Assignment 2: the first corridor simulation

The clearest first full version of the simulation logic appears in:
- `Lab 2/Mixmodel.py`

This model is still relatively simple, but it already contains the essential behavioral mechanics of the project.

### Model structure
The top-level model is `BangladeshModel`, built on Mesa’s:
- `Model`
- `BaseScheduler`
- `ContinuousSpace`

Time is modeled in **one-minute ticks**.

### Network representation in Lab 2
Lab 2 uses a corridor-style representation rather than a full graph. The model loads a CSV (`data/N1merge.csv`) and organizes path information in `path_ids_dict`.

This means vehicles do not yet compute arbitrary graph shortest paths. Instead, they use stored path sequences derived from the corridor layout.

### Truck generation in Lab 2
In Lab 2, a `Source` generates trucks at a fixed frequency:
- every `generation_frequency` ticks,
- with `generation_frequency = 5` by default.

Each generated truck:
1. receives a unique id,
2. is added to the schedule,
3. gets a path via `set_path()`,
4. starts at its generating source.

This is the first version of demand generation in the project.

### Vehicle states in Lab 2
The truck has two states:
- `DRIVE`
- `WAIT`

This is the simplest possible but very effective traffic-state machine.

#### `DRIVE`
The truck advances along the route using:
- a global speed,
- a fixed tick duration.

Distance per step is:

```text
speed × step_time
```

The model compares that distance to the remaining distance on the current infrastructure object.

#### `WAIT`
If the truck reaches a delayed bridge, it stops moving and remains in `WAIT` until its waiting time counts down to zero.

This is the basic disruption mechanism of the whole project.

### How movement works in Lab 2
The vehicle’s movement logic is implemented through:
- `drive()`
- `drive_to_next()`
- `arrive_at_next()`

#### `drive()`
This calculates how far the truck can move in the current tick.

If the truck cannot finish the current link, it just increases its local offset. If it does reach the end of the current object, it calls `drive_to_next()`.

#### `drive_to_next()`
This function advances the truck to the next infrastructure object along its route.

Special cases:
- if the next object is a `Sink`, the truck arrives and is removed,
- if the next object is a `Bridge`, bridge delay logic is applied,
- otherwise the truck either remains on the next object or recursively continues through multiple objects if enough distance remains.

#### `arrive_at_next()`
This updates the truck’s current location, resets its offset, and updates infrastructure vehicle counts.

This separation of movement into three methods remains a core design pattern in later labs too.

### Bridge logic in Lab 2
Bridge behavior is implemented in `Bridge.get_delay_time()`.

The bridge first decides whether it is delayed/broken in the current run based on:
- bridge condition (`A`, `B`, `C`, `D`)
- scenario probability settings stored in the model

If the bridge is delayed, the waiting time is sampled from a bridge-length-based distribution:
- short bridges → smaller delay ranges,
- long bridges → larger delay ranges.

This means the disruption model is probabilistic and heterogeneous.

### Metrics in Lab 2
The Lab 2 model already records several important outputs:
- average driving time,
- worst bridge name,
- worst bridge delay,
- bridge-specific total delays,
- bridge-specific truck counts.

### Scenario logic in Lab 2
The same file also includes batch-run logic where multiple scenarios are executed with different probabilities for bridge-condition categories.

This is the first version of the project’s scenario-comparison workflow.

---

## Lab 3 / Assignment 3: from corridor logic to graph-based routing

Lab 3 keeps much of the same agent behavior but places it on a richer network.

The key files are:
- `Lab 3/EPA1352-G17-A3/model/model.py`
- `Lab 3/EPA1352-G17-A3/model/components.py`
- `Lab 3/EPA1352-G17-A3/model/model_run.py`

### What changes in Lab 3
The biggest conceptual change is that the simulation is no longer tied to one predefined corridor path. Instead, the model builds a **`networkx` graph** from the processed network CSV.

### Internal graph in the model
`BangladeshModel.generate_model()` in Lab 3:
- loads `N1_N2_plus_sideroads.csv`,
- constructs a graph `G`,
- adds each processed network row as a node,
- adds weighted edges between consecutive rows on the same road.

This graph becomes the routing substrate of the simulation.

### Path management in Lab 3
Lab 3 keeps two routing ideas at once:
- `path_ids_dict` for straight road-based paths,
- `path_ids_dict_complex` for shortest paths over the graph.

The more important method here is:
- `get_route(source)`

This chooses a destination sink and then computes a shortest path with `networkx.shortest_path(..., weight='weight')`.

That means the truck is now navigating an actual graph instead of only following a corridor list.

### New infrastructure type: `Intersection`
Lab 3 introduces an `Intersection` agent. This matters because the network is now multi-road and trucks need to move across junctions.

The presence of intersections is what turns road sequences into a connected transport system.

### Vehicle behavior in Lab 3
The truck state machine remains conceptually similar:
- `DRIVE`
- `WAIT`

Movement still happens through the same method family:
- `set_path()`
- `step()`
- `drive()`
- `drive_to_next()`
- `arrive_at_next()`

This continuity is important: later labs do not replace the movement logic, they generalize the environment it runs on.

### Bridge logic in Lab 3
Bridge logic remains the same in spirit:
- determine if delay occurs from condition-based probabilities,
- sample delay from bridge-length-based ranges,
- accumulate total delay time and truck counts.

What changes is that bridge delay is now embedded in a larger network where trucks can traverse more varied paths.

### Why Lab 3 matters
Lab 3 is the point where the project becomes a true **network simulation** rather than a corridor simulation. The same behavioral ideas from Lab 2 now operate on:
- more roads,
- multiple sources and sinks,
- intersections,
- graph shortest paths.

---

## Lab 4 / Assignment 4: traffic-weighted, scenario-rich simulation logic

Lab 4 extends the network model into a more operational, metrics-rich simulation framework.

The most important files are:
- `Lab 4/EPA1352-G17-A4/model/model.py`
- `Lab 4/EPA1352-G17-A4/model/components.py`
- `Lab 4/EPA1352-G17-A4/model/model_run.py`
- `Lab 4/EPA1352-G17-A4/model/batch_run.py`

### Main themes of Lab 4
Compared with Lab 3, Lab 4 adds:
- weighted source and sink behavior,
- richer traffic accounting,
- route metadata and trajectory recording,
- fixed origin–destination mode,
- more detailed batch outputs.

### Weighted source generation
In Lab 4, `Source` and `SourceSink` agents no longer generate trucks simply every fixed number of ticks. Instead, they use an `out` probability attached to the infrastructure row.

At each step, the source tries multiple times to generate vehicles based on this probability. This ties generation to traffic preprocessing rather than a fixed universal frequency.

This is a major realism improvement because not every source should create the same amount of traffic.

### Weighted destination choice
In Lab 4, sinks have associated `in` weights. When the model chooses a destination, it uses those weights to bias sink selection.

This means:
- truck origins and destinations are no longer uniform,
- demand patterns can reflect traffic intensity,
- the simulation more closely reflects directional flow patterns.

### Fixed route mode
Lab 4 also introduces an optional **fixed route mode** with:
- `origin_id`
- `destination_id`

When these are set, the model does not pick random destinations. Instead, it consistently simulates a specific OD pair. This is useful for controlled scenarios and trajectory export.

### Vehicle tracking and trajectory logging
Lab 4 adds machinery for recording vehicle paths over time:
- `trajectory_logs`
- `truck_route_metadata`
- `record_vehicle_sample()`
- `register_vehicle()`
- `finalize_vehicle()`

This means trucks are not only simulated; their routes and sampled positions can also be exported or visualized later.

### Additional waiting and traffic metrics
Lab 4 tracks much more than travel time.

For sources, it records:
- `generated_traffic`
- `waiting_times`
- `waiting_freqs`

For sinks, it records:
- `removed_traffic`

For links and bridges, it records:
- how many trucks passed them

At the vehicle level, Lab 4 tracks:
- total time spent waiting,
- the number of waiting events.

This makes the model much stronger for post-run diagnostic analysis.

---

## Vehicle life cycle across the model

One of the clearest ways to understand the simulation is to follow a single truck.

### 1. Generation
A truck is created at a `Source` or `SourceSink`.

At creation time, it receives:
- a unique truck id,
- its generating infrastructure object,
- its creation timestamp,
- a route (set immediately after generation).

### 2. Route assignment
The truck calls `set_path()`.

Depending on the lab version, this means:
- Lab 2: choose from predefined corridor path series,
- Lab 3: compute a shortest path on the graph,
- Lab 4: compute a shortest path with weighted sink choice or fixed OD mode.

### 3. Driving
When the truck is in `DRIVE`, it advances by:

```text
speed × step_time
```

If that movement exceeds the current link length, it transitions to the next infrastructure object.

### 4. Waiting at bridges
If the next object is a delayed `Bridge`, the truck enters `WAIT` for a sampled number of ticks.

While waiting:
- the countdown decreases each step,
- in Lab 4 the truck also accumulates waiting statistics.

### 5. Continuing after delay
Once waiting time reaches zero, the truck returns to `DRIVE` and continues along its path.

### 6. Arrival and removal
If the truck reaches a `Sink`, it is removed from the schedule.

At that point the model records:
- travel time,
- removed traffic,
- and in later labs route/trajectory metadata and waiting statistics.

This life cycle is the operational heart of the entire repository.

---

## Bridge failure and delay logic

Bridge logic is central to the project’s purpose, so it deserves explicit explanation.

### Condition-based bridge failure
Each bridge has a condition category such as:
- `A`
- `B`
- `C`
- `D`

The simulation scenario provides probabilities for these categories. A bridge samples whether it is delayed/broken based on the probability associated with its condition.

This means poor-condition bridges can be made more vulnerable in scenario experiments.

### Delay instead of hard closure
In the versions present here, a broken or degraded bridge usually does **not** create a forced reroute or total closure. Instead, it produces a waiting delay.

That means the disruption model is:
- local,
- stochastic,
- and expressed as travel-time penalty rather than strict inaccessibility.

### Delay magnitude depends on bridge length
The longer the bridge, the larger the possible sampled delay range. This creates a simple but useful rule that ties disruption impact to infrastructure scale.

### Delay accumulation
Each bridge records:
- total delay time across all trucks,
- number of trucks passed.

This enables metrics such as average delay per truck at each bridge.

---

## Routing logic across labs

Routing evolves significantly through the project.

### Lab 2 routing
Lab 2 uses stored path sequences (`path_ids_dict`) based on the corridor layout. This is enough for a linear road model.

### Lab 3 routing
Lab 3 adds a graph and computes shortest paths dynamically using `networkx.shortest_path(..., weight='weight')`.

This is the first true network-routing version.

### Lab 4 routing
Lab 4 keeps graph shortest-path routing but adds:
- weighted destination choice via sink demand,
- optional fixed origin–destination mode,
- route metadata capture for each truck.

So by Lab 4, routing is no longer just movement support. It is also part of scenario control and downstream visualization/export.

---

## Metrics and outputs

The simulation collects more outputs as the labs progress.

### Core metrics present early
From Labs 2 and 3, the main reported metrics include:
- average driving time,
- worst bridge name,
- worst bridge delay.

### Expanded traffic metrics in Lab 4
Lab 4 adds a richer `compute_traffic()` output containing:
- generated traffic per source,
- removed traffic per sink,
- absolute and relative waiting times,
- absolute and relative waiting frequencies,
- truck counts per bridge,
- truck counts per link.

This makes the model suitable not just for end-result reporting, but also for network performance diagnostics.

### Batch scenarios
Lab 2 and especially Lab 4 support batch scenario execution where multiple bridge-condition probability settings are run repeatedly.

These batch runs are used to:
- compare scenarios,
- export aggregated results,
- save per-scenario CSV outputs.

This is where the simulation logic becomes an experiment engine rather than just a single animation or demonstration.

---

## How the simulation evolves across the assignments

The overall storyline is:

### Lab 2 — first working traffic-disruption model
- one main corridor,
- simple path logic,
- fixed-frequency generation,
- bridge delays,
- travel-time reporting.

### Lab 3 — network-aware route simulation
- full graph structure,
- shortest-path routing,
- intersections,
- same core vehicle behavior on a richer topology.

### Lab 4 — traffic-weighted and analysis-oriented simulation
- weighted origins and destinations,
- richer traffic accounting,
- fixed OD scenarios,
- trajectory logging,
- larger batch experiments.

This progression mirrors the development of the whole project:
- from cleaned data,
- to network structure,
- to operational traffic simulation,
- to scenario analysis.

---

## Limitations and modeling choices

The simulation logic reflects several deliberate simplifications.

### Delay instead of full rerouting or collapse
Broken bridges mainly create waiting time. They do not generally remove edges from the graph or force rerouting in the current versions documented here.

### Shared global speed
Vehicle speed is largely constant across trucks. This keeps the model simpler but does not capture heterogeneous driver or vehicle behavior.

### Demand generation is stylized
Even in Lab 4, truck generation is still a probabilistic abstraction rather than a direct replay of observed traffic trajectories.

### One-minute ticks
The tick length is simple and interpretable, but it is still a modeling choice that affects how movement and waiting are discretized.

### Routing assumes the constructed graph is valid
All route quality depends on the earlier network-construction stage being correct. If graph connectivity or weights are wrong, simulation logic will inherit those issues.

---

## Summary

Simulation logic in this repository is the behavioral layer that turns a processed transport network into a working truck-flow model.

- **Lab 2** introduces the core mechanics: truck generation, movement, bridge delay, sink removal, and basic scenario reporting.
- **Lab 3** extends those mechanics to a connected graph with shortest-path routing and intersections.
- **Lab 4** adds traffic-weighted generation and destination choice, richer bridge and traffic metrics, trajectory recording, and batch scenario analysis.

So, while preprocessing prepares the data and network construction builds the structure, simulation logic is what makes the system **dynamic, measurable, and useful for disruption experiments**.
