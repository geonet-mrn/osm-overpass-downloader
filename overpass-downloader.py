# -*- coding: utf-8 -*-

import overpy
import json
import time
import sys


def process_task(task, outfile_name):

    area = task['bbox']
    tags = task['tags']

    ################# BEGIN Construct query template ###############
    query_template = "[out:json];"

    # Add nodes part to query:
    query_template += "("

    for tag in tags:
        query_template += "node{a}[" + tag + "];"
        
    query_template += ");out body;"
    

    # Add ways part to query:
    query_template += "("

    for tag in tags:
        query_template += "way{a}[" + tag + "];"
        
    query_template += ");out body;"
    
    query_template += ">;out body;"
    ################# END Construct query template ###############
        
    query = query_template.format(a=area)



    #print("\n\nQuery:\n" + query + "\n")

    if 'description' in task:
        print("Now downloading: " + str(task['description']))
    else:
        print("Downloading ...")

    api = overpy.Overpass(url='https://lz4.overpass-api.de/api/interpreter')

    result = api.query(query)

    all_way_nodes = []


    geojson_output = {"type": "FeatureCollection", "features": []}


    ###################### BEGIN process ways #######################
    for way in result.ways:
    
        coords = []

        nodes = way.get_nodes(resolve_missing=True)

        all_way_nodes.extend(nodes)
        
        for node in nodes:        
            coords.append([float(node.lon), float(node.lat)])


        geometryType = "LineString"

        if len(nodes) > 2:
            
            # How to check whether a way is likely a polygon or not: 
            # https://wiki.openstreetmap.org/wiki/Overpass_turbo/Polygon_Features

            # TODO: 3 Add the remaining checks that are recommended on the aforementioned web page.

            if nodes[0].lon == nodes[-1].lon and nodes[0].lat == nodes[-1].lat:

                if way.tags.get("area") == "no":
                    print("It's a closed ring, but tagged as not an area")
                else:
                    geometryType = "Polygon"                
                    coords = [coords]

        feature = {"type": "Feature", "properties": way.tags, "geometry": { "type": geometryType, "coordinates": coords}}

        
        geojson_output["features"].append(feature)
    ###################### END process ways #######################


    ###################### BEGIN process nodes #######################
    for node in result.nodes:
        
        # If the node is part of a way (LineString or Polygon), don't add it as a separate point feature:
        if node in all_way_nodes:        
            continue
    
        feature = {"type": "Feature","properties": node.tags,"geometry": {"type": "Point", "coordinates": [float(node.lon), float(node.lat)]}}
            
        geojson_output['features'].append(feature)

    ###################### END process nodes #######################


    # Write result to GeoJSON file:    
    with open(outfile_name + ".geo.json", "w") as geojson_output_file:
        geojson_output_file.write(json.dumps(geojson_output))


    print("Nodes: %i" % len(result.nodes))
    print("Ways: %i" % len(result.ways))
    print("Relations: %i" % len(result.relations))




if len(sys.argv) < 2:
    print("Please pass the name/path of a tasks file as a command line argument.")
    exit(-1)



start = time.time()

tasksfile_path = sys.argv[1]

with open(tasksfile_path, "r") as tasksfile:
    taskslist = json.load(tasksfile)



for index, task in enumerate(taskslist):

    if 'skip' in task and task['skip']:
        continue
    
    process_task(task, str(index))



end = time.time()

print("\nAll tasks completed. Runtime: {:.1f} seconds.".format(float(end - start)))

