import pandas as pd
from scipy.spatial import distance
import math
import tensorflow as tf

# Load raw datafiles into DataFrames
roads = pd.read_csv("../data/raw/_roads3.csv")
bridges = pd.read_excel('../data/raw/BMMS_overview.xlsx', engine='openpyxl')

# --- Data processing input

# Specify main roads to find side roads to
mainroad = ['N1', 'N2']

# Specify road types to include
road_type = "N"

# Specify required length of the road to include it
length_required = 25

# --- Identifying side roads of N1 and N2

# Only keep the main roads we are interested in
df = roads.loc[(roads["road"].isin(mainroad))]

# List of all roads
Roads = roads['road'].unique().tolist()

# List of all crossroads and side roads (in ugly format)
names = df['name'].tolist()

# Find roads that appear in the crossroads / sideroads
side_roads = [road for road in Roads if any(road in name for name in names)]

# --- Filtering for road type and required length

# Take all side roads
sideroads_df = roads[roads['road'].isin(side_roads)]

# Filter for those over x km long (aka LRPE had chainage >x)
sideroads_ends = sideroads_df.loc[(sideroads_df["lrp"] == "LRPE") & (sideroads_df["chainage"] > length_required)]
sideroads_tokeep = sideroads_ends['road'].tolist()

# Apply filter
sideroads_df = sideroads_df.loc[(sideroads_df['road'].isin(sideroads_tokeep))]

# Filter for the right type of road
sideroads_tokeep = [s for s in sideroads_tokeep if road_type in s]

# Apply filter
sideroads_df = sideroads_df.loc[(sideroads_df['road'].isin(sideroads_tokeep))]

print("roads we consider in this assignment", sideroads_df['road'].unique())

# --- Adding a length to each road segment

# Create the length column
sideroads_df["length"] = sideroads_df["chainage"] * 1000
sideroads_df = sideroads_df.reset_index(drop=True)

# Change the chainage to a length
for i in range((len(sideroads_df) - 1), 0, -1):
    if sideroads_df["road"][i] == sideroads_df["road"][i - 1]:
        sideroads_df.loc[i, "length"] = sideroads_df.loc[i, "length"] - sideroads_df.loc[i - 1, "length"]
# sideroads_df.head()

# --- Moving on to bridges!

# Filter for relevant columns and relevant roads
bridges_relevant = bridges[
    ["road", "LRPName", "condition", "length", "chainage", "lat", "lon", 'name', 'km', 'constructionYear']]
bridges_relevant = bridges_relevant.loc[bridges['road'].isin(sideroads_tokeep)]
bridges_relevant = bridges_relevant.reset_index(drop=True)

bridgestemp = bridges_relevant  # useful in a second

# Only keep right side of each bridge
for i in range(1, len(bridges_relevant)):
    if len(str(bridges_relevant["name"][i])) > 4:
        if bridges_relevant["name"][i][-2:] == 'L)' or bridges_relevant["name"][i][-4:] == 'eft)' or \
                bridges_relevant["name"][i][-3:] == 'L )' or bridges_relevant["name"][i][-4:] == 'EFT)':
            bridgestemp = bridgestemp.drop(i, axis=0)

# Delete depulicates by removing older information
# assumption: no 2 lrps in the same road have the exact same km
bridges_relevant = bridgestemp \
    .sort_values(by=['road', 'km', 'constructionYear'], ascending=False) \
    .drop_duplicates(subset=['road', 'km'], keep='first')
# bridges_relevant.head()

# --- Bringing relevant roads and bridges together

# Prepare merge
bridges_relevant = bridges_relevant.rename(columns={"LRPName": "lrp"})

# Merge
merged = pd.merge(sideroads_df, bridges_relevant, how="outer", on=["road", "lrp"])
merged = merged.reset_index(drop=True)

# Add model_type
merged["model_type"] = merged["lrp"].apply(
    lambda x: "sourcesink" if x == "LRPS" else ("sourcesink" if x == "LRPE" else "link"))
merged.loc[merged["condition"].notnull(), "model_type"] = "bridge"

# Fill in missing data
merged["chainage_x"] = merged["chainage_x"].fillna(value=merged["chainage_y"])
merged["lat_x"] = merged["lat_x"].fillna(value=merged["lat_y"])
merged["lon_x"] = merged["lon_x"].fillna(value=merged["lon_y"])
merged["name_y"] = merged["name_y"].fillna(value=merged["name_x"])
merged["length_x"] = merged["length_x"].fillna(value=merged["length_y"])

# Keep and rename useful columns only
merged = merged.sort_values(by=['road', 'chainage_x'], ascending=True)
col_tokeep = ["road", "model_type", "lrp", "name_y", "lat_x", "lon_x", "length_x", "condition", "type", 'chainage_x']
merged = merged[col_tokeep]
merged = merged.rename(
    columns={"name_y": "name", 'chainage_x': 'chainage', "lat_x": "lat", "lon_x": "lon", "length_x": "length"})
merged = merged.reset_index(drop=True)

# Add ids
merged["id"] = range(1000000, len(merged) + 1000000)
cols = ["road", "model_type", "lrp", "name", "lat", "lon", "length", "condition", "type", "id", 'chainage']
merged = merged[cols]


def callgpu(merged):
    with tf.device('/GPU:0'):
        # warning: takes a very long time to run
        for i, row in merged.iterrows():
            for j in range(i, len(merged)):
                if merged['model_type'][j] != 'bridge':
                    if row['id'] != merged['id'][j] and merged['model_type'][j] != 'intersection' and row['road'] != \
                            merged['road'][j] and distance.euclidean((row['lat'], row['lon']),
                                                                     (merged['lat'][j], merged['lon'][j])) < 0.001:
                        merged.iloc[j, 9] = merged.iloc[i, 9]
                        merged.iloc[j, 4] = merged.iloc[i, 4]
                        merged.iloc[j, 5] = merged.iloc[i, 5]
                        merged.iloc[j, 1] = "intersection"
                        merged.iloc[i, 1] = "intersection"
                        print('new intersection made at ', row['id'], 'between', row['road'], 'and', merged['road'][j])
                        break

    return merged


merged = callgpu(merged)

# --- Adapting to the newest csv guidelines

# Adapting names
# move bridge names to a new column
merged["bridge_name"] = merged["name"].loc[merged['model_type'] == "bridge"]
# delete names for everything and replace that of SourceSinks according to convention
i = 1  # useful in a second
for index, row in merged.iterrows():
    if not row['model_type'] == "sourcesink":
        merged["name"][index] = ""

    elif row['model_type'] == "sourcesink":
        merged["name"][index] = "SoSi" + str(i)
        merged["condition"][index] = ""
        i += 1

# Put columns in right order
merged = merged[["road", "id", "model_type", "condition", "name", "lat", "lon", "length", "bridge_name", "chainage"]]

for i, row in merged.iterrows():
    if row['bridge_name'] == '.':
        merged.iloc[i, 8] = 'bridge at id ' + str(row['id'])


# Rename dataset to a more intuitive name
Roads_df = merged

# create two new columns, one for the ingoing traffic and one for the outgoing traffic

Roads_df['in'] = pd.Series()
Roads_df['out'] = pd.Series()

for index, row in Roads_df.iterrows():
    if row['model_type'] == "sourcesink":
        path = '../data/raw/traffic/'+row['road']+'.traffic.htm'
        trafficdata = pd.read_html(path)[2]
        trafficdata = trafficdata.iloc[4:-3, [0, 1, 4, 5, 25]]
        trafficdata.columns = trafficdata.iloc[0]
        trafficdata = trafficdata[2:]
        trafficdata["Start location"] = trafficdata["Start location"].astype(float)*1000
        trafficdata['Traffic'] = trafficdata['Traffic'].astype(float)
        closestrow = trafficdata.iloc[[0]]
        closestdistance = 1000
        # For some html files, it can occur that traffic is saved separately
        # for ingoing traffic and for outgoing traffic
        # If that is the case, we save those separately,
        # otherwise, we divide the traffic equally over the 'in' and 'out' columns
        closestrowright = trafficdata.iloc[[0]]
        twowaydata = False
        for i, r in trafficdata.iterrows():
            if abs(row['chainage']-r['Start location']) == closestdistance:
                closestrowright = r
                twowaydata = True
            elif abs(row['chainage']-r['Start location']) < closestdistance:
                closestrow = r
                closestdistance = abs(row['chainage']-r['Start location'])
        if twowaydata is True:
            Roads_df.iloc[index, 10] = closestrowright['Traffic']
            Roads_df.iloc[index, 11] = closestrow['Traffic']
        else:
            Roads_df.iloc[index, 10] = closestrow['Traffic']/2
            Roads_df.iloc[index, 11] = closestrow['Traffic']/2

# Save the traffic as a fraction/probability of trucks generation

total_in = Roads_df['in'].sum()
total_out = Roads_df['out'].sum()
for index, row in Roads_df.iterrows():
    if row['model_type'] == "sourcesink":
        Roads_df.iloc[index, 10] = row['in']/total_in
        Roads_df.iloc[index, 11] = row['out']/total_out


# Drop the chainage column

Roads_df = Roads_df[["road", "id", "model_type", "condition", "name",
                     "lat", "lon", "length", "bridge_name", "in", "out"]]

d = Roads_df.iloc[0, :]
Sparse_df = pd.DataFrame(data=d)
Sparse_df = Sparse_df.transpose()

# Merge al consecutive links together to one big link

chainage_build_up = 0
number_of_links = 0

for index, row in Roads_df.iterrows():
    if row["model_type"] == 'link':
        chainage_build_up += row['length']
        number_of_links += 1
    elif number_of_links > 0:
        if number_of_links == 1:
            Sparse_df = Sparse_df.append(Roads_df.iloc[index-1, :])
        else:
            Sparse_df = Sparse_df.append(Roads_df.iloc[index-math.floor(number_of_links/2)-1, :])
            Sparse_df.iloc[-1, 7] = chainage_build_up
        chainage_build_up = 0
        number_of_links = 0
        Sparse_df = Sparse_df.append(row)
    elif index > 0:
        Sparse_df = Sparse_df.append(row)

Sparse_df = Sparse_df.reset_index()
# Save to csv

Sparse_df.to_csv("../data/processed/N1_N2_plus_sideroads.csv", index=False)
