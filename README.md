# Fluigi

## Dependencies

- Python 3.8+
- Cairo
- GraphViz

```bash
sudo apt-get install libbz2-dev libcairo2-dev pkg-config python3-dev libffi-dev graphviz
```

## Running Benchmark Test Scripts

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
