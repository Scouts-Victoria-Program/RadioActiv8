import json
from pprint import pprint

with open('Base.geojson', 'r') as f:
    data=f.read()

obj = json.loads(data)

base_values_list = []

for f in obj['features']:
    name = f['properties']['Name']
    coords = f['geometry']['coordinates']
    #print(name, coords[:2])
    base_values_list.append([name, coords[:2], 0, 0])

pprint(base_values_list)
