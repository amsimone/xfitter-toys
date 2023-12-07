# xfitter-toys

A collection of code and scripts to generate and analyse pseudo-data (toys) with the xFitter program.

Patch xfitter to modify default structure of output files (easier to parse)

`git apply < patches/store_output.patch`

To generate toys run

`python3 run_toys.py`

and to create a folder with xfitter input datafiles run

`python3 parse_toys.py`
