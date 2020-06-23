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

OSM Overpass Downloader works with "task files". A task file is a JSON file which contains a set of data acquisition tasks for the script.
This repository comes with a sample tasks file with the instructions to download bicycle way data for the Rhine-Neckar region and landcover information
for the Heidelberg area.

To order Overpass Downloader to process a given tasks file, call the script with the path/name of the tasks file as a command line argument:

```python3 overpass-downloader sample_tasks.json```

The script will then download the specified data and write the results to GeoJSON files. For each task of a tasks file, a separate GeoJSON file is created.
The produced GeoJSON files are named with the number/index of the task in the tasks list.


## Usage Considerations and Design Decisions

### Why GeoJSON?
Being a text-based format, GeoJSON is not the best geodata file format in terms of data compression. If large amounts of data are to be stored, this can be a very significant disadvantage. However, GeoJSON also has two great advantages: Since it is JSON, it is *very* simple to write using Python's built-in JSON functionality, 
and - even more important here - it is *schemaless*.

"schemaless" means that (as opposed to binary-encoded, relational-table-data-based file formats like *GeoPackage*) there is no need to specify a fixed schema for the geo-features. In GeoJSON, each feature can have its own arbitary set of properties, and you can even mix all types of supported geometries in one feature collection.

This comes very handy for the case of OpenStreetMap data, since in OSM, features (nodes, ways and relations) can have wildly different properties (called "tags").
With GeoJSON, no additional logic is needed at all to construct an appropriate data schema based on the tag information of all the features before the data can be
written to the file.
