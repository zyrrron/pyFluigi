import click


@click.command(name="fluigi")
@click.option("--version", "-v", is_flag=True, help="Show version")

def lfr_compile(
    input_files,
    output_path,
    library,
    no_gen_flag,
    no_annotations_flag,
    pre_load_directory,
    pre_load_file,
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

    compile_lfr(
        input_files,
        output_path,
        library,
        no_gen_flag,
        no_annotations_flag,
        pre_load_directory,
        pre_load_file,
    )
