from mesa import Model
from mesa.time import BaseScheduler
from mesa.space import ContinuousSpace
from components import Source, Sink, SourceSink, Bridge, Link, Intersection
import pandas as pd
from collections import defaultdict
import networkx as nx
from pathlib import Path


# ---------------------------------------------------------------
def compute_traffic(model):
    generated = {source.unique_id: source.generated_traffic for source in model.schedule.agents
                 if source.__class__.__name__ == "SourceSink" or source.__class__.__name__ == "Source"}
    removed = {sink.unique_id: sink.removed_traffic for sink in model.schedule.agents
               if sink.__class__.__name__ == "SourceSink" or sink.__class__.__name__ == "Sink"}
    delay_time_abs = {source.unique_id: source.waiting_times for source in model.schedule.agents
                      if source.__class__.__name__ == "SourceSink" or source.__class__.__name__ == "Source"}
    delay_time_rel = {source.unique_id: source.waiting_times / source.generated_traffic
                      if source.generated_traffic > 0 else 0 for source in model.schedule.agents
                      if source.__class__.__name__ == "SourceSink" or source.__class__.__name__ == "Source"}
    delay_freq_abs = {source.unique_id: source.waiting_freqs for source in model.schedule.agents
                      if source.__class__.__name__ == "SourceSink" or source.__class__.__name__ == "Source"}
    delay_freq_rel = {source.unique_id: source.waiting_freqs / source.generated_traffic
                      if source.generated_traffic > 0 else 0 for source in model.schedule.agents
                      if source.__class__.__name__ == "SourceSink" or source.__class__.__name__ == "Source"}
    traffic_bridges = {bridge.unique_id: bridge.trucks_passed for bridge in model.schedule.agents
                       if bridge.__class__.__name__ == "Bridge"}
    traffic_links = {link.unique_id: link.trucks_passed for link in model.schedule.agents
                     if link.__class__.__name__ == "Link"}

    return generated, removed, delay_time_abs, delay_time_rel, delay_freq_abs, delay_freq_rel, \
        traffic_bridges, traffic_links


# ---------------------------------------------------------------
def compute_average_driving(model):
    return sum(model.drive_times) / len(model.drive_times) if len(model.drive_times) else 0


# ---------------------------------------------------------------
def compute_worst_bridge(model):
    times = {agent.name: agent.total_delay_time / agent.trucks_passed if agent.trucks_passed > 0 else 0 for agent in
             model.schedule.agents if agent.__class__.__name__ == "Bridge"}
    if not times:
        return None
    return max(times.items(), key=lambda item: item[1])[0]


# ---------------------------------------------------------------
def compute_worst_bridge_delay(model):
    times = {agent.name: agent.total_delay_time / agent.trucks_passed if agent.trucks_passed > 0 else 0 for agent in
             model.schedule.agents if agent.__class__.__name__ == "Bridge"}
    if not times:
        return 0
    name = max(times.items(), key=lambda item: item[1])[0]
    return times[name]


# ---------------------------------------------------------------
def get_probs(model):
    return model.probs


# ---------------------------------------------------------------
def set_lat_lon_bound(lat_min, lat_max, lon_min, lon_max, edge_ratio=0.02):
    """
    Set the HTML continuous space canvas bounding box (for visualization)
    give the min and max latitudes and Longitudes in Decimal Degrees (DD)

    Add white borders at edges (default 2%) of the bounding box
    """

    lat_edge = (lat_max - lat_min) * edge_ratio
    lon_edge = (lon_max - lon_min) * edge_ratio

    x_max = lon_max + lon_edge
    y_max = lat_min - lat_edge
    x_min = lon_min - lon_edge
    y_min = lat_max + lat_edge
    return y_min, y_max, x_min, x_max


# ---------------------------------------------------------------
class BangladeshModel(Model):
    """
    The main (top-level) simulation model

    One tick represents one minute; this can be changed
    but the distance calculation need to be adapted accordingly

    Class Attributes:
    -----------------
    step_time: int
        step_time = 1 # 1 step is 1 min

    path_ids_dict: defaultdict
        Key: (origin, destination)
        Value: the shortest path (Infra component IDs) from an origin to a destination

        Only straight paths in the Demo are added into the dict;
        when there is a more complex network layout, the paths need to be managed differently

    sources: list
        all sources in the network

    sinks: list
        all sinks in the network

    """

    step_time = 1

    file_name = Path(__file__).resolve().parents[1] / 'data' / 'processed' / 'N1_N2_plus_sideroads.csv'

    def __init__(
            self,
            prob_A=0,
            prob_B=0,
            prob_C=0,
            prob_D=0,
            seed=None,
            x_max=500,
            y_max=500,
            x_min=0,
            y_min=0,
            origin_id=None,
            destination_id=None,
            scenario_name="baseline",
            record_trajectories=False,
            sample_every_n_steps=1,
    ):

        self.seed = seed
        self.schedule = BaseScheduler(self)
        self.running = True
        self.path_ids_dict = defaultdict(lambda: pd.Series())
        self.path_ids_dict_complex = defaultdict(list)
        self.space = None
        self.sources = []
        self.sinks = []
        self.sinks_in = {}
        self.probs = {"A": prob_A, "B": prob_B, "C": prob_C, "D": prob_D}
        self.drive_times = []
        self.delay_at_bridge = []
        self.origin_id = origin_id
        self.destination_id = destination_id
        self.scenario_name = scenario_name
        self.record_trajectories = record_trajectories
        self.sample_every_n_steps = max(1, int(sample_every_n_steps))
        self.trajectory_logs = defaultdict(list)
        self.truck_route_metadata = {}
        self.node_positions = {}
        self.node_rows = {}
        self.bridge_ids = []
        self.fixed_route_mode = origin_id is not None and destination_id is not None
        self.active_source_ids = set()
        self.df = None

        self.generate_model()

    def generate_model(self):
        """
        generate the simulation model according to the csv file component information

        Warning: the labels are the same as the csv column labels
        """

        df = pd.read_csv(self.file_name)
        self.df = df.copy()
        self.node_rows = {
            int(row['id']): row.to_dict()
            for _, row in df.iterrows()
        }

        # construct network
        G = nx.Graph()

        for i, row in df.iterrows():
            G.add_node(row['id'], pos=[row['lon'], row['lat']])  # add all nodes from id
            self.node_positions[int(row['id'])] = (float(row['lat']), float(row['lon']))

        # add edges between all nodes on a road. Intersections have the same id, so will be connected this way too.
        p_row = None
        for i, row in df.iterrows():
            if p_row is not None:
                if p_row['road'] == row['road']:
                    G.add_edge(p_row['id'], row['id'], weight=row['length'])
            p_row = row

        self.network = G

        # a list of names of roads to be generated
        roads = df['road'].unique().tolist()

        df_objects_all = []

        for road in roads:
            # Select all the objects on a particular road in the original order as in the cvs
            df_objects_on_road = df[df['road'] == road]

            if not df_objects_on_road.empty:
                df_objects_all.append(df_objects_on_road)

                """
                Set the path 
                1. get the serie of object IDs on a given road in the cvs in the original order
                2. add the (straight) path to the path_ids_dict
                3. put the path in reversed order and reindex
                4. add the path to the path_ids_dict so that the vehicles can drive backwards too
                """
                path_ids = df_objects_on_road['id']
                path_ids.reset_index(inplace=True, drop=True)
                self.path_ids_dict[path_ids[0], path_ids.iloc[-1]] = path_ids
                self.path_ids_dict[path_ids[0], None] = path_ids
                path_ids = path_ids[::-1]
                path_ids.reset_index(inplace=True, drop=True)
                self.path_ids_dict[path_ids[0], path_ids.iloc[-1]] = path_ids
                self.path_ids_dict[path_ids[0], None] = path_ids

        # put back to df with selected roads so that min and max and be easily calculated
        df = pd.concat(df_objects_all)
        y_min, y_max, x_min, x_max = set_lat_lon_bound(
            df['lat'].min(),
            df['lat'].max(),
            df['lon'].min(),
            df['lon'].max(),
            0.05
        )

        # ContinuousSpace from the Mesa package;
        # not to be confused with the SimpleContinuousModule visualization
        self.space = ContinuousSpace(x_max, y_max, True, x_min, y_min)

        for df in df_objects_all:
            for _, row in df.iterrows():  # index, row in ...

                # create agents according to model_type
                model_type = row['model_type'].strip()
                agent = None

                name = row['name']
                if pd.isna(name):
                    name = ""
                else:
                    name = name.strip()

                if model_type == 'source':
                    agent = Source(row['id'], self, row['length'], name, row['road'], out=row['out'])
                    self.sources.append(agent.unique_id)
                elif model_type == 'sink':
                    agent = Sink(row['id'], self, row['length'], name, row['road'])
                    self.sinks.append(agent.unique_id)
                    self.sinks_in[agent.unique_id] = row['in']
                elif model_type == 'sourcesink':
                    agent = SourceSink(row['id'], self, row['length'], name, row['road'], out=row['out'])
                    self.sources.append(agent.unique_id)
                    self.sinks.append(agent.unique_id)
                    self.sinks_in[agent.unique_id] = row['in']
                elif model_type == 'bridge':
                    agent = Bridge(row['id'], self, row['length'], row['bridge_name'], row['road'], row['condition'])
                    self.bridge_ids.append(agent.unique_id)
                elif model_type == 'link':
                    agent = Link(row['id'], self, row['length'], name, row['road'])
                elif model_type == 'intersection':
                    if not row['id'] in self.schedule._agents:
                        agent = Intersection(row['id'], self, row['length'], name, row['road'])

                if agent:
                    self.schedule.add(agent)
                    y = row['lat']
                    x = row['lon']
                    self.space.place_agent(agent, (x, y))
                    agent.pos = (x, y)

        self.active_source_ids = {self.origin_id} if self.fixed_route_mode else set(self.sources)

    def get_route(self, source):
        if self.fixed_route_mode:
            destination = self.destination_id
            if destination == source:
                raise ValueError("Origin and destination must be different in fixed route mode")
        else:
            # set a source as destination, weighted by the amount of traffic that should go in
            sink_ids = list(self.sinks_in.keys())
            sink_weights = list(self.sinks_in.values())
            destination = self.random.choices(sink_ids, weights=sink_weights, k=1)[0]
            # loop untill destination is not the source
            while destination is source:
                destination = self.random.choices(sink_ids, weights=sink_weights, k=1)[0]
        # check if path is already known
        if not self.path_ids_dict_complex[source, destination]:
            self.path_ids_dict_complex[source, destination] = nx.shortest_path(self.network, source=source,
                                                                               target=destination, weight='weight')
        # return the path
        return self.path_ids_dict_complex[source, destination]

    def is_source_active(self, source_id):
        return source_id in self.active_source_ids

    def get_node_position(self, node_id):
        return self.node_positions.get(int(node_id))

    def get_bridge_ids(self):
        broken = []
        for bridge_id in self.bridge_ids:
            bridge = self.schedule._agents.get(bridge_id)
            if bridge is not None and getattr(bridge, 'delay', False):
                broken.append(bridge_id)
        return broken

    def interpolate_vehicle_position(self, vehicle):
        current = self.get_node_position(vehicle.location.unique_id)
        if current is None:
            return None

        current_lat, current_lon = current
        if vehicle.location_index >= len(vehicle.path_ids) - 1:
            return current_lat, current_lon

        if getattr(vehicle.location, 'length', 0) <= 0:
            return current_lat, current_lon

        next_id = vehicle.path_ids[min(vehicle.location_index + 1, len(vehicle.path_ids) - 1)]
        next_pos = self.get_node_position(next_id)
        if next_pos is None:
            return current_lat, current_lon

        next_lat, next_lon = next_pos
        ratio = max(0.0, min(1.0, float(vehicle.location_offset) / float(vehicle.location.length or 1)))
        lat = current_lat + (next_lat - current_lat) * ratio
        lon = current_lon + (next_lon - current_lon) * ratio
        return lat, lon

    def record_vehicle_sample(self, vehicle, force=False):
        if not self.record_trajectories:
            return
        if not force and (self.schedule.steps % self.sample_every_n_steps != 0):
            return

        pos = self.interpolate_vehicle_position(vehicle)
        if pos is None:
            return

        lat, lon = pos
        time_value = float(self.schedule.steps)
        sample = [time_value, float(lat), float(lon)]
        timeline = self.trajectory_logs[vehicle.unique_id]
        if not timeline or timeline[-1] != sample:
            timeline.append(sample)

    def register_vehicle(self, vehicle):
        meta = self.truck_route_metadata.setdefault(vehicle.unique_id, {})
        meta.setdefault('origin_id', vehicle.generated_by.unique_id)
        meta.setdefault('destination_id', None)
        meta.setdefault('route_ids', [])
        self.record_vehicle_sample(vehicle, force=True)

    def finalize_vehicle(self, vehicle):
        meta = self.truck_route_metadata.setdefault(vehicle.unique_id, {})
        meta['origin_id'] = vehicle.generated_by.unique_id
        meta['destination_id'] = vehicle.location.unique_id
        meta['route_ids'] = [int(route_id) for route_id in vehicle.path_ids]
        self.record_vehicle_sample(vehicle, force=True)

    def step(self):
        """
        Advance the simulation by one step.
        """
        self.schedule.step()

# EOF -----------------------------------------------------------
