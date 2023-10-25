import faulthandler
import json
import os
import subprocess
import sys
from pathlib import Path

import networkx as nx
from parchmint import Device
from pymint import MINTDevice

import fluigi.parameters as parameters
import fluigi.utils as utils
from fluigi.conversions import add_spacing, generate_device_from_mint
<<<<<<< HEAD
=======

>>>>>>> 4456493eb2a5187c1078a2a26a53121fe09ed7c3
# from fluigi.pnr.dropx import place_and_route_dropx
from fluigi.pnr.layout import Layout, PlaceAndRouteAlgorithms, RouterAlgorithms
from fluigi.pnr.placement.graph import (
    generateHOLALayout,
    generatePlanarLayout,
    generateSpectralLayout,
    generateSpringLayout,
)
from fluigi.pnr.placement.simulatedannealing import (
    generate_simulated_annealing_layout,
    generate_simulated_annealing_layout_v2,
)
from fluigi.pnr.sa.salayout import SALayout
from fluigi.pnr.sa.saplace import SAPlace
from fluigi.pnr.terminalassignment import assign_single_port_terminals
from fluigi.pnr.utils import assign_component_ports, reduce_device_size, size_nodes
from fluigi.primitives import (  # stop_java_vm,
    pull_defaults,
    pull_dimensions,
    pull_terminals,
)

faulthandler.enable()


<<<<<<< HEAD
=======
def generate_device_from_parchmint(file_path: str) -> Device:
    """Generate fom a Parchmint JSON file

    Args:
        file_path (str): file path
>>>>>>> 4456493eb2a5187c1078a2a26a53121fe09ed7c3

    Returns:
        Device: Device that is read from the JSON
    """
    with open(file_path, "r", encoding="utf-8") as data_file:
        text = data_file.read()
        device_json = json.loads(text)
        return Device(device_json)


def place_and_route_mint(
    input_file: str,
    outpath: str,
    route_only_flag: bool,
    render_flag: bool,
    ignore_layout_constraints: bool,
):
    print("output dir:", outpath)
    print("Running File: " + str(input_file))
    if Path(input_file).exists() is False:
        print("Could not find the input file - {}".format(input_file))
        return 0

    abspath = Path(outpath).resolve()
    parameters.OUTPUT_DIR = abspath

    if os.path.isdir(abspath) is not True:
        print("Creating the output directory:")
        path = Path(parameters.OUTPUT_DIR)
        path.mkdir(parents=True)

<<<<<<< HEAD
    mint_device = None
    current_device = None

    extension = Path(input_file).suffix
    if extension == ".mint" or extension == ".uf":
        mint_device = generate_device_from_mint(input_file, ignore_layout_constraints)
        current_device = mint_device.device
=======
    current_mint_device = None
    current_device = None

    extension = Path(input_file).suffix
    if extension in (".mint", ".uf"):
        current_mint_device = generate_device_from_mint(input_file, ignore_layout_constraints)
>>>>>>> 4456493eb2a5187c1078a2a26a53121fe09ed7c3
        # Set the device dimensions
        current_mint_device.device.params.set_param("x-span", parameters.DEVICE_X_DIM)
        current_mint_device.device.params.set_param("y-span", parameters.DEVICE_Y_DIM)
        current_device = current_mint_device.device

    elif extension == ".json":
        # Push it through the parchmint parser
        file_path = str(Path(input_file).resolve())
        current_device = generate_device_from_parchmint(file_path)
        # Set the device dimensions from the device
        parameters.DEVICE_X_DIM = current_device.params.get_param("x-span")
        parameters.DEVICE_Y_DIM = current_device.params.get_param("y-span")
        current_mint_device = MINTDevice(current_device.name, current_device)

    else:
        print("Unrecognized file Extension")
        sys.exit(0)

    # If the render svg parameter flag is enabled, then just render the svg
    file_path = Path(input_file)
    if render_flag:
        if file_path.suffix == ".json":
            utils.render_svg(current_device, file_path.stem)
        else:
            print("File extension not supported")
        sys.exit(0)

    # Decide if we want to delete this later on
    size_nodes(current_mint_device.device)
    assign_component_ports(current_mint_device.device)

<<<<<<< HEAD
    temp_parchmint_file = os.path.join(parameters.OUTPUT_DIR, "{}_no_par.json".format(current_device.name))
    with open(temp_parchmint_file, "w") as f:
        json.dump(current_device.to_parchmint_v1_2(), f)
=======
    temp_parchmint_file = os.path.join(parameters.OUTPUT_DIR, f"{current_device.name}_no_par.json")
    with open(temp_parchmint_file, "w") as parchmint_dump_file:
        json.dump(current_device.to_parchmint_v1_2(), parchmint_dump_file)
>>>>>>> 4456493eb2a5187c1078a2a26a53121fe09ed7c3

    # print(current_device.G.edges)

    utils.printgraph(current_device.graph, current_device.name + ".dot")

    # TODO - Delete this later
    # place_and_route_dropx(current_device)

    sys.exit(0)
    # We exit the process if only convert is set to true
    # # Do Terminal Assignment
    # assign_single_port_terminals(current_device)

    if route_only_flag is True:
        parameters.LAMBDA = 1

        # Do just the routing and end the process
        layout = Layout()
        if current_device is None:
            raise Exception("Could not parse the device correctly")

        layout.importMINTwithoutConstraints(current_device)

        layout.route_nets(RouterAlgorithms.AARF)

        layout.apply_layout()

        temp_parchmint_file = os.path.join(parameters.OUTPUT_DIR, "{}_only_route.json".format(current_device.name))
        with open(temp_parchmint_file, "w") as parchmint_dump_file:
            json.dump(current_device.to_parchmint_v1_x(), parchmint_dump_file)

        print("Completed Routing Operation, exiting...")
        sys.exit(0)

    # Check if the device netlist is planar
    graph = current_device.G

    if nx.algorithms.check_planarity(graph) is False:
        print("Error - Non-planar graph seen")
        sys.exit(0)

    # Planar Rotuer
    parameters.LAMBDA = 1

    if current_device is None:
        raise Exception("Could not parse the device correctly")

    temp_parchmint_file = os.path.join(parameters.OUTPUT_DIR, "{}_temp_par.json".format(current_device.name))
    with open(temp_parchmint_file, "w") as parchmint_dump_file:
        json.dump(current_device.to_parchmint_v1_x(), parchmint_dump_file)

    binary_path = parameters.FLUIGI_DIR.joinpath("bin/place_and_route")
    proc = subprocess.Popen([binary_path, os.path.abspath(temp_parchmint_file)])
    proc.wait()
    return_code = proc.returncode
    print("PAR Return code:" + str(return_code))
    if return_code == 0:
        par_device = generate_device_from_parchmint(str(temp_parchmint_file))
        reduce_device_size(par_device, parameters.DEVICE_PADDING)
        utils.render_svg(par_device, "_par")

        tnew = parameters.OUTPUT_DIR.joinpath("{}_placed_and_routed.json".format(par_device.name))
        with open(tnew, "w") as parchmint_dump_file:
            json.dump(par_device.to_parchmint_v1_x(), parchmint_dump_file)
    else:
        par_device = generate_device_from_parchmint(str(temp_parchmint_file))
        # reduce_device_size(par_device, parameters.DEVICE_PADDING)
        utils.render_svg(par_device, "_par_failed")

        tnew = parameters.OUTPUT_DIR.joinpath("{}_placed_and_routed_failed.json".format(par_device.name))
        with open(tnew, "w") as parchmint_dump_file:
            json.dump(par_device.to_parchmint_v1_x(), parchmint_dump_file)

        print("Place and Route completed with errors, please check the terminal output for information")
        sys.exit(-1)

    sys.exit(0)

    layout = Layout()

    layout.importMINTwithoutConstraints(current_device)

    layout.place_and_route_design()

    layout.print_layout("preview")

    layout.apply_layout()

    temp_parchmint_file = os.path.join(parameters.OUTPUT_DIR, "{}_placed_and_routed.json".format(current_device.name))
    with open(temp_parchmint_file, "w") as parchmint_dump_file:
        json.dump(current_device.to_parchmint_v1_x(), parchmint_dump_file)

    sys.exit(0)

    # #Generate the Simulated Annealing Layout
    # generate_simulated_annealing_layout_v2(current_device)
    # generate_simulated_annealing_layout(layout)

    if current_device is None:
        print("Error - Current device wasn't parsed correctly")
        sys.exit(1)

    # Running the SA version of the layout
    layout = SALayout()
    if current_device is None:
        raise Exception("Could not parse the device correctly")

    layout.importMINTwithoutConstraints(current_device)

    parameters.LAMBDA = 100

    placer = SAPlace(layout)

    placer.place()

    generateSpringLayout(layout)

    layout.place_and_route_design()

    layout.apply_layout()

    # generateSpectralLayout(layout)
    # generateHOLALayout(layout)
    # layout.applyLayout()
    layout.ensureLegalCoordinates()

    temp_parchmint_file = os.path.join(parameters.OUTPUT_DIR, "{}_hola_par.json".format(current_device.name))
    with open(temp_parchmint_file, "w") as parchmint_dump_file:
        json.dump(current_device.to_parchmint_v1_x(), parchmint_dump_file)

    utils.printgraph(layout.G, current_device.name + ".layout.dot")
