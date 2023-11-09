import folium
import geopandas as gpd
from pyproj import Transformer
from shapely import Point


gdf = gpd.read_file(r'phase-3-project-data/Wildfires_1878_2019_Polygon_Data/Shapefile/US_Wildfires_1878_2019.shp', rows=50)
# print(gdf.columns)

# gdf.to_dict('records')
# gdf[['geometry']]


# gdf[['geometry']].take([0])


# gdf[['geometry']].take([0]).to_dict('records')[0]['geometry']



# gdf[['geometry']].take([0]).to_dict('records')[0]['geometry'].boundary

hope = gdf[['geometry']].take([0]).to_dict('records')[0]['geometry']
# gpd.GeoSeries(hope).simplify(tolerance=0.001)
# gpd.GeoSeries(hope).simplify(tolerance=0.001).to_json()

geo_hope = gpd.GeoSeries(hope).simplify(tolerance=0.001)

gdf_rows = list(gdf.iterrows())
# print(list(gdf_rows))

transformer = Transformer.from_crs('EPSG:102100', 'EPSG:4326', always_xy = True)
result = [transformer.transform(row['x'], row['y']) for row in geo_hope.get_coordinates().to_dict('records')]




"""
We need to loop through all rows of our GDF and look at each geometry.
For each geometry, we want to loop through all points and get the relevant 
longitudinal and latitudinal points. We can then save those within a tuple and
put that in a big ass list. Each list corresponds to a specific polygon/geometry, 
and all tuples of that list correspond to each relevant lon/lat coordinate.
"""

for _, r in gdf.iterrows():
    sim_geo = gpd.GeoSeries(r['geometry']).simplify(tolerance=0.001).get_coordinates().to_dict('records')
    latlong_geo = gpd.GeoSeries(map(lambda x: Point(x[0],x[1]), [transformer.transform(row['x'], row['y']) for row in sim_geo]), crs='EPSG:4326')
    
    geo_j = folium.GeoJson(data=latlong_geo)
    

