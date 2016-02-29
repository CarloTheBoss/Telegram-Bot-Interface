""" A bunch of useful functions, like DeJsoner or custom errors """

import json
import random

# Custom error, need a better name for it, seriously:

class MyError(Exception):
    pass
    
# From JSON-string to dict:     

def DeJson(json_str):
    return json.loads(json_str)

# From dict to JSON-string:

def ToJson(tmp_dict):
    return json.dumps(tmp_dict)
    
# It returns parameters (also optional) from a dict:

def GetParameter(tmp_dict, param_name, optional=False):
    if param_name in tmp_dict:
        return tmp_dict[ param_name ]
    else:
        return None
        #if optional:
        #    return None
        #else:
        #    raise MyError("Missing fundamental attribute")

# Prints a dict in a clearer way (i.e. with endlines and without all those brackets etc):

def PrintDict(tmp_dict):
    for i in tmp_dict:
        print(str(i) + ": " + str(tmp_dict[i]))

# Given a pathname of a certain file, returns its name from the rightmost stop_char to end (useful to get extensions etc)
    
def GetFormat(file_name, stop_char):
    format_string = ""
    index = len(file_name) - 1
    while index >= 0:
        if file_name[ index ] == stop_char:
            break
        format_string += file_name[ index ]
        index -= 1
    
    return format_string[::-1]

# Reads the last saved getUpdates offset from <botname>/offset.txt

def ReadOffset(file_path):
    offset = 0
    with open(file_path, "r") as f:
        offset = int( f.read() )
    if not f.closed:
        f.close()
    return offset

# Writes the new getUpdates offset on <botname>/offset.txt

def WriteOffset(file_path, offset):
    with open(file_path,"w") as f:
        f.write(str(offset))
    if not f.closed:
        f.close()

# Returns a random line of a .txt file

def GetRandomString(file_path):
    with open(file_path, "r") as f:
        c = f.readlines()
    
    return c[ random.randint(0, len(c)) ]
    
