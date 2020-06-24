# OSM Overpass Downloader

A simple Python script to download OpenStreetMap data and save it as GeoJSON files

## General Notes

- This is a Python 3 program. It *might* still work with Python 2.x, but this has not been tested and is not recommended.

## Installation

### Cloning
As the very first step, obviously, clone this repository ;).

### Installing Dependencies
OSM Overpass Downloader depends on the *OverPy* library which is usually not included in typical Python distributions. 
This repository includes a *requirements.txt* file which allows you to easily install all requirements using Pythons's package mangager *pip*. 
Move your shell working directory to where you cloned this repository and enter the following command:

```pip3 install -r requirements.txt```

## Using the Program

### Tasks Files

OSM Overpass Downloader works with "task files". A task file is a JSON file which contains a set of data acquisition tasks for the script.
This repository comes with a sample tasks file with the instructions to download bicycle way data for the Rhine-Neckar region and landcover information
for the Heidelberg area.

To order Overpass Downloader to process a given tasks file, call the script with the path/name of the tasks file as a command line argument:

```python3 overpass-downloader sample_tasks.json```

The script will then download the specified data and write the results to GeoJSON files. For each task of a tasks file, a separate GeoJSON file is created.
The produced GeoJSON files are named with the number/index of the task in the tasks list.

### Defining a Task

A download task is defined as a list of strings. Each string specifies a tag filter rule in the normal OSM overpass API syntax. The results of each tag filter are merged into one result data set (logical "OR" or "UNION") without duplicates. For example, the following task selects all features which have the tag "bicycle" with the value "yes" or the tag "highway" with the value "cycleway":

``` 
{    
    "description" : "Bicycle ways for the Rhine-Neckar region",
    "bbox": "(48.9,7.8, 49.8,9.7)",
    
    "tags": [
        "'bicycle'~'yes'",
        "'highway'='cycleway'",
        "'cycleway'"
    ]
}
``` 

Multiple allowed values for one tag can be given with the '|' operator:

``` 
 "tags": [
            "'bicycle'~'yes|designated|permissive|use_sidepath'"         
        ]
``` 

For more information about Overpass tag filters, please refer to the OSM Overpass API language documentation.


### Nodes, Ways, Relations, Tags - What is Downloaded and how is it stored?

OSM Overpass Downloader downloads *all nodes and ways* that match the given tag filters. Relations are currently not supported.

Transformation of the downloaded data to GeoJSON is done the following way:

Each *way* is stored as either a *LineString* or a *Polygon*. OSM Overpass Downloader tries to automatically figure out which of the two geometry types is a better fit for the data by checking two criteria:

- Is the first and last node coordinate of a way identical? If yes, the way is assumed to define an area and stored as a *Polygon*.
- Does the way have the tag "area=no". If yes, it is stored as a LineString, even if it has identical first and last node coorindates.

Each *node* is stored as a *Point*, but *only if the node is not part of one of the retrieved *ways*.

For each downloaded way and individual node, all of the object's tags are stored as properties of the resulting GeoJSON feature (Point, LineString or Polygon).


## Design Principles and Limitations

### Why GeoJSON as Output Format?
Being a text-based format, GeoJSON is not the best geodata file format in terms of data compression. If large amounts of data are to be stored, this can be a very significant disadvantage. However, GeoJSON also has two great advantages: Since it is JSON, it is *very* simple to write using Python's built-in JSON functionality, 
and - even more important here - it is *schemaless*.

"schemaless" means that (as opposed to binary-encoded, relational-table-data-based file formats like *GeoPackage*) there is no need to specify a fixed schema for the data to store. In GeoJSON, each feature can have its own arbitary set of properties, you can mix all types of supported geometries in one feature collection, and you can
start to write your file without having to know and specify the exact data structure of features you might want to write to the file along the way.

This comes very handy for the case of OpenStreetMap data, since in OSM, features (nodes, ways and relations) can have wildly different properties (called "tags").
With GeoJSON, you can simply

### Limitations and Peculiarities of Converting OSM Data to the OGC Simple Feature Model

TODO