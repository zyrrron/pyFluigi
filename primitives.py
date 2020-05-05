from pyMINT.mintdevice import MINTDevice
import subprocess
import json

def get_defaults(mint:str):

    cmd = ['node', 'index.js' , mint,  'defaults']
    
    # cmd = ['node', '--version']

    output = subprocess.run(cmd, cwd="./primitives/dist/", stdout=subprocess.PIPE)
    
    # p = Popen(cmd, shell=True, stdin=PIPE, stdout=PIPE, stderr=STDOUT, close_fds=True)
    # output = p.stdout.read()
    # print(output)
    try:
        python_object = json.loads(output.stdout.decode('utf-8'))
    except:
        print("Could not retrieve default parameters for {}".format(mint))
        return None

    
    return python_object

def get_dimensions(mint:str, params):
    cmd = ['node', 'index.js', mint, 'dimension', json.dumps(params.data)]
    # p = Popen(cmd, shell=True, stdin=PIPE, stdout=PIPE, stderr=STDOUT, close_fds=True)
    output = subprocess.run(cmd, cwd="./primitives/dist/", stdout=subprocess.PIPE)
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
        defaults = get_dimensions(component.entity, component.params)
        if defaults is None:
            print("Warning: Could not pull default values for {} of type :{}".format(component.name, component.entity))
            continue
        
        #Fills out all the missing params
        for key in defaults.keys():
            if not component.params.exists(key):
                component.params.setParam(key, defaults[key])
