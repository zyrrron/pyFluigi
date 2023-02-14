# Fluigi

## Development Guide

### Cloning and tracking for development

First, run the following commands for recursively cloning all the required dependencies for the project and set up the sub repo branch tracking for development:

```
git clone --recurse-submodules -j8 https://github.com/cidarlab/pyfluigi
cd pyfluigi
git submodule update --init --recursive
git submodule foreach -q --recursive 'git checkout $(git config -f $toplevel/.gitmodules submodule.$name.branch || echo master)'
```
[Submodule Recipe Reference](https://gist.github.com/slavafomin/08670ec0c0e75b500edbaa5d43a5c93c)

Please use `poetry` for adding new dependencies, installing the environment, and running the tests.

```
poetry install
```

Use the vscode development container for development. The container will automatically install the required dependencies and set up the environment.

## Dependencies

- Python 3.8+
- Cairo
- GraphViz

```bash
sudo apt-get install libbz2-dev libcairo2-dev pkg-config python3-dev libffi-dev graphviz
```

## Running Benchmark Test Scripts (For full Fluigi Pipeline)


```
cd scripts
./convert.sh > covert-log_"`date +"%d-%m-%Y-%T"`".log 2>&1
```

```
cd scripts
./par.sh > par-log_"`date +"%d-%m-%Y-%T"`".log 2>&1
```

Generating renders
```
find ../solverpnr/result/dropx_ref/*.json -exec fluigi utils-render-svg {} +
```


## License

BSD-3-Clause

Copyright (c) 2021, CIDAR LAB All rights reserved.
