from mesa import Model
from mesa.time import BaseScheduler
from mesa.space import ContinuousSpace
from components import Source, Sink, SourceSink, Bridge, Link, Intersection
import pandas as pd
from collections import defaultdict
import networkx as nx


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
    return max(times, key=times.get)


# ---------------------------------------------------------------
def compute_worst_bridge_delay(model):
    times = {agent.name: agent.total_delay_time / agent.trucks_passed if agent.trucks_passed > 0 else 0 for agent in
             model.schedule.agents if agent.__class__.__name__ == "Bridge"}
    name = max(times, key=times.get)
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

    file_name = '../data/processed/N1_N2_plus_sideroads.csv'

    def __init__(self, prob_A=0, prob_B=0, prob_C=0, prob_D=0, seed=None, x_max=500, y_max=500, x_min=0, y_min=0):

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

        self.generate_model()

    def generate_model(self):
        """
        generate the simulation model according to the csv file component information

        Warning: the labels are the same as the csv column labels
        """

        df = pd.read_csv(self.file_name)

        # construct network
        G = nx.Graph()

        for i, row in df.iterrows():
            G.add_node(row['id'], pos=[row['lon'], row['lat']])  # add all nodes from id

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

    def get_route(self, source):
        # set a source as destination, weighted by the amount of traffic that should go in
        destination = self.random.choices(list(self.sinks_in.keys()), weights=self.sinks_in.values(), k=1)[0]
        # loop untill destination is not the source
        while destination is source:
            destination = self.random.choices(list(self.sinks_in.keys()), weights=self.sinks_in.values(), k=1)[0]
        # check if path is already known
        if not self.path_ids_dict_complex[source, destination]:
            self.path_ids_dict_complex[source, destination] = nx.shortest_path(self.network, source=source,
                                                                               target=destination, weight='weight')
        # return the path
        return self.path_ids_dict_complex[source, destination]

    def step(self):
        """
        Advance the simulation by one step.
        """
        self.schedule.step()

# EOF -----------------------------------------------------------
