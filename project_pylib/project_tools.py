import os


def seqwrap(sequence, add_star=False, char_width=60):
    """
    Wraps a sequence string to a given character width (default: 60).

    Parameters
    ----------
    sequence: str
    add_star: bool
        If add_star is set to true, an asterisk will be added
    to the end of the sequence, for compatibility with
    Modeller.
    wrap_width: int
        Default: 60

    Returns
    -------
    wrapped: str
    """
    if add_star:
        sequence += '*'
    wrapped = ''
    for i in range(0, len(sequence), char_width):
        wrapped += sequence[i: i+char_width] + '\n'
    return wrapped


def sequnwrap(sequence):
    """
    Removes new-lines from a sequence string.

    Parameters
    ----------
    sequence: str

    Returns
    -------
    unwrapped: str
    """
    unwrapped = sequence.strip()
    unwrapped = ''.join(unwrapped.split('\n'))
    return unwrapped


def parse_nested_dicts(nested_dict, parse_keys):
    """
    Pass a nested dict structure and a list of keys to parse hierarchically.
    """
    if not isinstance(nested_dict, dict):
        raise Exception, 'parse_nested_dicts expected to be passed a dict.'

    child = nested_dict

    for parse_key in parse_keys:
        #current_dict = get_from_dict(current_dict, parse_key)
        child = child.get(parse_key)
        if child == None:
            return None
        elif parse_key == parse_keys[-1]:
            return child
        elif not isinstance(child, dict):
            return None


def which(program):
    """
    Searches $PATH environment variable (from parent shell) for a program.
    """
    fpath, fname = os.path.split(program)
    if fpath:
        if is_exe(program):
            return program
    else:
        for path in os.environ['PATH'].split(os.pathsep):
            path = path.strip('"')
            exe_file = os.path.join(path, program)
            if is_exe(exe_file):
                return exe_file

    return None


def is_exe(fpath):
    return os.path.isfile(fpath) and os.access(fpath, os.X_OK)


def parse_fasta_string(fasta_string):
    """
    Should also work with Vienna format
    """
    seq_strings = fasta_string.split('>')[1:]   # First element is '', so ignore
    seq_strings_split = [seq_string.split('\n') for seq_string in seq_strings]
    seq_ids = [seq_string_lines[0] for seq_string_lines in seq_strings_split]
    sequences = [''.join(seq_string_lines[1:]) for seq_string_lines in seq_strings_split]
    return seq_ids, sequences

