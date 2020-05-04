import json

def write_file(obj, filename):
    """takes a list obj and saves a json file"""
    with open(filename, 'w') as outputfile:
        json.dump(obj, outputfile, indent=4)

def read_file(filename):
    """Reads in a json file"""
    with open(filename, 'r') as inputfile:
        json_file = json.load(inputfile)
    return json_file