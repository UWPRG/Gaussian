# log2xyz

Converts Gaussian log files (`*.log`) to `*.xyz` files for easy visualization on Hyak.

In an optimization job, it will write coordinates at all optimization steps. Using `-l` or `--last-frame` will override this and only return the final frame. If using post-Hartree-Fock level of theory (only MP2 and MP3 supported), must specify with `-p` or `--post-hartree-fock` followed by the level of theory.

Does not currently support sequential energy evaluation post optimization (e.g., MP2/cc-pVTZ//B3LYP/6-31G).

## Dependencies
- `python`
- `pandas`
- **Gaussian 16 log files**

## Usage
```
usage: log2xyz [-h] [-s] [-c] [-a] [--no-energy] [-l] [-p POST_HARTREE_FOCK]
               [-o OUTFILE]
               logfile

positional arguments:
  logfile               full name of log file with extension (e.g.,
                        "<filename>.log"); output is saved in <filename>.xyz

optional arguments:
  -h, --help            show this help message and exit
  -s, --scan            denotes a scan calulation
  -c, --no-clobber      prevent overwrite of XYZ file with the name
                        <filename>.xyz
  -a, --all             save all frames, regardless of it being a scan
  --no-energy           turn off energy recording
  -l, --last-frame      save only last structure
  -p POST_HARTREE_FOCK, --post-hartree-fock POST_HARTREE_FOCK
                        denotes a post-Hartree-Fock level of theory; default
                        assumes semiempirical, HF, or DFT level of theory;
                        valid options are: MP2, MP3
  -o OUTFILE, --outfile OUTFILE
                        output file name with or without xyz extension; xyz
                        extension is forced; optional
```

# Installation
```
pip install -e .
```
