import json
from pathlib import Path

import networkx as nx
import pandas as pd


ROOT = Path(__file__).resolve().parents[3]
DATA_DIR = ROOT / "docs" / "visualization" / "data"
PROCESSED_CSV = Path(__file__).resolve().parents[1] / "data" / "processed" / "N1_N2_plus_sideroads.csv"
CHITTAGONG_PORT = (22.2960, 91.7900)
DHAKA_HUB = (23.7060, 90.4433)
LAB_SCENARIO_PROBABILITIES = [
    {"prob_A": 0.0, "prob_B": 0.0, "prob_C": 0.0, "prob_D": 0.0},
    {"prob_A": 0.0, "prob_B": 0.0, "prob_C": 0.0, "prob_D": 0.05},
    {"prob_A": 0.0, "prob_B": 0.0, "prob_C": 0.05, "prob_D": 0.10},
    {"prob_A": 0.0, "prob_B": 0.05, "prob_C": 0.10, "prob_D": 0.20},
    {"prob_A": 0.05, "prob_B": 0.10, "prob_C": 0.20, "prob_D": 0.40},
    {"prob_A": 0.25, "prob_B": 0.50, "prob_C": 0.75, "prob_D": 1.00},
]


def _distance_sq(lat, lon, target_lat, target_lon):
    return (float(lat) - float(target_lat)) ** 2 + (float(lon) - float(target_lon)) ** 2


def find_chittagong_dhaka_endpoints(df):
    n1_rows = df[df["road"] == "N1"].copy()
    if n1_rows.empty:
        raise ValueError("Expected N1 rows in processed network data")

    chittagong = min(
        n1_rows.to_dict("records"),
        key=lambda row: _distance_sq(row["lat"], row["lon"], CHITTAGONG_PORT[0], CHITTAGONG_PORT[1]),
    )
    dhaka = min(
        n1_rows.to_dict("records"),
        key=lambda row: _distance_sq(row["lat"], row["lon"], DHAKA_HUB[0], DHAKA_HUB[1]),
    )
    return int(chittagong["id"]), int(dhaka["id"])


def build_network_graph(df):
    graph = nx.Graph()
    for _, row in df.iterrows():
        graph.add_node(int(row["id"]), lat=float(row["lat"]), lon=float(row["lon"]))

    previous = None
    for _, row in df.iterrows():
        current = int(row["id"])
        if previous is not None and previous["road"] == row["road"]:
            graph.add_edge(int(previous["id"]), current, weight=float(row["length"]), road=row["road"])
        previous = row
    return graph


def build_node_lookup(df):
    return {int(row["id"]): row for _, row in df.iterrows()}


def bridge_delay_for_condition(condition):
    return {
        "A": 0,
        "B": 2,
        "C": 6,
        "D": 12,
    }.get(str(condition).strip(), 0)


def condition_probability_key(condition):
    return f"prob_{str(condition).strip()}"


def select_broken_bridges_for_probs(route_ids, node_lookup, scenario_probs):
    bridges_by_condition = {}

    for node_id in route_ids:
        row = node_lookup[int(node_id)]
        if str(row.get("model_type", "")).strip() != "bridge":
            continue
        condition = str(row.get("condition", "")).strip()
        bridges_by_condition.setdefault(condition, []).append(row)

    broken_bridge_ids = []
    for condition, rows in bridges_by_condition.items():
        probability = float(scenario_probs.get(condition_probability_key(condition), 0.0) or 0.0)
        if probability <= 0 or not rows:
            continue

        rows = sorted(rows, key=lambda row: (float(row.get("chainage", 0) or 0), int(row["id"])))
        selected_count = max(1, round(len(rows) * probability))
        selected_count = min(len(rows), selected_count)
        broken_bridge_ids.extend(int(row["id"]) for row in rows[:selected_count])

    return sorted(set(broken_bridge_ids))


def format_probability_label(scenario_probs):
    return ", ".join(
        f"{key.split('_')[1]}={float(value):.2f}"
        for key, value in scenario_probs.items()
    )


def build_truck_timeline(route_ids, node_lookup, broken_bridge_ids=None, start_offset=0.0, speed_m_per_min=800.0):
    broken_bridge_ids = set(broken_bridge_ids or [])
    timeline = []
    current_time = float(start_offset)

    for idx, node_id in enumerate(route_ids):
        row = node_lookup[int(node_id)]
        timeline.append([round(current_time, 3), float(row["lat"]), float(row["lon"])] )

        if idx == len(route_ids) - 1:
            continue

        next_row = node_lookup[int(route_ids[idx + 1])]
        travel_minutes = max(float(next_row["length"]) / speed_m_per_min, 1.0)
        current_time += travel_minutes

        if int(node_id) in broken_bridge_ids:
            current_time += bridge_delay_for_condition(row.get("condition", ""))

    return timeline


def build_scenario_payload(
    df,
    scenario_name,
    route_ids,
    broken_bridge_ids=None,
    truck_count=4,
    launch_gap=18.0,
    scenario_probs=None,
):
    node_lookup = build_node_lookup(df)
    trucks = []
    t_end = 0.0

    for index in range(truck_count):
        timeline = build_truck_timeline(
            route_ids,
            node_lookup,
            broken_bridge_ids=broken_bridge_ids,
            start_offset=index * launch_gap,
        )
        t_end = max(t_end, timeline[-1][0])
        trucks.append(
            {
                "truck_id": f"Truck{index + 1}",
                "timeline": timeline,
                "origin_id": int(route_ids[0]),
                "destination_id": int(route_ids[-1]),
                "route_ids": [int(route_id) for route_id in route_ids],
            }
        )

    return {
        "scenario_name": scenario_name,
        "t0": 0,
        "t_end": t_end,
        "broken_bridges": [int(bridge_id) for bridge_id in (broken_bridge_ids or [])],
        "scenario_probs": scenario_probs or {},
        "trucks": trucks,
    }


def build_network_geojson(df):
    features = []
    edge_counter = 1

    for road, road_df in df.groupby("road", sort=False):
        road_df = road_df.reset_index(drop=True)
        for i in range(len(road_df) - 1):
            current = road_df.iloc[i]
            nxt = road_df.iloc[i + 1]
            if current["road"] != nxt["road"]:
                continue

            bridge_row = current if str(current["model_type"]).strip() == "bridge" else None

            properties = {
                "edge_id": f"E{edge_counter}",
                "from_id": int(current["id"]),
                "to_id": int(nxt["id"]),
                "road": str(road),
                "is_bridge": bridge_row is not None,
                "length": float(nxt["length"]),
            }

            if bridge_row is not None:
                properties.update({
                    "bridge_id": int(bridge_row["id"]),
                    "bridge_name": str(bridge_row.get("bridge_name") or ""),
                    "condition": str(bridge_row.get("condition") or ""),
                })

            features.append({
                "type": "Feature",
                "properties": properties,
                "geometry": {
                    "type": "LineString",
                    "coordinates": [
                        [float(current["lon"]), float(current["lat"])],
                        [float(nxt["lon"]), float(nxt["lat"])],
                    ],
                },
            })
            edge_counter += 1

    return {"type": "FeatureCollection", "features": features}


def build_bridges_geojson(df):
    bridges = df[df["model_type"].astype(str).str.strip() == "bridge"]
    features = []
    for _, row in bridges.iterrows():
        features.append({
            "type": "Feature",
            "properties": {
                "bridge_id": int(row["id"]),
                "bridge_name": str(row.get("bridge_name") or ""),
                "condition": str(row.get("condition") or ""),
                "road": str(row.get("road") or ""),
            },
            "geometry": {
                "type": "Point",
                "coordinates": [float(row["lon"]), float(row["lat"])],
            },
        })
    return {"type": "FeatureCollection", "features": features}


def export_scenario_json(payload, output_path):
    output_path.write_text(json.dumps(payload, indent=2), encoding="utf-8")
    return payload


def write_scenario_index(entries, output_path):
    output_path.write_text(json.dumps({"scenarios": entries}, indent=2), encoding="utf-8")


def validate_payload(payload, network_geojson):
    if not network_geojson.get("features"):
        raise ValueError("Exported network.geojson contains no features")
    if not payload.get("trucks"):
        raise ValueError("No truck trajectories were exported")
    for truck in payload["trucks"]:
        timeline = truck.get("timeline", [])
        if timeline != sorted(timeline, key=lambda item: item[0]):
            raise ValueError(f"Timeline for truck {truck['truck_id']} is not ordered")


def run_visualization_export():
    DATA_DIR.mkdir(parents=True, exist_ok=True)
    df = pd.read_csv(PROCESSED_CSV)
    origin_id, destination_id = find_chittagong_dhaka_endpoints(df)
    graph = build_network_graph(df)
    route_ids = nx.shortest_path(graph, source=origin_id, target=destination_id, weight="weight")
    node_lookup = build_node_lookup(df)

    network_geojson = build_network_geojson(df)
    bridges_geojson = build_bridges_geojson(df)
    (DATA_DIR / "network.geojson").write_text(json.dumps(network_geojson, indent=2), encoding="utf-8")
    (DATA_DIR / "bridges.geojson").write_text(json.dumps(bridges_geojson, indent=2), encoding="utf-8")

    scenario_entries = []
    scenario_specs = [
        {
            "label": "Chittagong Port to Dhaka (baseline)",
            "filename": "traj_chittagong_dhaka_baseline.json",
            "scenario_probs": LAB_SCENARIO_PROBABILITIES[0],
        }
    ]

    for index, scenario_probs in enumerate(LAB_SCENARIO_PROBABILITIES[1:], start=1):
        label = f"Chittagong Port to Dhaka (Lab scenario {index}: {format_probability_label(scenario_probs)})"
        scenario_specs.append(
            {
                "label": label,
                "filename": f"traj_chittagong_dhaka_lab_scenario_{index}.json",
                "scenario_probs": scenario_probs,
            }
        )

    for spec in scenario_specs:
        broken_bridge_ids = select_broken_bridges_for_probs(route_ids, node_lookup, spec["scenario_probs"])
        payload = build_scenario_payload(
            df,
            spec["label"],
            route_ids,
            broken_bridge_ids=broken_bridge_ids,
            scenario_probs=spec["scenario_probs"],
        )
        payload = export_scenario_json(payload, DATA_DIR / spec["filename"])
        validate_payload(payload, network_geojson)
        scenario_entries.append({"label": spec["label"], "file": spec["filename"]})

    write_scenario_index(scenario_entries, DATA_DIR / "scenarios.json")
    # Keep the historical placeholder name pointed at the real baseline scenario for compatibility.
    (DATA_DIR / "traj_baseline.json").write_text(
        (DATA_DIR / "traj_chittagong_dhaka_baseline.json").read_text(encoding="utf-8"),
        encoding="utf-8",
    )
    return scenario_entries


if __name__ == "__main__":
    run_visualization_export()