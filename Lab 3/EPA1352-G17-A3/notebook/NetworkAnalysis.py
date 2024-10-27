import networkx as nx
import pandas as pd
import tensorflow as tf
# import matplotlib.pyplot as plt

G = nx.Graph()

df = pd.read_csv("../data/processed/N1_N2_plus_sideroads.csv")

for i in range(len(df)):
    G.add_node(df['id'][i], road=df['road'][i], length=df['length'][i], pos=[df['lon'][i], df['lat'][i]])

intersections = df.loc[df['model_type'] == "intersection"]
intersections = intersections.reset_index()


previousnode = -1
for i, row in df.iterrows():
    if previousnode != -1:
        if row['road'] == df.iloc[previousnode, 0]:
            G.add_edge(df.iloc[previousnode, 1], row['id'], weight=row['length'])
    previousnode = i

pos = nx.get_node_attributes(G, 'pos')

shortestpath_dict = {}


def find_shortest_path(graph, a, b):
    if (a, b) in shortestpath_dict:
        p = shortestpath_dict[(a, b)]
    else:
        p = nx.shortest_path(graph, source=a, target=b, weight='weight')
        shortestpath_dict.update({(a, b): p})
    return p


sourcesinks = df.loc[df['model_type'] == "sourcesink"]
sourcesinks = sourcesinks.reset_index()

found = 0
not_found = 0
for i, row in sourcesinks.iterrows():
    for j in range(1, len(sourcesinks)):
        try:
            find_shortest_path(G, row['id'], sourcesinks.iloc[j, 2])
            # print("found path between",row['road'], "and", sourcesinks.iloc[j,1])
            found += 1
        except:
            print("could not find a path between", row['road'], "and", sourcesinks.iloc[j, 1])
            not_found += 1
print(not_found / found * 100, "percent of the paths could not be found")


def callfunc(G):
    with tf.device('/GPU:0'):
        closenessdict = nx.closeness_centrality(G)

        betweennessdict = nx.betweenness_centrality(G)

        degreecentralitydict = nx.degree_centrality(G)

    return [closenessdict, betweennessdict, degreecentralitydict]


closenessdict, betweennessdict, degreecentralitydict = callfunc(G)

bridges = df.loc[df['model_type'] == "bridge"]
bridgemetrics = bridges[['road', 'id', 'condition', 'bridge_name']]
bridgemetrics['betweenness_centrality'] = ''
bridgemetrics['closeness_centrality'] = ''
bridgemetrics['degreecentrality_centrality'] = ''

for i, row in bridgemetrics.iterrows():
    # points = callfunc(G)
    bridgemetrics['closeness_centrality'][i] = closenessdict[row['id']]
    bridgemetrics['betweenness_centrality'][i] = betweennessdict[row['id']]
    bridgemetrics['degreecentrality_centrality'][i] = degreecentralitydict[row['id']]


bridgemetrics.to_csv("../data/output/network_metrics.csv", index=None)

inters = intersections[['road', 'id', 'condition', 'bridge_name']]
inters['betweenness_centrality'] = ''
inters['closeness_centrality'] = ''
inters['degreecentrality_centrality'] = ''

for i, row in inters.iterrows():
    # points = callfunc(G)
    inters['closeness_centrality'][i] = closenessdict[row['id']]
    inters['betweenness_centrality'][i] = betweennessdict[row['id']]
    inters['degreecentrality_centrality'][i] = degreecentralitydict[row['id']]


inters.to_csv("../data/output/network_intersection_metrics.csv", index=None)
