# BioProfileKit

## Install
```bash
pip install -e .
python setup.py build_ext --inplace

```

## Parameter
Currently only supports .csv, .tsv and .json as input files
```bash 
 Options:
  -i,   --input PATH           Input file as .tsv, .csv or .json  [required]
  -t,   --tax                  Enable taxonomy analysis
  -f,   --func [cog|go]        Choose between COG or GO analysis, if validation is needed
  -tc,  --target_column TEXT   Target column for further analysis
  -h,   --help                 Show this message and exit.
```