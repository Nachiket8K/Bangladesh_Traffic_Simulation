import tensorflow as tf
import os
os.environ['USE_PYGEOS'] = '0'
import geopandas as gpd
import pandas as pd
# import contextily as ctx

dbf = gpd.read_file("../data/raw/roads.dbf")

frame = pd.read_csv("../data/processed/N1_N2_plus_sideroads.csv")

latmin = frame['lat'].min()
latmax = frame['lat'].max()
lonmin = frame['lon'].min()
lonmax = frame['lon'].max()

from shapely.geometry import Polygon

polyshape = gpd.GeoSeries(Polygon([(lonmin, latmin), (lonmin, latmax), (lonmax, latmax), (lonmax, latmin)]))
polydf = gpd.GeoDataFrame({'geometry': polyshape, 'df1': [1]})
polydf.crs = dbf.crs
clipped_gdf = gpd.clip(dbf, polydf)
clipped_gdf = clipped_gdf['geometry']
clipped_gdf = clipped_gdf.reset_index(drop=True)

points = []


def callfunc():
    with tf.device('/GPU:0'):
        for i in range(len(clipped_gdf)):
            # Iterate over all rows
            for j in range(len(clipped_gdf)):
                if j > i:
                    if clipped_gdf.geometry[i].touches(clipped_gdf.geometry[j]) == True:
                        point = clipped_gdf.geometry[i].intersection(clipped_gdf.geometry[j])
                        # print(point)
                        if point.geom_type == "Point":
                            point_coor = point.x, point.y
                            points.append(point_coor)
                        else:
                            try:
                                point_coor = [(p.x, p.y) for p in point]
                                points.append(point_coor)
                            except:
                                print(point)
                                break

            if i % 1000 == 0:
                print(i)
    return points


points=callfunc()

df1 = pd.DataFrame(points)
df1.to_csv('../data/processed/points_shapefile_new.csv')
