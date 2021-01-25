from fluigi.pnr.sa.saplace import SAPlace
from fluigi.pnr.sa.salayout import SALayout
from pymint import MINTDevice
import fluigi.utils as utils
from fluigi.primitives import (
    pull_defaults,
    pull_dimensions,
    pull_terminals,
    # stop_java_vm,
)
from fluigi.pnr.layout import Layout, PlaceAndRouteAlgorithms, RouterAlgorithms
import sys
import os
from pathlib import Path
import argparse
import fluigi.parameters as parameters
import json
import networkx as nx
import pyfiglet
from parchmint import Device, device
from fluigi.pnr.terminalassignment import assign_single_port_terminals

from fluigi.pnr.placement.graph import (
    generatePlanarLayout,
    generateSpectralLayout,
    generateSpringLayout,
    generateHOLALayout,
)

from fluigi.pnr.placement.simulatedannealing import (
    generate_simulated_annealing_layout,
    generate_simulated_annealing_layout_v2,
)

import faulthandler

faulthandler.enable()


def generate_device_from_mint(
    file_path: str, skip_constraints: bool = False
) -> MINTDevice:
    current_device = MINTDevice.from_mint_file(file_path, skip_constraints)
    if current_device is None:
        raise Exception("Error generating device from the MINT file !")
    try:
        # start_java_vm()
        pull_defaults(current_device)
        pull_dimensions(current_device)
        pull_terminals(current_device)
        # stop_java_vm()
    except Exception as e:
        print("Error getting Primitive data: {}".format(e))
    print(
        "Setting Default MAX Dimensions to the device: ({}, {})".format(
            parameters.DEVICE_X_DIM, parameters.DEVICE_Y_DIM
        )
    )
    return current_device


def generate_device_from_parchmint(file_path: str) -> Device:
    with open(file_path) as data_file:
        text = data_file.read()
        device_json = json.loads(text)
        return Device(device_json)


def main():

    parser = argparse.ArgumentParser()

    parser.add_argument("input", help="This is the file thats used as the input ")
    parser.add_argument(
        "--outpath", type=str, default="out/", help="This is the output directory"
    )
    parser.add_argument(
        "-c",
        "--convert",
        action="store_true",
        help="Sets the flag to only convert the design and nothing else",
    )
    parser.add_argument(
        "-r",
        "--route",
        action="store_true",
        help="Sets the flag to only perform the routing",
    )
    parser.add_argument(
        "-u",
        "--unconstrained",
        action="store_true",
        help="Sets the flag to skip constraint parsing",
    )

    args = parser.parse_args()

    ascii_banner = pyfiglet.figlet_format("Fluigi")
    print(ascii_banner)

    print("output dir:", args.outpath)
    print("Running File: " + args.input)
    if Path(args.input).exists() is False:
        print("Could not find the input file - {}".format(args.input))
        return 0

    abspath = Path(args.outpath).resolve()
    parameters.OUTPUT_DIR = abspath

    if os.path.isdir(abspath) is not True:
        print("Creating the output directory:")
        path = Path(parameters.OUTPUT_DIR)
        path.mkdir(parents=True)

    current_device = None

    extension = Path(args.input).suffix
    if extension == ".mint" or extension == ".uf":
        current_device = generate_device_from_mint(args.input, args.unconstrained)
    elif extension == ".json":
        # Push it through the parchmint parser
        file_path = str(Path(args.input).resolve())
        current_device = generate_device_from_parchmint(file_path)
    else:
        print("Unrecognized file Extension")
        exit(0)

    tt = os.path.join(
        parameters.OUTPUT_DIR, "{}_no_par.json".format(current_device.name)
    )
    with open(tt, "w") as f:
        json.dump(current_device.to_parchmint_v1(), f)

    print(current_device.G.edges)

    utils.printgraph(current_device.G, current_device.name + ".dot")

    # We exit the process if only convert is set to true
    if args.convert:
        sys.exit(0)

    # # Do Terminal Assignment
    # assign_single_port_terminals(current_device)

    if args.route is True:
        parameters.LAMBDA = 1

        # Set the device dimensions from the device
        parameters.DEVICE_X_DIM = current_device.params.get_param("xspan")
        parameters.DEVICE_Y_DIM = current_device.params.get_param("yspan")

        # Do just the routing and end the process
        layout = Layout()
        if current_device is None:
            raise Exception("Could not parse the device correctly")

        layout.importMINTwithoutConstraints(current_device)

        layout.route_nets(RouterAlgorithms.AARF)

        layout.apply_layout()

        tt = os.path.join(
            parameters.OUTPUT_DIR, "{}_only_route.json".format(current_device.name)
        )
        with open(tt, "w") as f:
            json.dump(current_device.to_parchmint_v1(), f)

        print("Completed Routing Operation, exiting...")
        exit(0)

    # Check if the device netlist is planar
    graph = current_device.G

    if nx.algorithms.check_planarity(graph) is False:
        print("Error - Non-planar graph seen")
        sys.exit(0)

    # Planar Rotuer
    parameters.LAMBDA = 1
    current_device.params.set_param("xspan", parameters.DEVICE_X_DIM)
    current_device.params.set_param("yspan", parameters.DEVICE_Y_DIM)

    layout = Layout()
    if current_device is None:
        raise Exception("Could not parse the device correctly")

    layout.importMINTwithoutConstraints(current_device)

    layout.place_and_route_design()

    layout.print_layout()

    # layout.route_nets(RouterAlgorithms.AARF)

    layout.apply_layout()

    tt = os.path.join(
        parameters.OUTPUT_DIR, "{}_placed_and_routed.json".format(current_device.name)
    )
    with open(tt, "w") as f:
        json.dump(current_device.to_parchmint_v1(), f)

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
    # layout.print_layout()

    tt = os.path.join(
        parameters.OUTPUT_DIR, "{}_hola_par.json".format(current_device.name)
    )
    with open(tt, "w") as f:
        json.dump(current_device.to_parchmint_v1(), f)

    utils.printgraph(layout.G, current_device.name + ".layout.dot")


if __name__ == "__main__":
    main()
