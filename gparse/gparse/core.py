import os.path
import re
import sys

import argparse
try:
    import numpy as np
except ImportError:
    raise ImportError("Install numpy to use this script.")


element_dict = {1: 'H', 2: 'He', 3: 'Li', 4: 'Be', 5: 'B', 6: 'C', 7: 'N',
                8: 'O', 9: 'F', 10: 'Ne', 11: 'Na', 16: 'S'}

def fortrandouble(x):
    """Converts string of Fortran double scientific notation to python float.
    
    Example
    -------
    >>> val = '-0.12345D+03'
    >>> print(fortrandouble(val))
    -123.45
    """
    return float(x.replace('D', 'E'))


class Args:
    # Empty class to house argparse variables.
    pass


if __name__ == '__main__':
    # Parse command line arguments --------------------------------------------
    parser = argparse.ArgumentParser(prog='log2xyz')
    parser.add_argument('-s', '--scan', action='store_true',
                        help='denotes a scan calulation')
    parser.add_argument('-c', '--no-clobber', action='store_false',
                        help='prevent overwrite of XYZ file with '
                        'the name <filename>.xyz')
    parser.add_argument('-a', '--all', action='store_true',
                        help='save all frames, regardless of it being a scan')
    parser.add_argument('--no-energy', action='store_true',
                        help='turn off energy recording')
    parser.add_argument('-l', '--last-frame', action='store_true',
                        help='save only last structure')
    parser.add_argument('-p', '--post-hartree-fock', help='denotes a ' +
                        'post-Hartree-Fock level of theory; default assumes ' +
                        'semiempirical, HF, or DFT level of theory; valid ' +
                        'options are: MP2, MP3')
    parser.add_argument('-o', '--outfile', default=None,
                        help='output file name with or ' +
                        'without xyz extension; xyz extension is forced; ' +
                        'optional')
    parser.add_argument('logfile', default=None,
                        help='full name of log file with extension (e.g., ' +
                        '"<filename>.log"); output is saved in <filename>.xyz')
    args = parser.parse_args(sys.argv[1:], namespace=Args)
    scan = args.scan
    logfile = args.logfile
    overwrite = args.no_clobber
    full = args.all
    no_energy = args.no_energy
    last_frame = args.last_frame
    post_hartree_fock = args.post_hartree_fock
    outfile = args.outfile

    # Check post-Hartree-Fock method ------------------------------------------
    post_HF_options = {'MP2': 'EUMP2', 'MP3': 'EUMP3'}
    if post_hartree_fock:
        assert post_hartree_fock in post_HF_options.keys(), \
            "{} not available. ".format(post_hartree_fock) +\
            "Must choose from: {}".format(post_HF_options.keys())
    else:
        pass

    # Read log file into lists ------------------------------------------------
    cartcoords = []
    frame_num = 0
    step_num = []
    step_pattern = r'\d+'
    energy = []
    scf_pattern =r'([-]?\d+\.\d+)'
    mp_pattern = r'([-]?\d+\.\d+[DE][+-]\d+)'
    with open(logfile, 'r') as logf:
        for line in logf:
            if 'Input orientation' in line.strip():
                # Throw away the 4 header lines.
                for _ in range(4):
                    _ = next(logf)
                cartcoords.append([])
                line = logf.readline()
                while not '-----' in line:
                    cartcoords[frame_num].append(line.split())
                    line = logf.readline()
                frame_num += 1
            elif 'Step number' in line.strip():
                nums = re.findall(step_pattern, line)
                step_num.append([int(n) for n in nums])
            elif not no_energy:
                # Set parameters for grepping the energy from log file
                if post_hartree_fock:
                    grep_string = post_HF_options[post_hartree_fock]
                    ener_pattern = mp_pattern
                else:
                    grep_string = 'SCF Done'
                    ener_pattern = scf_pattern
                if grep_string in line.strip():
                    ener_string = re.findall(ener_pattern, line)[-1]
                    ener_float = fortrandouble(ener_string)
                    energy.append(ener_float)
            else:
                pass

    # Prepare data for writing to file ----------------------------------------
    # Delete first and third columns from coordinates.
    cartcoords = np.array(cartcoords, dtype=np.float)
    cartcoords = np.delete(cartcoords, [0, 2] ,axis=2)

    # Determine which frames to write to file.
    if scan and not full:
        # `save_frames` is a list of frame indices to be saved, not actual
        # frame numbers.
        save_frames = []
        for i, step in enumerate(step_num[:-1]):
            # Only pull the last frame of each scan point.
            if step[2] != step_num[i + 1][2]:
                save_frames.append(i)
            else:
                pass
        # Save last frame as well.
        save_frames.append(len(step_num) - 1)
    else:
        if full:
            # Save all frames, even if it is a scan calculation.
            pass
        else:
            # Check if step numbers repeat (i.e., if calculation is a scan).
            unique_step_num = np.unique([step[-2] for step in step_num])
            # Allow for 1 or 2 extra frames associated with freq calculations.
            if len(step_num) - len(unique_step_num) < 2:
                pass
            else:
                raise Exception("Calculation is likely a scan. Recheck "
                                "arguments.\nIf so, add -s (or --scan) flag "
                                "to function call.")
        save_frames = range(len(step_num))

    # Writing to file ---------------------------------------------------------
    if outfile:
        if outfile.endswith('.xyz'):
            pass
        else:
            outfile = outfile + '.xyz'
        outputfile = outfile
    else:
        outputfile = os.path.splitext(logfile)[0] + '.xyz'

    if overwrite:
        # Do not change output file name.
        pass
    else:
        # Add version number without overwriting.
        counter = 0
        while os.path.exists(outputfile):
            if counter > 99:
                raise Exception("Too many versions.")
            else:
                pass
            if outfile:
                outputfile = os.path.splitext(outfile)[0] +\
                    '{}.xyz'.format(counter)
            else:
                outputfile = os.path.splitext(logfile)[0] +\
                    '{}.xyz'.format(counter)
            counter += 1

    with open(outputfile, 'w') as outf:
        if last_frame:
            save_frames = [save_frames[-1]]
        else:
            pass

        for f in save_frames:
            outf.write('{}\n'.format(len(cartcoords[f])))
            if no_energy:
                outf.write('i = {0:3d}\n'.format(step_num[f][-2]))
            else:
                outf.write('i = {0:3d}, E = {1: >17.12f}\n'
                           .format(step_num[f][-2], energy[f]))
            for line in cartcoords[f]:
                element = element_dict[int(line[0])]
                outf.write(' {0:s}\t\t\t{1: 2.5f}  {2: 2.5f}  {3: 2.5f}\n'\
                           .format(element, *line[1:]))

    print('Output written to {}'.format(outputfile))
