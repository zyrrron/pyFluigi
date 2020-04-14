import sys
import os
from pathlib import Path
import time
from antlr4 import *
import argparse
import parameters

import utils

from pyMINT.antlr.mintLexer import mintLexer
from pyMINT.antlr.mintParser import mintParser
from pyMINT.mintcompiler import MINTCompiler


def main():
    parser = argparse.ArgumentParser()

    parser.add_argument(
        'input', help="This is the file thats used as the input ")
    parser.add_argument('--outpath', type=str, default="out/",
                        help="This is the output directory")

    args = parser.parse_args()
    print("output dir:", args.outpath)
    print(args.input)

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

    tree = parser.netlist()

    walker = ParseTreeWalker()

    listener = MINTCompiler()

    walker.walk(listener, tree)

    print(listener.currentdevice.G.edges)
    utils.printgraph(listener.currentdevice.G, "TEST")

if __name__ == "__main__":
    main()
