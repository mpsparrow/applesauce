import json

# config loader and unloader
def configLoad(filename):
    with open(filename, 'r') as jsondata:
        f = json.load(jsondata)
    return f

def configDump(filename, data):
    with open(filename, 'w') as jsondata:
        json.dump(data, jsondata, indent=4)