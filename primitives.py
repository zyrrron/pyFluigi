from mint.mintdevice import MINTDevice
import subprocess
import json
import os
import parameters

#All the imports for the java pipe
import jpype
import jpype.imports
from jpype.types import *

jpype.startJVM(classpath=['./pnr/fluigi-java/Fluigi-jar-with-dependencies.jar'])

import java
from org.cidarlab.fluigi.fluigi import *

OLD_PRIMITIVES_CHECKLIST = [
    "DROPLET GENERATOR FLOW FOCUS",
    "DROPLET GENERATOR T",
    "LOGIC ARRAY"
    ]


def get_defaults(mint:str):

    if mint in [s.replace(" ", "") for s in OLD_PRIMITIVES_CHECKLIST]:
        print("Warning this is one of the the old fluigi primitives, this means that the we dont pull defaults")
        return None
    else:
        primitives_dir = os.path.join(parameters.PROGRAM_DIR, "primitives","dist")

        cmd = ['node', 'index.js' , mint,  'defaults']
        
        output = subprocess.run(cmd, cwd=primitives_dir, stdout=subprocess.PIPE)
        
        try:
            python_object = json.loads(output.stdout.decode('utf-8'))
        except:
            print("Could not retrieve default parameters for {}".format(mint))
            return None

        return python_object

def get_dimensions(mint:str, params):

    if mint in [s.replace(" ", "") for s in OLD_PRIMITIVES_CHECKLIST]:
        print("Warning this is one of the the old fluigi primitives, this means that the default values can be incorrect")
        
        map = dict()
        for key in params.data.keys():
            val = params.data[key]
            try: 
                map[key] = int(val)

            except ValueError:
                print("Found a non int param: {} - {}".format(key,val))
        
        python_object = dict(Fluigi.getDimensions(mint, java.util.HashMap(map)))
        print('Data Retrieved by the java pipe: {}'.format(python_object))
        return python_object

    else:
        primitives_dir = os.path.join(parameters.PROGRAM_DIR, "primitives","dist")

        cmd = ['node', 'index.js', mint, 'dimension', json.dumps(params.data)]

        output = subprocess.run(cmd, cwd=primitives_dir, stdout=subprocess.PIPE)

        try:
            python_object = json.loads(output.stdout.decode('utf-8'))
        except:
            print("Could not retrieve dimensions for {}".format(mint))
            print(output.stdout)
            return None

    
    return python_object


def get_terminals(mint:str, params):

    if mint in [s.replace(" ", "") for s in OLD_PRIMITIVES_CHECKLIST]:
        print("Warning this is one of the the old fluigi primitives, this means that the default values can be incorrect")
        
        map = dict()
        for key in params.data.keys():
            val = params.data[key]
            try: 
                map[key] = int(val)

            except ValueError:
                print("Found a non int param: {} - {}".format(key,val))
        
        python_object = dict(Fluigi.getTerminals(mint, java.util.HashMap(map)))
        print('Data Retrieved by the java pipe: {}'.format(python_object))
        return python_object

    else:
        primitives_dir = os.path.join(parameters.PROGRAM_DIR, "primitives","dist")

        cmd = ['node', 'index.js', mint, 'terminals', json.dumps(params.data)]

        output = subprocess.run(cmd, cwd=primitives_dir, stdout=subprocess.PIPE)

        try:
            python_object = json.loads(output.stdout.decode('utf-8'))
        except:
            print("Could not retrieve dimensions for {}".format(mint))
            print(output.stdout)
            return None

    
    return python_object


def pull_defaults(device: MINTDevice):
    for component in device.components:
        defaults = get_defaults(component.entity)
        if defaults is None:
            print("Warning: Could not pull default values for {} of type :{}".format(component.name, component.entity))
            continue
        
        #Fills out all the missing params
        for key in defaults.keys():
            if not component.params.exists(key):
                component.params.setParam(key, defaults[key])


def pull_dimensions(device:MINTDevice):
    for component in device.components:
        dims = get_dimensions(component.entity, component.params)
        if dims is None:
            print("Warning: Could not pull default values for {} of type :{}".format(component.name, component.entity))
            continue
        
        #Assign the xspan and yspan
        component.xspan = dims["x-span"]
        component.yspan = dims["y-span"]
        
def pull_terminals(device: MINTDevice):
    for component in device.components:
        terminals = get_terminals(component.entity, component.params)
        if terminals is None:
            print("Warning: Could not pull terminal data for {} of type: {}".format(component.name, component.entity))

        #Assign the terminals
