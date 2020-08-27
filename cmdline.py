#!/usr/bin/env python3

from os import system
from mint.constraints.constraintlistener import ConstraintListener
from mint.mintErrorListener import MINTErrorListener
from primitives import pull_defaults, pull_dimensions
from pnr.layout import Layout
import sys
import os
from pathlib import Path
import time
from antlr4 import CommonTokenStream, ParseTreeWalker, FileStream
import argparse
import parameters
import json
import utils
import networkx as nx
import io
import pyfiglet

from mint.antlr.mintLexer import mintLexer
from mint.antlr.mintParser import mintParser
from mint.mintcompiler import MINTCompiler

from pnr.placement.graph import generatePlanarLayout, generateSpectralLayout, generateSpringLayout, generateHOLALayout


def main():

    parameters.PROGRAM_DIR = os.path.abspath(os.path.dirname(__file__))

    parser = argparse.ArgumentParser()

    parser.add_argument(
        'input', help="This is the file thats used as the input ")
    parser.add_argument('--outpath', type=str, default="out/",
                        help="This is the output directory")
    parser.add_argument('-c','--convert',action='store_true', help='Sets the flag to only convert the design and nothing else')
    
    args = parser.parse_args()

    ascii_banner = pyfiglet.figlet_format("Fluigi")
    print(ascii_banner)

    print("output dir:", args.outpath)
    print("Running File: "+args.input)

    extension = Path(args.input).suffix
    if extension != '.mint' and extension != '.uf' :
        print("Unrecognized file Extension")
        exit()

    abspath = os.path.abspath(args.outpath)
    parameters.OUTPUT_DIR = abspath

    if os.path.isdir(abspath) is not True:
        print("Creating the output directory:")
        path = Path(parameters.OUTPUT_DIR)
        path.mkdir(parents=True)

    finput = FileStream(args.input)

    lexer = mintLexer(finput)

    stream = CommonTokenStream(lexer)

    parser = mintParser(stream)

    #Connect the Error Listener
    parse_output = io.StringIO()
    parse_output.write("MINT SYNTAX ERRORS:\n")

    error_listener = MINTErrorListener(parse_output)
    parser.addErrorListener(error_listener)

    tree = parser.netlist()

    if error_listener.pass_through is False:
        print('STOPPED: Syntax Error(s) Found')
        sys.exit(0)
    
    walker = ParseTreeWalker()

    listener = MINTCompiler()

    walker.walk(listener, tree)

    constraint_listener = ConstraintListener(listener.current_device)

    walker.walk(constraint_listener, tree)


    current_device = listener.current_device
    
    #Check if the device netlist is planar
    graph = current_device.G


    if nx.algorithms.check_planarity(graph) == False:
        print('Error - Non-planar graph seen')
        sys.exit(0)


    try:
        pull_defaults(current_device)
        pull_dimensions(current_device)
    except Exception as e:
        print('Error getting Primitive data: {}'.format(e))


    layout = Layout()
    layout.importMINTwithoutConstraints(current_device)


    pull_defaults(current_device)
    pull_dimensions(current_device)

    generateSpringLayout(layout)

    layout.applyLayout()

    tt = os.path.join(parameters.OUTPUT_DIR, '{}_no_par.json'.format(current_device.name))
    with open(tt, 'w') as f:
        json.dump(current_device.to_parchmint_v1(), f)

    
    print(listener.current_device.G.edges)
    
    utils.printgraph(listener.current_device.G, current_device.name+'.dot')

    # We exit the process if only convert is set to true
    if args.convert:
        sys.exit(0)

    layout = Layout()
    layout.importMINTwithoutConstraints(current_device)
    
    # generateSpectralLayout(layout)
    generateHOLALayout(layout)
    layout.applyLayout()
    layout.ensureLegalCoordinates()

    tt = os.path.join(parameters.OUTPUT_DIR, '{}_hola_par.json'.format(current_device.name))
    with open(tt, 'w') as f:
        json.dump(current_device.toParchMintV1(), f)

    utils.printgraph(layout.G, current_device.name+'.layout.dot')



if __name__ == "__main__":
    main()
