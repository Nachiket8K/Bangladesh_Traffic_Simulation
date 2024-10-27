import pandas as pd

# load raw datafiles into DataFrames
roads = pd.read_csv("../data/raw/_roads3.csv")
bridges = pd.read_excel('../data/raw/BMMS_overview.xlsx')

# remove unneeded data
roads = roads[["road", "chainage", "lrp", "lat", "lon"]]
roads = roads.loc[(roads["road"] == "N1") & (roads["chainage"] < 241.2)]

# convert chainage length to meters (1 chain = 60 feet = 20.11680 meters)
roads["chainage"] = roads["chainage"].astype(float)
roads["length"] = roads["chainage"]*1000 # 20.11680

# calculate length of segment in stead of cumulative length of the road
for i in range((len(roads["length"])-1),0,-1):
    roads.loc[i,"length"] = roads.loc[i,"length"]-roads.loc[i-1,"length"]

bridges = bridges[["road", "LRPName", "condition", "length", "chainage", "lat", "lon", 'name', 'km','constructionYear']]

# the N1 between Dhaka and Chittagong are the first 164 entries
BridgesN1 = bridges.loc[(bridges["road"] == "N1") & (bridges["chainage"] < 241)]
BridgesN1 = BridgesN1.reset_index()

bridgestemp = BridgesN1

# drop all left side bridges, we checked that there is no condition data lost
for i in range(1,len(BridgesN1["road"])):
    if len(BridgesN1["name"][i]) > 4:
        if BridgesN1["name"][i][-2:] == 'L)' or BridgesN1["name"][i][-4:] == 'eft)' or BridgesN1["name"][i][-3:] == 'L )' or BridgesN1["name"][i][-4:] == 'EFT)':
            bridgestemp = bridgestemp.drop(i,axis = 0)

# for all remaining duplicates: drop the least recent one or the one with the missing value
# assumption: no 2 lrps in the same road have the exact same km
BridgesN1 = bridgestemp \
    .sort_values(by=['road','km','constructionYear'], ascending=False) \
    .drop_duplicates(subset=['road', 'km'], keep='first')

BridgesN1 = BridgesN1.rename(columns={"LRPName": "lrp"})

# merge the roads and bridges datafile
merged = pd.merge(roads, BridgesN1, how="outer", on=["road", "lrp", "length", "lat", "lon", "chainage"])

# add type of road/bridge
merged["model_type"] = merged["lrp"].apply(lambda x: "sink" if x == "LRPS" else ("source" if x == "LRPE" else "link"))
merged.loc[merged["condition"].notnull(), "model_type"] = "bridge"

merged = merged.sort_values(by=['road','chainage'],ascending = False)
merged = merged[2:]
merged = merged.reset_index()

# for the n1 the source should be the first entry, as we no not consider the whole road but only to Chitigong, this has to be done artificially
merged.loc[0,"model_type"] = "source"
merged.loc[0,"name"] = "source"

merged["bridge_name"] = merged["name"]
merged["name"] = merged["model_type"]

# create the index as a column
merged["id"] = range(len(merged))

# order and rename columns so it fits data structure
merged = merged[["road", "id", "model_type", "name", "lat", "lon", "length", "condition", "bridge_name"]]

# save to csv (only the N1 road)
merged[merged["road"] == "N1"].to_csv("../data/processed/N1.csv", index=None)