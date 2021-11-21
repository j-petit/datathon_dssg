import folium
import pandas
from folium.plugins import TimestampedGeoJson

# Mapping table for colors
city_cluster = {'Aschaffenburg1': 'purple',
 'Berlin1': 'blue',
 'Berlin2': 'blue',
 'Berlin3': 'blue',
 'Berlin4': 'blue',
 'Berlin5': 'blue',
 'Berlin6': 'blue',
 'Berlin7': 'blue',
 'Berlin8': 'blue',
 'Berlin9': 'blue',
 'Berlin10': 'blue',
 'Berlin11': 'blue',
 'Berlin12': 'blue',
 'Berlin13': 'blue',
 'Berlin14': 'blue',
 'Berlin15': 'blue',
 'Berlin16': 'orange',
 'Berlin17': 'blue',
 'Berlin18': 'lightred',
 'Bochum1': 'purple',
 'Bochum2': 'purple',
 'Bonn1': 'darkblue',
 'Darmstadt1': 'red',
 'Dortmund1': 'purple',
 'Düsseldorf1': 'blue',
 'Düsseldorf2': 'beige',
 'Düsseldorf3': 'green',
 'Düsseldorf4': 'green',
 'Düsseldorf5': 'green',
 'Düsseldorf6': 'green',
 'Heidelberg1': 'orange',
 'Heidelberg2': 'orange',
 'Karlsruhe1': 'blue',
 'Köln1': 'green',
 'Köln2': 'darkblue',
 'Köln3': 'green',
 'Köln4': 'green',
 'Köln5': 'green',
 'Köln6': 'darkblue',
 'Köln7': 'darkblue',
 'Köln8': 'green',
 'Köln9': 'darkblue',
 'Köln10': 'darkblue',
 'Köln11': 'purple',
 'Köln12': 'red',
 'Köln13': 'red',
 'Köln14': 'red',
 'Köln15': 'red',
 'Ludwigsburg1': 'purple',
 'Osnabrück1': 'red',
 'Rostock1': 'darkred',
 'Rostock2': 'blue',
 'Rostock3': 'orange',
 'Rostock4': 'blue',
 'Rostock5': 'blue',
 'Rostock6': 'blue',
 'Rostock7': 'orange',
 'Rostock8': 'purple',
 'Rostock9': 'purple',
 'Rostock10': 'blue',
 'Rostock11': 'purple',
 'Rostock12': 'red',
 'Stuttgart1': 'green',
 'Stuttgart2': 'green',
 'Stuttgart3': 'purple',
 'Stuttgart4': 'purple',
 'Stuttgart5': 'red',
 'Stuttgart6': 'red',
 'Stuttgart7': 'red',
 'Stuttgart8': 'red',
 'Stuttgart9': 'red',
 'Stuttgart10': 'red',
 'Stuttgart11': 'red',
 'Stuttgart12': 'red',
 'Stuttgart13': 'red',
 'Stuttgart14': 'red',
 'Stuttgart15': 'red'}


blubb = 5

def bla():
    print("bla")

def create_geojson_features(df):
    features = []
    
    for _, row in df.iterrows():
        feature = {
            'type': 'Feature',
            'geometry': {
                'type':'Point', 
                'coordinates':[row['longitude'],row['latitude']]
            },
            'properties': {
                'time': str(row["date"]),
                'style': {'color' : ''},
                'icon': 'circle',
                'iconstyle':{
                    'fillColor': "red",
                    'fillOpacity': 0.6,
                    'stroke': 'true',
                    'radius': row['count'] + 5
                }
            }
        }
        features.append(feature)
    return features


def create_map(df, export=True, city_name="generic_city", start_location=[52.514066, 13.417751]):
    
    geo_json = create_geojson_features(df)
    our_map = folium.Map(location = start_location , tiles = "CartoDB Positron", zoom_start = 13)

    TimestampedGeoJson(geo_json,
                  period = 'PT1H',
                  duration = 'PT1M',
                  transition_time = 100,
                  auto_play = True).add_to(our_map)

    if export:
        our_map.save("../visualizations/" + city_name + ".html")
        
    return our_map