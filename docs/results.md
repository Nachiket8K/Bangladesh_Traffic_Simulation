---
title: Experiments & Results
nav_order: 5
---

# Experiments & Results

This page explains how the project’s experiments were designed, what outputs were measured, and what kinds of findings emerged across the assignments. As with the rest of the documentation, the key idea is that the repository develops in stages: the early experiments focus on corridor-level delay behavior, while later work expands toward network-wide criticality and vulnerability analysis.

So this page is not only about “what numbers came out.” It is about how the project turns scenarios into interpretable evidence.

---

## What “experiments and results” mean in this repository

Once the project has:
- cleaned the infrastructure data,
- built a network structure,
- and implemented traffic simulation logic,

the next step is to ask analytical questions such as:
- What happens when more bridges are vulnerable or broken?
- Which bridges create the greatest delays?
- How stable are the results across repeated runs?
- Which parts of the network are most critical for flow?
- Which parts appear most vulnerable to disruption?

The experiments in this repository answer these questions through:
- repeated scenario runs,
- measured simulation outputs,
- plots and comparisons,
- and network/traffic interpretation.

---

## How experimentation evolves across the assignments

The experiments do not stay the same throughout the project.

### In Stage 1
Experiments are mainly about:
- varying bridge-condition failure probabilities,
- observing how those settings affect driving time and delay on the `N1` corridor,
- identifying which bridge becomes the worst bottleneck.

### In Stage 2
Experiments expand to a network with `N1`, `N2`, and side roads, so results can be interpreted in a broader structural context.

### In Stage 3
Experiments become more analytical and network-oriented. Instead of only asking “how much delay occurred?”, the work increasingly asks:
- where traffic concentrates,
- which bridges are most critical,
- which locations are vulnerable,
- how simulation results relate to network structure and traffic demand.

---

## Scenario design across the project

One of the main ways the project creates experiments is by defining **scenario sets** that change how likely bridges are to be delayed or disrupted.

### Shared idea behind the scenarios
Bridges are categorized by condition classes such as:
- `A`
- `B`
- `C`
- `D`

The scenarios adjust the probabilities associated with those classes. This means the experiments can represent a progression from:
- little or no disruption,
- to increasingly severe disruption conditions.

### Repeated runs per scenario
The scenario experiments are not run only once. Multiple iterations are used so that:
- random bridge outcomes can vary,
- the spread of results can be observed,
- scenario comparisons are less dependent on one unlucky or lucky run.

### Simulation duration
The batch-run files use a model duration of:
- **5 days**, represented as minutes,
- i.e. `5 * 24 * 60` ticks.

This gives the trucks enough time to accumulate meaningful differences in travel and waiting behavior.

---

## Main metrics used across the labs

Although the exact analysis becomes richer over time, several core metrics appear repeatedly.

### Average driving time
This is the most visible performance metric in the earlier experiments. It captures how much total travel time trucks need under a given scenario.

### Worst bridge name
This identifies which bridge produced the highest average delay under a run or scenario.

### Worst bridge delay
This quantifies the size of the bottleneck created by the most delay-causing bridge.

### Delay distributions
Later analysis looks beyond just one number and examines how delay times vary by:
- scenario,
- run,
- bridge.

### Generated and removed traffic
In the more advanced models, traffic volume is also tracked at:
- source nodes,
- sink nodes,
- bridges,
- links.

### Criticality and vulnerability indicators
By Assignment 4, results are increasingly interpreted using two higher-level concepts:
- **criticality** — how important a road, bridge, or segment is for carrying traffic
- **vulnerability** — how susceptible that component is to disruption and delay

---

## Stage 1: first corridor scenario experiments


### What Stage 1 is testing
Stage 1 experiments the simplest question in the project:

> If bridge disruption probabilities increase, what happens to truck travel time along the N1 corridor?

### Data used in the analysis
The notebook reads:
- `all_scenarios.csv`

This file contains the outcomes of repeated runs across the defined scenario set.

### Main analyses in Stage 1
The notebook performs several kinds of aggregation and plotting:

1. **Average driving time per scenario**
   The analysis groups runs by scenario and calculates:
   - mean driving time,
   - minimum driving time,
   - maximum driving time.

2. **Spread across runs**
   The notebook preserves the min/max spread so it can show how variable results are within a scenario.

3. **Scenario comparison plots**
   Seaborn line and categorical plots are used to compare how average driving time changes as scenarios worsen.

4. **Delay-time analysis**
   The notebook creates boxplots or bar-style comparisons of the worst bridge delay by scenario.

5. **Worst-bridge identification**
   It sorts and counts which bridge names appear most often as the bridge with the greatest delay.

### What Stage 1 results mean
The main interpretation of Stage 1 is straightforward:
- more severe bridge-failure assumptions produce more travel delay,
- average driving times increase across scenarios,
- some bridges appear repeatedly as dominant bottlenecks.

This is the project’s first demonstration that stochastic bridge degradation can meaningfully affect corridor performance.

---

## Stage 2 / Assignment 3: experiments on a connected network

### What changes in Stage 2
The experiment pattern is similar to Stage 1, but the setting is broader:
- the network now includes `N1`, `N2`, and side roads,
- trucks route over a graph rather than a single line,
- bridges are interpreted within a more connected network structure.

### Main analyses in Stage 2
The notebook again reads:
- `../data/experiment/all_scenarios.csv`

and performs similar scenario-based comparisons, including:

1. **Average driving time by scenario**
   Means, maximums, and minimums are calculated and plotted.

2. **Scenario-run comparisons**
   Individual run results within a scenario are visualized so that readers can see variability rather than only averages.

3. **Delay-time plots**
   Delays by scenario are plotted to show how disruption intensity changes across the scenario set.

4. **Worst bridge frequency analysis**
   The analysis counts which bridges repeatedly emerge as the worst-delay bridge.

5. **Graph context**
   The notebook also rebuilds the processed network as a `networkx` graph, which helps interpret the bridge results structurally.

### What Stage 2 results add
Compared with Stage 1, Stage 2 results allow a more network-oriented interpretation:
- delays are no longer only corridor effects,
- a bridge’s importance now depends partly on its structural position,
- the result space becomes richer because route alternatives and intersections matter.

This means the analysis is moving away from “one route gets slower” and toward “the network has structurally important weak points.”

---

## Stage 3 / Assignment 4: criticality and vulnerability analysis

Stage 3 shifts the emphasis from pure scenario comparison toward **network interpretation**.

### What Assignment 4 asks for
The assignment brief explicitly frames the work around:
- **criticality** — the importance of roads, segments, and bridges in carrying goods traffic
- **vulnerability** — the susceptibility of those components to becoming problematic under disruption

This changes the role of experiments. The purpose is no longer only to compare scenario averages, but to interpret how traffic and failure interact in the network.

### Richer outputs in Stage 3
The Stage 3 batch runs export more than just travel-time summaries. They include dictionaries for:
- generated traffic,
- removed traffic,
- absolute and relative delay time,
- absolute and relative delay frequency,
- traffic over bridges,
- traffic over links.

The analysis notebook converts these stored dictionaries back into Python objects so they can be studied directly.

### Main analyses in Stage 3
1. **Scenario labeling and repeated-run organization**
   The notebook explicitly reconstructs scenario ids and scenario-run ids so each output row can be traced back to its experimental condition.

2. **Bridge traffic analysis**
   The number of trucks crossing each bridge is plotted and compared. This is important because high bridge traffic is a natural proxy for **criticality**.

3. **Worst bridge delay analysis**
   The notebook checks which bridges repeatedly produce the highest delay across runs and scenarios.

4. **Average driving time across scenarios**
   Plots compare how overall travel time responds to scenario severity.

5. **Criticality interpretation**
   Bridges or segments with consistently high throughput are interpreted as critical because much of the simulated flow depends on them.

6. **Vulnerability interpretation**
   Bridges with poor condition and strong delay impact are interpreted as vulnerable because they can produce large disruption effects if degraded.

### What Stage 3 results add
Stage 3 is where the project’s output becomes most policy-relevant:
- it links traffic importance to infrastructure condition,
- it moves from local bottlenecks to network significance,
- it uses the simulation as one way to reason about criticality and vulnerability.

---

## Criticality and vulnerability in the project’s results

Because Assignment 4 foregrounds these concepts, the documentation should explain how the project operationalizes them.

### Criticality
In the context of the repository, criticality is approximated through indicators such as:
- high truck throughput,
- high bridge traffic counts,
- strong effect on average driving time,
- repeated appearance in worst-case traffic or delay patterns.

A bridge or segment is critical if much of the modeled flow depends on it.

### Vulnerability
Vulnerability is approximated through indicators such as:
- poor bridge condition,
- high expected or realized delay,
- strong travel-time impact when disruption occurs,
- a structurally weak position in the network.

A bridge can be critical, vulnerable, or both:
- **critical but robust** if it carries much traffic but rarely creates delay,
- **vulnerable but not highly critical** if it fails easily but affects little flow,
- **critical and vulnerable** if it is both busy and disruptive when degraded.

---

## Visual outputs produced in the notebooks

The analysis notebooks generate several kinds of figures, including:
- line or bar plots of average driving time by scenario,
- per-scenario run comparisons,
- delay-time plots,
- bridge frequency plots for the most disruptive bridges,
- bridge traffic barplots,
- faceted plots comparing scenario behavior.

These visualizations matter because the assignments repeatedly emphasize not just running experiments, but communicating findings clearly.

---

## Cross-lab experiments-and-results storyline

The full results story of the repository can be summarized in three stages.

### Stage 1 — Corridor disruption experiments
Stage 1 asks whether changing bridge-failure probabilities changes corridor performance.

Main finding pattern:
- yes, worse disruption scenarios increase travel times and delays.

### Stage 2 — Network-aware delay analysis
Stage 2 asks similar questions, but on a richer network where structural position matters more.

Main finding pattern:
- some bridges repeatedly emerge as bottlenecks,
- network structure matters for interpreting which components are important.

### Stage 3 — Criticality and vulnerability interpretation
Stage 3 uses richer outputs to relate:
- traffic volume,
- bridge importance,
- disruption effects,
- and infrastructure quality.

Main finding pattern:
- the project moves from measuring delay to interpreting the strategic importance and vulnerability of network elements.

---

## Main findings the documentation should emphasize

Although the exact numeric values depend on scenario settings and stochastic runs, the documentation can safely emphasize several recurring findings from the notebooks and assignment framing.

### 1. Higher disruption probabilities increase travel time
Across scenario sweeps, more severe bridge-failure assumptions lead to worse travel-time performance.

### 2. Delays are not distributed evenly across bridges
A relatively small number of bridges repeatedly emerge as the “worst bridge” or as major sources of delay.

### 3. Repeated runs matter
Because bridge delays are stochastic, different runs under the same scenario can produce different results. That is why the analysis repeatedly uses 10-run scenario sets.

### 4. Structural position matters in the wider network
Once the model includes side roads and multiple routes, the importance of a bridge depends not just on its condition but also on where it sits in the network.

### 5. Traffic-based interpretation strengthens the analysis
When bridge/link traffic counts are added, the model can move from simple disruption reporting toward network criticality analysis.

---

## Limitations and next steps

The experiments are useful, but they remain stylized.

### Scenario assumptions are simplified
Bridge-condition probabilities are scenario inputs, not empirically calibrated collapse probabilities.

### Delay is easier to represent than full closure
The results mainly capture delay-based disruption rather than complete network failure or rerouting under hard closures.

### Traffic demand is modeled, not observed directly at truck level
Even when traffic data is used, source/sink demand remains a simulation abstraction rather than a direct replay of observed truck trajectories.

### Results are best read comparatively
The strongest conclusions are relative ones:
- which scenarios perform worse,
- which bridges matter more,
- which parts of the network seem more vulnerable.

The outputs are more robust as comparative scenario evidence than as exact forecasts.

---

## Summary

Experiments and results in this repository develop from simple corridor scenario tests into broader network-analysis findings.

- **Stage 1** establishes the first bridge-delay experiments and shows how scenario severity affects driving time.
- **Stage 2** extends those experiments to a connected network and reveals bridge importance in a broader structural setting.
- **Stage 3** adds traffic-weighted interpretation and frames the results in terms of **criticality** and **vulnerability**.

So the project’s experiments do not only measure delay. They increasingly explain **which parts of the network matter, why they matter, and how disruption affects them**.
