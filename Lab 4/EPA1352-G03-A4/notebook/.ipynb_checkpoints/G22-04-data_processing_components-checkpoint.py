import pandas as pd
from scipy.spatial import distance
import os
import math


def get_bridge_road_data(roads, bridges, mainroad, road_type, length_required):
    """collects all the relevant road and bridge data and merges them together

    Args:
        roads (DataFrame): roads data as structured in the _roads3.csv format
        bridges (DataFrame): bridge data as structured in the BMMS_overview.xlsx format
        mainroad (list): all the main roads to find sideroads on
        road_type (st): the types of roads to include
        length_required (int): the required length of sideroads to keep

    Returns:
        DataFrame: all the relevant roads and bridges
    """
    df = roads.loc[(roads["road"].isin(mainroad))
                   ]  # Only keep the main roads we are interested in
    Roads = roads['road'].unique().tolist()  # List of all roads
    # List of all crossroads and side roads (in ugly format)
    names = df['name'].tolist()

    # Find roads that appear in the crossroads / sideroads
    side_roads = [road for road in Roads if any(
        road in name for name in names)]

    # Take all side roads and filter for those over x km long (aka LRPE had chainage >x)
    sideroads_df = roads[roads['road'].isin(side_roads)]
    sideroads_tokeep = sideroads_df.loc[(sideroads_df["lrp"] == "LRPE") & (
        sideroads_df["chainage"] > length_required)]['road'].tolist()

    # Filter for the right type of road
    sideroads_tokeep = [s for s in sideroads_tokeep if road_type in s]
    sideroads_df = sideroads_df.loc[(
        sideroads_df['road'].isin(sideroads_tokeep))]  # Apply filter

    # --- Adding a length to each road segment

    # Create the length column
    sideroads_df["length"] = sideroads_df["chainage"]*1000
    sideroads_df = sideroads_df.reset_index(drop=True)

    # Change the chainage to a length
    for i in range((len(sideroads_df)-1), 0, -1):
        if sideroads_df["road"][i] == sideroads_df["road"][i-1]:
            sideroads_df.loc[i, "length"] = sideroads_df.loc[i,
                                                             "length"]-sideroads_df.loc[i-1, "length"]

    # Filter for relevant columns and relevant roads
    bridges_relevant = bridges[["road", "LRPName", "condition", "length",
                                "chainage", "lat", "lon", 'name', 'km', 'constructionYear']]
    bridges_relevant = bridges_relevant.loc[bridges['road'].isin(
        sideroads_tokeep)]
    bridges_relevant = bridges_relevant.reset_index(drop=True)

    bridgestemp = bridges_relevant  # useful in a second

    # Only keep right side of each bridge
    for i in range(1, len(bridges_relevant)):
        if len(str(bridges_relevant["name"][i])) > 4:
            if bridges_relevant["name"][i][-2:] == 'L)' or bridges_relevant["name"][i][-4:] == 'eft)' or bridges_relevant["name"][i][-3:] == 'L )' or bridges_relevant["name"][i][-4:] == 'EFT)':
                bridgestemp = bridgestemp.drop(i, axis=0)

    # Delete depulicates by removing older information
    # assumption: no 2 lrps in the same road have the exact same km
    bridges_relevant = bridgestemp \
        .sort_values(by=['road', 'km', 'constructionYear'], ascending=False) \
        .drop_duplicates(subset=['road', 'km'], keep='first')
    bridges_relevant.head()

    # --- Bringing relevant roads and bridges together

    # Prepare merge
    bridges_relevant = bridges_relevant.rename(columns={"LRPName": "lrp"})

    # Merge
    merged = pd.merge(sideroads_df, bridges_relevant,
                      how="outer", on=["road", "lrp"])
    merged = merged.reset_index(drop=True)

    # Add model_type
    merged["model_type"] = merged["lrp"].apply(
        lambda x: "sourcesink" if x == "LRPS" else ("sourcesink" if x == "LRPE" else "link"))
    merged.loc[merged["condition"].notnull(), "model_type"] = "bridge"

    # Fill in missing data
    merged["chainage_x"] = merged["chainage_x"].fillna(
        value=merged["chainage_y"])
    merged["lat_x"] = merged["lat_x"].fillna(value=merged["lat_y"])
    merged["lon_x"] = merged["lon_x"].fillna(value=merged["lon_y"])
    merged["name_y"] = merged["name_y"].fillna(value=merged["name_x"])
    merged["length_x"] = merged["length_x"].fillna(value=merged["length_y"])

    # Keep and rename useful columns only
    merged = merged.sort_values(by=['road', 'chainage_x'], ascending=True)
    col_tokeep = ["road", "model_type", "lrp", "name_y", "lat_x",
                  "lon_x", "length_x", "condition", "type", 'chainage_x']
    merged = merged[col_tokeep]
    merged = merged.rename(columns={"name_y": "name", 'chainage_x': 'chainage',
                           "lat_x": "lat", "lon_x": "lon", "length_x": "length"})
    merged = merged.reset_index(drop=True)

    # Add ids
    merged["id"] = range(1000000, len(merged) + 1000000)
    return merged[["road", "model_type", "lrp", "name", "lat", "lon", "length", "condition", "type", "id", 'chainage']]


def add_intersections(merged):
    """adds the intersections at the needed places

    Args:
        merged (DataFrame): DataFrame with the following columns: ["road", "model_type", "lrp", "name", "lat", "lon", "length", "condition","type","id", 'chainage']

    Returns:
        DataFrame: DataFrame that can be used in the Mesa model, uses the following columns: ["road", "id", "model_type", "condition", "name", "lat", "lon", "length", "bridge_name","chainage"]
    """
    # --- Defining the intersections

    # subset the dataframe to only the rows that indicate an intersection
    cross_sideroads = merged.loc[(merged['type'].str.contains(
        "CrossRoad")) | (merged['type'].str.contains("SideRoad"))]
    cross_sideroads = cross_sideroads.reset_index()

    roads_done = []
    # iterate over all road rows that are crossroads or sideroads
    for i, crossrow in cross_sideroads.iterrows():
        # check if any of those roads indicate in their name that they intersect with a road that crosses the N1 and/or N2
        for j in merged.road.unique():
            if j in str(crossrow["name"]) and j != crossrow["road"]:
                # if you are not trying one intersection that you already did the other way around
                if i not in roads_done:
                    # iterate over all points in that intersecting road to see if any of those indicate to be an intersection with the road at hand
                    # since a road can cross another road on multiple occasions, we only look as far as 1 lat and 1 lon
                    for k, roadrow in merged[merged['road'] == j].iterrows():
                        if crossrow["name"] in roadrow["name"] and (roadrow["lat"] - crossrow["lat"] < 1) and (roadrow["lon"] - crossrow["lon"] < 1) and crossrow["road"] != roadrow["road"]:
                            # if this finds the intersection point, make its id, lat and lon the same and make the model_type "intersection"
                            merged.iloc[k, 4] = cross_sideroads.iloc[i, 5]
                            merged.iloc[k, 5] = cross_sideroads.iloc[i, 6]
                            for l, newestrow in merged.loc[merged["id"] == roadrow["id"]].iterrows():
                                merged.iloc[l, 9] = cross_sideroads.iloc[i, 10]
                                merged.iloc[l, 1] = "intersection"
                            merged.iloc[cross_sideroads.iloc[i, 0],
                                        1] = "intersection"
                            #print("made indersection here1:",merged.iloc[k,:],merged.iloc[cross_sideroads.iloc[i,0],1])
                            # save the fact that you have handled this intersection
                            roads_done.append(i)
                            break
                    # if you didnt find the intersecting road through the name, assign the closest road point as the intersection
                    # assumption: projection is so small that it will not distort the distance to much so we can use euclidean distance to determine the closest point
                    else:
                        closestrow = merged.iloc[[0]]
                        closestindex = 0
                        closestdistance = 1000
                        p1 = (crossrow["lat"], crossrow["lon"])
                        # calculate for each road point the distance to the intersection, save it if it is closer than what you found before
                        for k, roadrow in merged[merged['road'] == j].iterrows():
                            p2 = (roadrow["lat"], roadrow["lon"])
                            if distance.euclidean(p1, p2) < closestdistance:
                                closestrow = roadrow
                                closestindex = k
                                closestdistance = distance.euclidean(p1, p2)
                        # of the closest point, make the id, lat and lon the same and make the model_type "intersection"
                        merged.iloc[closestindex,
                                    9] = cross_sideroads.iloc[i, 10]
                        merged.iloc[closestindex,
                                    4] = cross_sideroads.iloc[i, 5]
                        merged.iloc[closestindex,
                                    5] = cross_sideroads.iloc[i, 6]
                        merged.iloc[closestindex, 1] = "intersection"
                        merged.iloc[cross_sideroads.iloc[i, 0],
                                    1] = "intersection"
                        #print("made indersection here2:",merged.iloc[k,:],"other roadpoint:",merged.iloc[cross_sideroads.iloc[i,0],:])
                        # save the fact that you have handled this intersection
                        roads_done.append(i)
    # as the above code does not find all intersections, here is a more crude way to find them anyhow based on the closeness of the points in different roads
    for i, row in merged.iterrows():
        for j in range(i, len(merged)):
            if merged['model_type'][j] != 'bridge':
                if row['id'] != merged['id'][j] and merged['model_type'][j] != 'intersection' and row['road'] != merged['road'][j] and distance.euclidean((row['lat'], row['lon']), (merged['lat'][j], merged['lon'][j])) < 0.001:
                    merged.iloc[j, 9] = merged.iloc[i, 9]
                    merged.iloc[j, 4] = merged.iloc[i, 4]
                    merged.iloc[j, 5] = merged.iloc[i, 5]
                    merged.iloc[j, 1] = "intersection"
                    merged.iloc[i, 1] = "intersection"
                    break

    # --- Adapting to the newest csv guidelines

    # Adapting names
    # move bridge names to a new column
    merged["bridge_name"] = merged["name"].loc[merged['model_type'] == "bridge"]
    # delete names for everything and replace that of SourceSinks according to convention
    i = 1  # useful in a second
    for index, row in merged.iterrows():
        if not row['model_type'] == "sourcesink":
            merged.loc[index, "name"] = ""

        elif row['model_type'] == "sourcesink":
            merged.loc[index, "name"] = "SoSi" + str(i)
            merged.loc[index, "condition"] = ""
            i += 1

    # fill missing bridge names
    for i, row in merged.iterrows():
        if row['bridge_name'] == '.':
            merged.loc[i, 'bridge_name'] = 'bridge at id ' + str(row['id'])

    # Put columns in right order
    return merged[["road", "id", "model_type", "condition", "name", "lat", "lon", "length", "bridge_name", "chainage"]]


def add_traffic(Roads_df, location_traffic):
    """adds traffic data from the traffic html files

    Args:
        Roads_df (DataFrame): road and bridge data with the following columns: ["road", "id", "model_type", "condition", "name", "lat", "lon", "length", "bridge_name","chainage"]
        location_traffic (str): path to traffic html files

    Returns:
        DataFrame: DataFrame: DataFrame that can be used in the Mesa model, uses the following columns: ["road", "id", "model_type", "condition", "name", "lat", "lon", "length", "bridge_name","in", "out"]
    """
    # create two new columns, one for the ingoing traffic and one for the outgoing traffic
    Roads_df['in'] = pd.Series()
    Roads_df['out'] = pd.Series()

    # For each sourcesink, find the closest point in the traffic data by comparing chainages.
    for index, row in Roads_df.iterrows():
        if row['model_type'] == "sourcesink":
            path = location_traffic + row['road']+'.traffic.htm'
            trafficdata = pd.read_html(path)[2]
            trafficdata = trafficdata.iloc[4:-3, [0, 1, 4, 5, 25]]
            trafficdata.columns = trafficdata.iloc[0]
            trafficdata = trafficdata[2:]
            trafficdata["Start location"] = trafficdata["Start location"].astype(
                float)*1000
            trafficdata['Traffic'] = trafficdata['Traffic'].astype(float)
            closestrow = trafficdata.iloc[[0]]
            closestdistance = 1000
            # For some html files, it can occur that traffic is saved separately for ingoing traffic and for outgoing traffic
            # If that is the case, we save those separately, otherwise, we divide the traffic equally over the 'in' and 'out' columns
            closestrowright = trafficdata.iloc[[0]]
            twowaydata = False
            for i, r in trafficdata.iterrows():
                if abs(row['chainage']-r['Start location']) == closestdistance:
                    closestrowright = r
                    twowaydata = True
                elif abs(row['chainage']-r['Start location']) < closestdistance:
                    closestrow = r
                    closestdistance = abs(row['chainage']-r['Start location'])
            if twowaydata == True:
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

    # Keep the right columns in the right order
    Roads_df = Roads_df[["road", "id", "model_type", "condition",
                         "name", "lat", "lon", "length", "bridge_name", "in", "out"]]

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
                Sparse_df = Sparse_df.append(
                    Roads_df.iloc[index-math.floor(number_of_links/2)-1, :])
                Sparse_df.iloc[-1, 7] = chainage_build_up
            chainage_build_up = 0
            number_of_links = 0
            Sparse_df = Sparse_df.append(row)
        elif index > 0:
            Sparse_df = Sparse_df.append(row)

    return Sparse_df.reset_index()
