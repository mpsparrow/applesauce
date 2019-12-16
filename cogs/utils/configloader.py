import json

# config loader
def configLoad(filename):
    with open(filename, 'r') as jsondata:
        f = json.load(jsondata)
    return f

# config dumper
def configDump(filename, data):
    with open(filename, 'w') as jsondata:
        json.dump(data, jsondata, indent=4)