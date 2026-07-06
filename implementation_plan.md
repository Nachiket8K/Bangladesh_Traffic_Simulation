# Implementation Plan

[Overview]
Run the Lab 4 Bangladesh traffic model for a Chittagong-to-Dhaka truck flow and export real trajectory/network files for playback in `docs/visualization/index.html`.

The repo already contains a working network simulation in `Lab 4/EPA1352-G17-A4/model/` and a separate Leaflet viewer in `docs/visualization/`, but the viewer currently reads placeholder `network.geojson`, `bridges.geojson`, `scenarios.json`, and `traj_*.json` files. The implementation should connect these pieces by exporting real assets from the Lab 4 model into `docs/visualization/data/`.

The chosen approach is to extend the Lab 4 model because it already uses `N1_N2_plus_sideroads.csv`, weighted source/sink demand, bridge delay logic, and shortest-path routing. The implementation must add fixed Chittagong-origin / Dhaka-destination routing, per-truck position logging, GeoJSON export, scenario JSON export, and final browser verification.

[Types]
Add export schemas for network, bridge, scenario, and truck playback data.

- `VisualizationScenarioIndex`: `{ scenarios: list[VisualizationScenarioEntry] }`.
- `VisualizationScenarioEntry`: `label: str`, `file: str`.
- `VisualizationScenario`: `scenario_name: str`, `t0: number`, `t_end: number`, `broken_bridges: list[str|int]`, `trucks: list[TruckTrajectory]`.
- `TruckTrajectory`: `truck_id: str`, `timeline: list[TimelinePoint]`, optional `origin_id`, `destination_id`, `route_ids`.
- `TimelinePoint`: JSON tuple `[time, lat, lon]`.
- `NetworkFeature.properties`: `edge_id`, `from_id`, `to_id`, `road`, `is_bridge`, optional `bridge_id`, `bridge_name`, `condition`, `length`.
- `BridgeFeature.properties`: `bridge_id`, `bridge_name`, `condition`, `road`.
- Simulation structures: `truck_logs`, `truck_route_metadata`, `selected_origin_id`, `selected_destination_id`.

[Files]
Modify the Lab 4 simulation and docs visualization assets to support real export and playback.

- New files to be created:
  - `Bangladesh_Traffic_Simulation/Lab 4/EPA1352-G17-A4/model/export_visualization.py` - run scenarios and write `network.geojson`, `bridges.geojson`, `scenarios.json`, and `traj_*.json`.
  - `Bangladesh_Traffic_Simulation/Lab 4/EPA1352-G17-A4/model/route_selection.py` - optional Chittagong/Dhaka endpoint lookup helper.
  - `Bangladesh_Traffic_Simulation/Lab 4/EPA1352-G17-A4/model/trajectory_utils.py` - optional interpolation/export helpers.

- Existing files to be modified:
  - `Bangladesh_Traffic_Simulation/Lab 4/EPA1352-G17-A4/model/model.py` - add fixed origin/destination routing, coordinate lookup data, export metadata, and trajectory recording containers.
  - `Bangladesh_Traffic_Simulation/Lab 4/EPA1352-G17-A4/model/components.py` - record per-step positions and preserve completion/bridge-delay metadata.
  - `Bangladesh_Traffic_Simulation/Lab 4/EPA1352-G17-A4/model/model_run.py` - optionally point to the export workflow.
  - `Bangladesh_Traffic_Simulation/docs/visualization/app.js` - support generated scenario names, real bridge IDs, and any minor shape adjustments.
  - `Bangladesh_Traffic_Simulation/docs/visualization/data/network.geojson` - replace placeholder network.
  - `Bangladesh_Traffic_Simulation/docs/visualization/data/bridges.geojson` - replace placeholder bridge data.
  - `Bangladesh_Traffic_Simulation/docs/visualization/data/scenarios.json` - replace placeholder scenario index.
  - `Bangladesh_Traffic_Simulation/docs/visualization/data/traj_baseline.json` or new `traj_chittagong_dhaka_*.json` files - replace placeholder trajectories.
  - `Bangladesh_Traffic_Simulation/docs/visualization.md` and `Bangladesh_Traffic_Simulation/README.md` - document generation and viewing steps.

- Files to be deleted or moved: no required deletions; placeholder assets may be overwritten or renamed.

- Configuration updates: no new package manifest is required; output paths can live in the export script.

[Functions]
Add export, routing, interpolation, and trajectory-recording helpers that bridge the Python model and the Leaflet viewer.

- New functions:
  - `find_chittagong_dhaka_endpoints(df) -> tuple[int, int]` in `export_visualization.py` or `route_selection.py`.
  - `build_network_geojson(df) -> dict` in `export_visualization.py`.
  - `build_bridges_geojson(df) -> dict` in `export_visualization.py`.
  - `interpolate_vehicle_position(vehicle) -> tuple[float, float]` in `components.py` or `trajectory_utils.py`.
  - `record_vehicle_sample(model, vehicle) -> None` in `components.py` or `model.py`.
  - `export_scenario_json(model, scenario_name, output_path, broken_bridges) -> None` in `export_visualization.py`.
  - `write_scenario_index(entries, output_path) -> None` in `export_visualization.py`.
  - `run_visualization_export(...) -> list[dict]` in `export_visualization.py`.

- Modified functions:
  - `BangladeshModel.__init__` in `Lab 4/EPA1352-G17-A4/model/model.py` - accept `origin_id`, `destination_id`, `record_trajectories`, `scenario_name`, and sampling controls.
  - `BangladeshModel.generate_model` in `Lab 4/EPA1352-G17-A4/model/model.py` - retain row metadata and coordinate lookup by node ID.
  - `BangladeshModel.get_route` in `Lab 4/EPA1352-G17-A4/model/model.py` - support fixed Chittagong-to-Dhaka routing.
  - `Vehicle.set_path`, `Vehicle.step`, `Vehicle.arrive_at_next`, and `Vehicle.drive_to_next` in `Lab 4/EPA1352-G17-A4/model/components.py` - attach route metadata, record samples, and guarantee a final point before removal.
  - `loadScenario(file)` and `renderNetwork()` in `Bangladesh_Traffic_Simulation/docs/visualization/app.js` - tolerate generated file names and real bridge IDs.

- Removed functions: none.

[Classes]
Extend the existing Lab 4 model and vehicle classes instead of creating a separate simulation architecture.

- New classes: optional `VisualizationExporter` in `export_visualization.py` with methods such as `build_network_geojson()`, `build_bridges_geojson()`, `run_scenario()`, and `write_outputs()`.
- Modified classes:
  - `BangladeshModel` - store coordinate lookup data, support fixed endpoints, expose bridge/export metadata, and maintain trajectory containers.
  - `Vehicle` - record per-step positions, keep route metadata, and log the final destination position before removal.
  - `Source` / `SourceSink` - optionally constrain generation to the Chittagong endpoint and avoid cross-run counter leakage.
  - `Bridge` - expose stable bridge identifiers for export and scenario metadata.
- Removed classes: none.

[Dependencies]
Reuse the project's existing Python and browser dependencies, with compatibility validation rather than package expansion.

- Existing Python stack already covers the work: `mesa`, `pandas`, `networkx`, and standard library modules like `json`, `pathlib`, and `math`.
- Existing frontend dependency remains CDN-loaded Leaflet in `docs/visualization/index.html`.
- No new package should be added unless act-mode testing reveals a real need.
- Validate that the installed Mesa version still supports the legacy coursework imports.

[Testing]
Validate with script-level checks plus manual browser playback of the generated Chittagong-to-Dhaka scenario.

- Add runtime validation in the export script: exported network must have features, at least one truck trajectory must exist, timelines must be ordered, and `t_end` must match the last sample.
- Validation steps:
  1. Run the export script for a baseline scenario with no broken bridges.
  2. Confirm `docs/visualization/data/network.geojson` contains a real corridor network instead of the placeholder sample.
  3. Confirm `scenarios.json` references generated `traj_*.json` files.
  4. Open `docs/visualization/index.html` and verify trucks move along the Bangladesh network.
  5. If a bridge-down scenario is added, confirm listed bridges render red.
  6. Spot-check that the route visually trends from the Chittagong side toward Dhaka.

[Implementation Order]
Implement the exportable simulation path first, then generate visualization assets, then verify playback end to end.

1. Inspect the Lab 4 processed CSV and determine the exact source/sink IDs for the Chittagong-origin and Dhaka-destination flow.
2. Extend `BangladeshModel` to support fixed endpoint routing and optional trajectory recording containers.
3. Extend `Vehicle` movement logic to sample and retain per-step geographic positions, including final destination samples.
4. Build Python export helpers that transform processed network rows into `network.geojson` and `bridges.geojson`.
5. Implement a scenario runner/export script that executes the Chittagong-to-Dhaka simulation and writes `traj_*.json` plus `scenarios.json` into `docs/visualization/data/`.
6. Replace placeholder visualization data with generated outputs and update any file naming assumptions in `docs/visualization/app.js`.
7. Update repository documentation with exact commands for generating assets and opening the visualization.
8. Run the export workflow, inspect generated files, and verify the result in `docs/visualization/index.html`.