

## Requirements
The data checker relies on the following libraries:

numpy, xarray, argparse, dateutil.relativedelta, datetime, json, sys, os, pathlib, re, stat, logging, typing


## How to run

1. Add `${checkerdir}/src` to `PYTHONPATH` in `~/.bashrc`, where `${checkerdir}` is the full path to the checker directory:<br>
`export PYTHONPATH="${PYTHONPATH}:${checkerdir}/src"`

<br>

2. Configure the file `config_lu.json` which contains the following settings:
   - `directory`: the directory with the files requiring checking;
   - `log_path`: where to save logs (relative path inside the checker directory);
   - `base_path`: full path to the checker directory;
   - `required_file_types`: for the landuse files there are "multiple-management", "multiple-states", "multiple-transitions";
   - `required_variables`: variables which are mandatory to be in the files (for each file type independently)
   - `required_coords`: coordinates which are mandatory to be in the files (for each file type independently);
   - `required_attributes`: general attributes which are mandatory for the files;
   - `required_attributes_in_vars`: variable-specific attributes which are mandatory for the files.

<br>

3. Configure the file `${checkerdir}/src/variable-info.json` which contains the variable ranges requirements (for each file type independently).
<br>

4. Run: `python run_script.py config_lu.json`. 

## Checkers 

**FileNameChecker**: `${checkerdir}/src/checkers/checker_00_file_name.py`
 
Check filetype ("multiple-management", "multiple-states", or "multiple-transitions") and the filename (it should match a pattern `multiple-<...>_input4MIPs_landState_<...>_gn_YYYY-YYYY.nc`). 
It uses functions from `${checkerdir}/src/utils/misc_utils.py`.
<br>

**StandardComplianceChecker**: `${checkerdir}/src/checkers/checker_01_standard_compliance.py`

Check file permissions, dimension variables, compulsory attributes, `_FillValue`.
<br>  

**SpatialCompletenessChecker**: `${checkerdir}/src/checkers/checker_02_spatial_completeness.py`

Create the reference mask based on the reference file and check the presence of missing values. 
It uses functions from `${checkerdir}/src/utils/misc_utils.py`.
<br>

**SpatialConsistencyChecker**: `${checkerdir}/src/checkers/checker_03_spatial_consistency.py`

Check that the lon/lat grid points correspond to the reference file.
<br>

**TemporalConsistencyChecker**: `${checkerdir}/src/checkers/checker_04_temporal_consistency.py`

Check timesteps for consistency.
It uses functions from `${checkerdir}/src/utils/path_utils.py`.
<br>

**ValidRangesChecker**: `${checkerdir}/src/checkers/checker_05_valid_ranges.py`

Check that data values are in the required range (defined in `${checkerdir}/src/variable-info.json`).
It uses functions from `${checkerdir}/src/utils/misc_utils.py`.

## Other files

- `${checkerdir}/run_script.py`:  run the "main" function; `${checkerdir}/src/checkers/directory_checker.py` and `${checkerdir}/scripts/check_file.py`: configure the parameters and run all checkers;
- `${checkerdir}/src/utils`: functions which are used by checkers.

## Logging

For each run, the checker creates a new logging directory (its name includes the dataset name, current date and time) in  `${checkerdir}/logs` (the "logs" name can be modified in `config_lu.json` in "log_path"). 

There are files: 
- `<...>_errors.log` - only errors;
- `<...>_output.log` - all information about the checking.