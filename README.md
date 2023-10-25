<<<<<<< HEAD
# Fluigi <img align="right" src="logo-Fluigi-color.png" width="250">
=======
# Fluigi <img align="right" src="fluigiLogo.png" width="250">
>>>>>>> 4456493eb2a5187c1078a2a26a53121fe09ed7c3

## Command Line Interface

The toolchain when installed correctly provides the following interface for the user 

```
Usage: fluigi [OPTIONS] COMMAND [ARGS]...

Options:
  --version
  --help     Show this message and exit.

Commands:
  convert-to-parchmint  Convert a list of input files into a single...
  lfr-compile           Compile a list of input files into a single...
  mint-compile          Compile a list of input files into a single...
  synthesize
  utils-render-svg

```

### CMD 1 - `convert-to-parchmint`
```
Usage: fluigi convert-to-parchmint [OPTIONS] INPUT_FILES...

  Convert a list of input files into a single output file. :param input_files:
  list of input files :param output_path: output file path :return:

Options:
  -o, --outpath PATH         This is the output directory
  --assign-terminals         Sets the flag to assign terminals to the pins in
                             default cases
  --skip-layout-constraints  Sets the flag to skip layout constraints
  --generate-graph-view      Sets the flag to generate the graph
  --help                     Show this message and exit.
```

### CMD 2 - `lfr-compile`

```
Usage: fluigi lfr-compile [OPTIONS] INPUT_FILES...

  Compile a list of input files into a single output file. :param input_files:
  list of input files :param output_path: output file path :param library:
  library name :param no_gen_flag: flag to disable generation of the output
  file :param no_annotations_flag: flag to disable generation of the output
  file :param pre_load_directory: directory to load pre-compiled files from
  :param pre_load_file: file to load pre-compiled files from :return:

Options:
  -o, --outpath PATH        Output path
  --technology TEXT         Technology Platform for LFR to compile the design
                            into
  --library-path TEXT       Library to use
  --no-gen BOOLEAN          Force the program to skip the device generation
  --no-annotations BOOLEAN  Force the compiler to skip reading postprocess
                            annotations like #MAP and #CONSTRAIN
  --no-gen BOOLEAN
  --pre-load PATH           This lets the preprocessor look for the different
                            design libraries that need to be added to the
                            memory (avoid using this outside bulk testing)
  --help                    Show this message and exit.
  ```

  ### CMD 3 - `mint-compile`

```
Usage: fluigi mint-compile [OPTIONS] INPUT_FILES...

  Compile a list of input files into a single output file. :param input_files:
  list of input files :param output_path: output file path :param route: flag
  to only perform routing :param render_svg: flag to generate the preview SVGs
  :return:

Options:
  -o, --outpath PATH              This is the output directory
  --route BOOLEAN                 Sets the flag to only perform the routing
  --render-svg BOOLEAN            Sets the flag to generate the preview SVGs
  --ignore-layout-constraints BOOLEAN
                                  Sets the flag to ignore layout constraints
  --help                          Show this message and exit.
  ```


### CMD 4 - `synthesize`

```
Usage: fluigi synthesize [OPTIONS] INPUT_FILES...

Options:
  -o, --outpath PATH   Output path
  --technology TEXT    Technology Platform for LFR to compile the design into
  --library-path PATH  Library to use
  --pre-load PATH      This lets the preprocessor look for the different
                       design libraries that need to be added to the memory
                       (avoid using this outside bulk testing)
  --help               Show this message and exit.

```

## Development Guide

### Step 1 - Cloning and tracking for development

First, run the following commands for recursively cloning all the required dependencies for the project and set up the sub repo branch tracking for development:

```
git clone --recurse-submodules -j8 https://github.com/cidarlab/pyfluigi
cd pyfluigi
git submodule update --init --recursive
git submodule foreach -q --recursive 'git checkout $(git config -f $toplevel/.gitmodules submodule.$name.branch || echo master)'
```
[Submodule Recipe Reference](https://gist.github.com/slavafomin/08670ec0c0e75b500edbaa5d43a5c93c)


### Step 2 - Setting up Benchmarks

Currently all the all benchmarks we are utilizing for this project are in the located in the Microfluidics-Benchmarks [Repository](https://github.com/CIDARLAB/Microfluidics-Benchmarks.git)

Since we do not want to create a git dependency within this project we just need to clone the repo into the current directory. 

```git clone https://github.com/CIDARLAB/Microfluidics-Benchmarks.git```

This will allow us to run the benchmarks

### Step 3 - Setting up 3DuF Primitives Server

Since none of the benchmarks will have all the component parameters and definitions by default, this step is crucial to ensure that the components generated by the tools are valid and compatible with 3DuF. The `primitives-server` needs to be setup in the following manner.

```
cd <different-folder-anywhere>
git clone https://github.com/cidarlab/3duf primitives-server
cd primitives-server
git checkout primitives-server
docker build -f primitives-server.Dockerfile -t primitives-server:latest .
docker run -p 6060:6060 primitives-server
```

### Step 4 - Start VSCode Devcontainer

The project comes packaged with VSCode Dev Container Support. 

1. Open the Project in VSCode
2. Install the dev containers Plugin
3. `cntrl+shift+P` for opening the command pallete and
4.  Select `DevContainers: Open Folder in Container`

### Step 5 - Python environment setup

Please use `poetry` for adding new dependencies, installing the environment, and running the tests.

```
poetry install
```


In order to access the `fluigi` command and have visibility of the python dependencies. A new poetry shell needs to be spawned:

```
poetry shell
```

To verify if everything is working, you can try the following command:

```
fluigi --help
```


### Step 6 - Running Benchmark Test Scripts (For full Fluigi Pipeline)


```
./scripts/convert.sh > covert-log_"`date +"%d-%m-%Y-%T"`".log 2>&1
```

```
./scripts/par.sh > par-log_"`date +"%d-%m-%Y-%T"`".log 2>&1
```

Generating renders
```
find ../solverpnr/result/dropx_ref/*.json -exec fluigi utils-render-svg {} +
```

## Poetry Environment

In order to access the `fluigi` command and have visibility of the python dependencies. A new poetry shell needs to be spawned:

```
poetry shell
```

To verify if everything is working, you can try the following command:

```
fluigi --help
```



## Dependencies

- Python 3.8+
- Cairo
- GraphViz

```bash
sudo apt-get install libbz2-dev libcairo2-dev pkg-config python3-dev libffi-dev graphviz
```



## Dependencies

- Python 3.8+
- Cairo
- GraphViz

```bash
sudo apt-get install libbz2-dev libcairo2-dev pkg-config python3-dev libffi-dev graphviz
```



## License

BSD-3-Clause

Copyright (c) 2023, CIDAR LAB All rights reserved.
<<<<<<< HEAD
=======

>>>>>>> 4456493eb2a5187c1078a2a26a53121fe09ed7c3
