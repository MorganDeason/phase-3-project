import folium
from dash import Dash, html, dash_table
from data import gdf
import flask
from pyproj import Transformer

# from folium.features import GeoJson, GeoJsonTooltip, GeoJsonPopup


us_map = folium.Map(location=[39.8283, -98.5795], zoom_start=4)

transformer = Transformer.from_crs('EPSG:102100', 'EPSG:4326', always_xy=True)


def bad_lat_calc(coord, adjust=0):
    return ((coord + 180 + adjust) % 360) - 180


for _, r in gdf.iterrows():
    # # Takes polygon and turns it into a series of points and simplifying it and then collects all of the points and puts them into a dictionary
    # sim_geo = gpd.GeoSeries(r['geometry']).simplify(tolerance=0.001).get_coordinates().to_dict('records')
    # # Loops through every point and transforms it from shitty coords to lat longs
    # transformed_data = [transformer.transform(row['x'], row['y']) for row in sim_geo]
    # # Geo series requires an array of shaply.Point. This line converts lat longs into points then into a GeoSeries
    # latlong_geo = gpd.GeoSeries(map(lambda x: Point(x[0], x[1]), transformed_data), crs='EPSG:4326')
    # # Adds to the map
    # geo_j = folium.GeoJson(data=latlong_geo)
    # geo_j.add_to(us_map)

    # Attempt to add markers for each fire
    fire_centroid = transformer.transform(
        r['geometry'].centroid.xy[0][0], r['geometry'].centroid.xy[1][0])
    fire_marker = folium.Marker(location=[bad_lat_calc(
        fire_centroid[1]+40), bad_lat_calc(fire_centroid[0]-100)], popup=r['FireName'])
    fire_marker.add_to(us_map)

# All of the lines fo the 'for'   appears to do something? Its very uneffiecient and needs improving
# Possible improvement is to stop going from GeoSeries to Dict to list back to GeoSeries(Lines 22, 24, 26)

us_map.save('us_map.html')

app = Dash(__name__, title='Historical Fires')

app.layout = html.Div(
    children=[html.H1("History of fires from 1878-2019"),
              html.Div(children=[

                  html.Div(id='map_container', children=[html.Iframe(id='map', src='./us_map', width='100%', height='1000')],
                           style={'flex': 2, 'padding': 5}
                           ),

                  html.Div(
                      [dash_table.DataTable(
                          data=gdf[['FireName', 'FireYear', 'Acres','FireCause']].to_dict('records'),
                          columns=[{'id': column, 'name': column} for column in gdf.drop(columns=["geometry"]).columns],
                          style_as_list_view=True,
                          page_size=32,
                          sort_action='native',
                          style_cell={'textAlign': 'center'},
                          style_header={
                              'backgroundColor': 'rgb(30,30,30)',
                              'color': 'white',
                              'fontWeight': 'bold',
                              'textAlign': 'center'
                          },
                          style_data={'backgroundColor': 'rgb(60,60,60)', 'color': 'white'
                                      },
                          style_table={'height': '1000px'}
                      )],
                      style={'flex': 1, 'padding': 5}
                  )
              ], style={'display': 'flex', 'height': 800})
              ], style={})


@app.server.route('/us_map')
def serve_us_map():
    return flask.send_from_directory('.', 'us_map.html')


if __name__ == '__main__':
    app.run(debug=True)
