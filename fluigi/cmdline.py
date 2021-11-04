import json
from pathlib import Path
from typing import List
import click
from lfr.parameters import LIB_DIR as LFR_LIB_DIR
from parchmint.device import Device
import pyfiglet
from fluigi import parameters

from fluigi.utils import render_svg


def print_version(ctx, param, value):
    if not value or ctx.resilient_parsing:
        return

    import pkg_resources

    click.echo(pkg_resources.get_distribution("fluigi").version)
    ctx.exit()


@click.group()
@click.option(
    "--version", is_flag=True, callback=print_version, expose_value=False, is_eager=True
)
def default_cli():
    ascii_banner = pyfiglet.figlet_format("Fluigi")
    print(ascii_banner)


@default_cli.command(name="synthesize")
@click.argument("input_files", nargs=-1, required=True, type=click.Path(exists=True))
@click.option(
    "--outpath", "-o", default=".", help="Output path", type=click.Path(exists=True)
)
@click.option(
    "--technology",
    default="dropx",
    help="Technology Platform for LFR to compile the design into",
)
@click.option(
    "--library-path", default="", help="Library to use", type=click.Path(exists=True)
)
@click.option(
    "--pre-load",
    multiple=True,
    type=click.Path(exists=True),
    help=(
        "This lets the preprocessor look for the different design libraries that"
        " need to be added to the memory (avoid using this outside bulk testing)"
    ),
)
def synthesize(
    input_files: List[str],
    outpath: str,
    technology: str,
    library_path: str,
    pre_load: List[str],
):
    synthesize(input_files, outpath, technology, library_path, pre_load)


@default_cli.command(name="lfr-compile")
@click.argument(
    "input_files",
    nargs=-1,
    required=True,
    type=click.Path(exists=True),
)
@click.option(
    "--outpath", "-o", default=".", help="Output path", type=click.Path(exists=True)
)
@click.option(
    "--technology",
    default="dropx",
    help="Technology Platform for LFR to compile the design into",
)
@click.option("--library-path", default="", help="Library to use")
@click.option(
    "--no-gen",
    type=click.BOOL,
    default=False,
    help="Force the program to skip the device generation",
)
@click.option(
    "--no-annotations",
    type=click.BOOL,
    default=False,
    help=(
        "Force the compiler to skip reading postprocess annotations like #MAP and"
        " #CONSTRAIN"
    ),
)
@click.option("--no-gen", type=click.BOOL, default=False)
@click.option(
    "--pre-load",
    multiple=True,
    type=click.Path(exists=True),
    help=(
        "This lets the preprocessor look for the different design libraries that"
        " need to be added to the memory (avoid using this outside bulk testing)"
    ),
)
def lfr_compile(
    input_files: List[str],
    outpath: str,
    technology: str,
    library_path: str,
    no_gen: bool,
    no_annotations: bool,
    pre_load: List[str],
):
    """
    Compile a list of input files into a single output file.
    :param input_files: list of input files
    :param output_path: output file path
    :param library: library name
    :param no_gen_flag: flag to disable generation of the output file
    :param no_annotations_flag: flag to disable generation of the output file
    :param pre_load_directory: directory to load pre-compiled files from
    :param pre_load_file: file to load pre-compiled files from
    :return:
    """
    from lfr.api import compile_lfr

    # Check if library path is "" and set it to the default library path in lfr package
    if library_path == "":
        library_path = str(LFR_LIB_DIR)

    print(
        input_files, outpath, technology, library_path, no_gen, no_annotations, pre_load
    )

    compile_lfr(
        input_files=input_files,
        outpath=outpath,
        technology=technology,
        library_path=library_path,
        no_gen_flag=no_gen,
        no_annotations_flag=no_annotations,
        pre_load=pre_load,
    )


@default_cli.command(name="mint-compile")
@click.argument(
    "input_files",
    nargs=-1,
    required=True,
    type=click.Path(exists=True),
)
@click.option(
    "--outpath",
    "-o",
    default=".",
    help="This is the output directory",
    type=click.Path(exists=True),
)
@click.option(
    "--route",
    type=click.BOOL,
    default=False,
    help="Sets the flag to only perform the routing",
)
@click.option(
    "--render-svg",
    type=click.BOOL,
    default=False,
    help="Sets the flag to generate the preview SVGs",
)
@click.option(
    "--ignore-layout-constraints",
    type=click.BOOL,
    default=False,
    help="Sets the flag to ignore layout constraints",
)
def mint_compile(
    input_files: List[str],
    outpath: str,
    route: bool,
    render_svg: bool,
    ignore_layout_constraints: bool,
):
    """
    Compile a list of input files into a single output file.
    :param input_files: list of input files
    :param output_path: output file path
    :param route: flag to only perform routing
    :param render_svg: flag to generate the preview SVGs
    :return:
    """
    from fluigi.place_and_route import place_and_route_mint

    place_and_route_mint(
        input_files=input_files,
        outpath=outpath,
        route_only_flag=route,
        render_flag=render_svg,
        ignore_layout_constraints=ignore_layout_constraints,
    )


@default_cli.command(name="utils-render-svg")
@click.argument(
    "input_files",
    nargs=-1,
    required=True,
    type=click.Path(exists=True),
)
@click.option(
    "--outpath",
    "-o",
    default=".",
    help="This is the output directory",
    type=click.Path(exists=True),
)
def utils_render_svg(
    input_files: List[str],
    outpath: str,
):

    parameters.OUTPUT_DIR = Path(outpath)

    for input_file in input_files:
        devicejson = json.load(open(input_file))
        device = Device(devicejson)
        render_svg(device, "")


if __name__ == "__main__":
    default_cli()
