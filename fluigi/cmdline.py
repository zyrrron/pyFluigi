from pymint import MINTDevice
import fluigi.utils as utils
from fluigi.primitives import pull_defaults, pull_dimensions, pull_terminals
from fluigi.pnr.layout import Layout, RouterAlgorithms
import sys
import os
from pathlib import Path
import argparse
import fluigi.parameters as parameters
import json
import networkx as nx
import pyfiglet
from parchmint import Device
from fluigi.pnr.terminalassignment import assign_single_port_terminals


os.environ["LD_LIBRARY_PATH"] = "/home/krishna/CIDAR/pyfluigi/bin"

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


def generate_device_from_mint(file_path: str) -> MINTDevice:
    current_device = MINTDevice.from_mint_file(file_path)
    try:
        pull_defaults(current_device)
        pull_dimensions(current_device)
        pull_terminals(current_device)
    except Exception as e:
        print("Error getting Primitive data: {}".format(e))

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

    args = parser.parse_args()

    ascii_banner = pyfiglet.figlet_format("Fluigi")
    print(ascii_banner)

    print("output dir:", args.outpath)
    print("Running File: " + args.input)

    abspath = Path(args.outpath).resolve()
    parameters.OUTPUT_DIR = abspath

    if os.path.isdir(abspath) is not True:
        print("Creating the output directory:")
        path = Path(parameters.OUTPUT_DIR)
        path.mkdir(parents=True)

    current_device = None

    extension = Path(args.input).suffix
    if extension == ".mint" and extension == ".uf":
        current_device = generate_device_from_mint(args.input)
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

    layout = Layout()
    layout.importMINTwithoutConstraints(current_device)

    # Do Terminal Assignment
    assign_single_port_terminals(current_device)

    if args.route is True:
        # Do just the routing and end the process
        layout.route_nets(RouterAlgorithms.AARF)
        layout.print_layout()

    tt = os.path.join(
        parameters.OUTPUT_DIR, "{}_no_par.json".format(current_device.name)
    )
    with open(tt, "w") as f:
        json.dump(current_device.to_parchmint_v1(), f)

    # #Generate the Simulated Annealing Layout
    # generate_simulated_annealing_layout_v2(current_device)
    # generate_simulated_annealing_layout(layout)

    # Check if the device netlist is planar
    graph = current_device.G

    if nx.algorithms.check_planarity(graph) is False:
        print("Error - Non-planar graph seen")
        sys.exit(0)

    if current_device is None:
        print("Error - Current device wasn't parsed correctly")
        sys.exit(1)

    layout = Layout()
    layout.importMINTwithoutConstraints(current_device)

    generateSpringLayout(layout)

    layout.applyLayout()

    # generateSpectralLayout(layout)
    generateHOLALayout(layout)
    layout.applyLayout()
    layout.ensureLegalCoordinates()
    layout.print_layout()

    tt = os.path.join(
        parameters.OUTPUT_DIR, "{}_hola_par.json".format(current_device.name)
    )
    with open(tt, "w") as f:
        json.dump(current_device.to_parchmint_v1(), f)

    utils.printgraph(layout.G, current_device.name + ".layout.dot")


if __name__ == "__main__":
    main()
