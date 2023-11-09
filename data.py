import sqlite3
import pandas as pd
import geopandas as gpd
# conn = sqlite3.connect('FPA_FOD_20170508.sqlite')
# df = pd.read_sql_query(
#     'SELECT * FROM Fires where FIRE_SIZE>100000 and FIRE_SIZE is not null', conn)
# df = df[['FIRE_NAME', 'FIRE_YEAR',
#         'SOURCE_REPORTING_UNIT_NAME', 'STAT_CAUSE_DESCR',
#         'FIRE_SIZE', 'LATITUDE',
#         'LONGITUDE', 'STATE']]

gdf = gpd.read_file(r'phase-3-project-data/Wildfires_1878_2019_Polygon_Data/Shapefile/US_Wildfires_1878_2019.shp', rows=250)[['FireName', 'FireYear', 'Acres', 'FireCause', 'geometry']]

gdf["Acres"] = gdf["Acres"].apply(round)