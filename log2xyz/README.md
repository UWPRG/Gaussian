# log2xyz

Converts Gaussian log files (`*.log`) to `*.xyz` files for easy visualization on Hyak.

In an optimization job, it will write coordinates at all optimization steps. Using `-l` or `--last-frame` will override this and only return the final frame.

**Only applies to Gaussian 16 log files.**

## Usage
```
usage: log2xyz [-h] [-s] [-c] [-a] [--no-energy] [-l] [-o OUTFILE] logfile

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
  -o OUTFILE, --outfile OUTFILE
                        output file name with or without xyz extension; xyz
                        extension is forced; optional
```
