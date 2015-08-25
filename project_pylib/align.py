import os
import shlex
from subprocess import Popen, PIPE
import imp
project_tools = imp.load_source('project_tools', os.path.join(os.path.dirname(__file__), 'project_tools.py'))
which = project_tools.which
seqwrap = project_tools.seqwrap
parse_fasta_string = project_tools.parse_fasta_string

# Gonnet_PAM250 is a scoring matrix based on an alignment of the entire SWISS-PROT database, by Gonnet, Cohen and Benner (1992).
# More info here: http://imed.med.ucm.es/Tools/sias_help.html
Gonnet_PAM250 = {
    'C': {
        'C': 12, 'S': 0, 'T': 0, 'P': -3, 'A': 0, 'G': -2, 'N': -2, 'D': -3, 'E': -3, 'Q': -2, 'H': -1, 'R': -2, 'K': -3, 'M': -1, 'I': -1, 'L': -2, 'V': 0, 'F': -1, 'Y': 0, 'W': -1, 'X': -3, '*': -8 },
    
    'S': {
        'C': 0, 'S': 2, 'T': 2, 'P': 0, 'A': 1, 'G': 0, 'N': 1, 'D': 0, 'E': 0, 'Q': 0, 'H': 0, 'R': 0, 'K': 0, 'M': -1, 'I': -2, 'L': -2, 'V': -1, 'F': -3, 'Y': -2, 'W': -3, 'X': 0, '*': -8 },
    
    'T': {
        'C': 0, 'S': 2, 'T': 2, 'P': 0, 'A': 1, 'G': -1, 'N': 0, 'D': 0, 'E': 0, 'Q': 0, 'H': 0, 'R': 0, 'K': 0, 'M': -1, 'I': -1, 'L': -1, 'V': 0, 'F': -2, 'Y': -2, 'W': -4, 'X': 0, '*': -8 },
    
    'P': {
        'C': -3, 'S': 0, 'T': 0, 'P': 8, 'A': 0, 'G': -2, 'N': -1, 'D': -1, 'E': 0, 'Q': 0, 'H': -1, 'R': -1, 'K': -1, 'M': -2, 'I': -3, 'L': -2, 'V': -2, 'F': -4, 'Y': -3, 'W': -5, 'X': -1, '*': -8 },
    
    'A': {
        'C': 0, 'S': 1, 'T': 1, 'P': 0, 'A': 2, 'G': 0, 'N': 0, 'D': 0, 'E': 0, 'Q': 0, 'H': -1, 'R': -1, 'K': 0, 'M': -1, 'I': -1, 'L': -1, 'V': 0, 'F': -2, 'Y': -2, 'W': -4, 'X': 0, '*': -8 },
    
    'G': {
        'C': -2, 'S': 0, 'T': -1, 'P': -2, 'A': 0, 'G': 7, 'N': 0, 'D': 0, 'E': -1, 'Q': -1, 'H': -1, 'R': -1, 'K': -1, 'M': -4, 'I': -4, 'L': -4, 'V': -3, 'F': -5, 'Y': -4, 'W': -4, 'X': -1, '*': -8 },
    
    'N': {
        'C': -2, 'S': 1, 'T': 0, 'P': -1, 'A': 0, 'G': 0, 'N': 4, 'D': 2, 'E': 1, 'Q': 1, 'H': 1, 'R': 0, 'K': 1, 'M': -2, 'I': -3, 'L': -3, 'V': -2, 'F': -3, 'Y': -1, 'W': -4, 'X': 0, '*': -8 },
    
    'D': {
        'C': -3, 'S': 0, 'T': 0, 'P': -1, 'A': 0, 'G': 0, 'N': 2, 'D': 5, 'E': 3, 'Q': 1, 'H': 0, 'R': 0, 'K': 0, 'M': -3, 'I': -4, 'L': -4, 'V': -3, 'F': -4, 'Y': -3, 'W': -5, 'X': -1, '*': -8 },
    
    'E': {
        'C': -3, 'S': 0, 'T': 0, 'P': 0, 'A': 0, 'G': -1, 'N': 1, 'D': 3, 'E': 4, 'Q': 2, 'H': 0, 'R': 0, 'K': 1, 'M': -2, 'I': -3, 'L': -3, 'V': -2, 'F': -4, 'Y': -3, 'W': -4, 'X': -1, '*': -8 },
    
    'Q': {
        'C': -2, 'S': 0, 'T': 0, 'P': 0, 'A': 0, 'G': -1, 'N': 1, 'D': 1, 'E': 2, 'Q': 3, 'H': 1, 'R': 2, 'K': 2, 'M': -1, 'I': -2, 'L': -2, 'V': -2, 'F': -3, 'Y': -2, 'W': -3, 'X': -1, '*': -8 },
    
    'H': {
        'C': -1, 'S': 0, 'T': 0, 'P': -1, 'A': -1, 'G': -1, 'N': 1, 'D': 0, 'E': 0, 'Q': 1, 'H': 6, 'R': 1, 'K': 1, 'M': -1, 'I': -2, 'L': -2, 'V': -2, 'F': 0, 'Y': 2, 'W': -1, 'X': -1, '*': -8 },
    
    'R': {
        'C': -2, 'S': 0, 'T': 0, 'P': -1, 'A': -1, 'G': -1, 'N': 0, 'D': 0, 'E': 0, 'Q': 2, 'H': 1, 'R': 5, 'K': 3, 'M': -2, 'I': -2, 'L': -2, 'V': -2, 'F': -3, 'Y': -2, 'W': -2, 'X': -1, '*': -8 },
    
    'K': {
        'C': -3, 'S': 0, 'T': 0, 'P': -1, 'A': 0, 'G': -1, 'N': 1, 'D': 0, 'E': 1, 'Q': 2, 'H': 1, 'R': 3, 'K': 3, 'M': -1, 'I': -2, 'L': -2, 'V': -2, 'F': -3, 'Y': -2, 'W': -4, 'X': -1, '*': -8 },
    
    'M': {
        'C': -1, 'S': -1, 'T': -1, 'P': -2, 'A': -1, 'G': -4, 'N': -2, 'D': -3, 'E': -2, 'Q': -1, 'H': -1, 'R': -2, 'K': -1, 'M': 4, 'I': 2, 'L': 3, 'V': 2, 'F': 2, 'Y': 0, 'W': -1, 'X': -1, '*': -8 },
    
    'I': {
        'C': -1, 'S': -2, 'T': -1, 'P': -3, 'A': -1, 'G': -4, 'N': -3, 'D': -4, 'E': -3, 'Q': -2, 'H': -2, 'R': -2, 'K': -2, 'M': 2, 'I': 4, 'L': 3, 'V': 3, 'F': 1, 'Y': -1, 'W': -2, 'X': -1, '*': -8 },
    
    'L': {
        'C': -2, 'S': -2, 'T': -1, 'P': -2, 'A': -1, 'G': -4, 'N': -3, 'D': -4, 'E': -3, 'Q': -2, 'H': -2, 'R': -2, 'K': -2, 'M': 3, 'I': 3, 'L': 4, 'V': 2, 'F': 2, 'Y': 0, 'W': -1, 'X': -1, '*': -8 },
    
    'V': {
        'C': 0, 'S': -1, 'T': 0, 'P': -2, 'A': 0, 'G': -3, 'N': -2, 'D': -3, 'E': -2, 'Q': -2, 'H': -2, 'R': -2, 'K': -2, 'M': 2, 'I': 3, 'L': 2, 'V': 3, 'F': 0, 'Y': -1, 'W': -3, 'X': -1, '*': -8 },
    
    'F': {
        'C': -1, 'S': -3, 'T': -2, 'P': -4, 'A': -2, 'G': -5, 'N': -3, 'D': -4, 'E': -4, 'Q': -3, 'H': 0, 'R': -3, 'K': -3, 'M': 2, 'I': 1, 'L': 2, 'V': 0, 'F': 7, 'Y': 5, 'W': 4, 'X': -2, '*': -8 },
    
    'Y': {
        'C': 0, 'S': -2, 'T': -2, 'P': -3, 'A': -2, 'G': -4, 'N': -1, 'D': -3, 'E': -3, 'Q': -2, 'H': 2, 'R': -2, 'K': -2, 'M': 0, 'I': -1, 'L': 0, 'V': -1, 'F': 5, 'Y': 8, 'W': 4, 'X': -2, '*': -8 },
    
    'W': {
        'C': -1, 'S': -3, 'T': -4, 'P': -5, 'A': -4, 'G': -4, 'N': -4, 'D': -5, 'E': -4, 'Q': -3, 'H': -1, 'R': -2, 'K': -4, 'M': -1, 'I': -2, 'L': -1, 'V': -3, 'F': 4, 'Y': 4, 'W': 14, 'X': -4, '*': -8 },
    
    'X': {
        'C': -3, 'S': 0, 'T': 0, 'P': -1, 'A': 0, 'G': -1, 'N': 0, 'D': -1, 'E': -1, 'Q': -1, 'H': -1, 'R': -1, 'K': -1, 'M': -1, 'I': -1, 'L': -1, 'V': -1, 'F': -2, 'Y': -2, 'W': -4, 'X': -1, '*': -8 },
    
    '*': {
        'C': -8, 'S': -8, 'T': -8, 'P': -8, 'A': -8, 'G': -8, 'N': -8, 'D': -8, 'E': -8, 'Q': -8, 'H': -8, 'R': -8, 'K': -8, 'M': -8, 'I': -8, 'L': -8, 'V': -8, 'F': -8, 'Y': -8, 'W': -8, 'X': -8, '*': 1 }
}



def run_clustalo(sequence_ids, sequences, outfmt='vienna', dealign=True, force=False, clustalo_binary=None):
    """Multiple sequence alignment using clustalo

    Pass a list of sequence ids and a list of sequences
    Returns a list of aligned sequences
    """
    # If clustalo binary not passed as an argument, try to autodetect
    if clustalo_binary == None:
        # First try searching $PATH
        which_result = which('clustalo')
        if which_result != None:
            clustalo_binary = which_result
    if clustalo_binary != None:
        if not os.path.exists(clustalo_binary):
            raise Exception, 'clustalo binary not found.'
    else:
        raise Exception, 'clustalo binary not found.'

    # Put the lists of sequence ids and sequences into FASTA format
    nseq = len(sequence_ids)
    seq_string = ''
    for s in range(nseq):
        try:
            seq_string += '>%s\n%s\n' % (sequence_ids[s], seqwrap(sequences[s]))
        except:
            print sequence_ids[s], sequences[s]
            raise

    # Construct the command string
    command = '%(clustalo_binary)s -i - --outfmt=%(outfmt)s' % vars()
    if dealign == True:
        command += ' --dealign'
    if force==True:
        command += ' --force'

    # Execute the command
    p = Popen(shlex.split(command), stdin=PIPE, stdout=PIPE)
    stdout = p.communicate(input=seq_string)[0]

    # Extract the aligned sequences and return
    aln_seq_ids, aln_seqs = parse_fasta_string(stdout)
    return aln_seqs


def score_aln(seq1, seq2, gap_penalty=0):
    '''
    Scores an alignment between two sequences using a PAM matrix.
    '''
    if len(seq1) != len(seq2):
        raise Exception, 'ERROR: len(seq1) must equal len(seq2)'
    score = 0
    for i in range(len(seq1)):
        if seq1[i] == '-' or seq2[i] == '-':
            score = gap_penalty
        else:
            score += Gonnet_PAM250[seq1[i].upper()][seq2[i].upper()]
    return score

