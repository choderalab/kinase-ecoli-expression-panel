import os, re, gzip
from lxml import etree
import pandas as pd
import Bio.pairwise2
import Bio.SubsMat.MatrixInfo
import imp
seq2html = imp.load_source('seq2html', '../../../project_pylib/seq2html.py')
gen_html = seq2html.gen_html

css_path = 'seqlib.css'

database_path = '../../../kinome-database/database.xml.gz'

# ========
# Read in plasmid data
# ========

df = pd.read_csv('plasmid-data.csv', index_col='cloneID')

# ========
# Read in database
# ========

with gzip.open(database_path) as database_file:
    DB_root = etree.parse(database_file)

alignments_dirpath = 'alignments'
if not os.path.exists(alignments_dirpath):
    os.mkdir(alignments_dirpath)

AlnPlasmidData = {
'cloneID': [],
'clone_seq_aln': [],
'UniProt_seq_aln': [],
'nconflicts_target_domain_region': [],
'pctidentity_target_domain_region': [],
'nextraneous_plasmid_residues': [],
'matching_domainID': [],
'matching_targetID': [],
}

# ========
# Iterate through plasmids
# ========

ofile = open('plasmid-data-aln.txt', 'w')

for cloneID in df.index:
    plasmid_data = df.loc[cloneID]
    AlnPlasmidData['cloneID'].append(cloneID)
    AlnPlasmidData['clone_seq_aln'].append(None)
    AlnPlasmidData['UniProt_seq_aln'].append(None)
    AlnPlasmidData['nconflicts_target_domain_region'].append(None)
    AlnPlasmidData['pctidentity_target_domain_region'].append(None)
    AlnPlasmidData['nextraneous_plasmid_residues'].append(None)
    AlnPlasmidData['matching_domainID'].append(None)
    AlnPlasmidData['matching_targetID'].append(None)

    # if cloneID != 'TAF1A-c005':
    #     continue

    print 'Working on cloneID %s' % cloneID
    UniProtAC = plasmid_data['UniProtAC']
    if UniProtAC == 'None':
        continue
    DB_entry = DB_root.find('entry/UniProt[@AC="%s"]/..' % UniProtAC)
    UniProt_entry_name = DB_entry.find('UniProt').get('entry_name')
    domains = DB_entry.findall('UniProt/domains/domain[@targetID]')

    UniProt_seq = ''.join(DB_entry.findtext('UniProt/isoforms/canonical_isoform/sequence').strip().split('\n'))
    plasmid_aa_seq = plasmid_data['construct_aa_seq']

    # Separate expression tag from the plasmid insert sequence

    expr_tag_regex = '(^MG{0,1}HHHHHHSSGVD[A-Z]*GTENLYFQSM)|(^MGSSHHHHHHSSGRENLYFQGHM)|(^MHHHHHHSSGRENLYFQG)'
    expr_tag_match = re.search(expr_tag_regex, plasmid_aa_seq)
    if expr_tag_match != None:
        expr_tag_seq = plasmid_aa_seq[ slice(*expr_tag_match.span()) ]
        plasmid_insert_seq = plasmid_aa_seq[expr_tag_match.end() : ]
    else:
        expr_tag_seq = None
        plasmid_insert_seq = plasmid_aa_seq

    # Conduct alignment
    matrix = Bio.SubsMat.MatrixInfo.gonnet
    gap_open = -10
    gap_extend = -0.5
    aln = Bio.pairwise2.align.globalds(UniProt_seq, plasmid_insert_seq, matrix, gap_open, gap_extend)
    aln = [aln[0][0], aln[0][1]]

    # Calculate the number of plasmid residues outside the target domain region (excluding N-terminal expression tag)
    # Also use this to determine which target domain the plasmid is most likely to represent
    nextraneous_plasmid_residues = []
    for domain in domains:
        nextraneous_plasmid_residues.append(0)
        domain_seq = ''.join(domain.findtext('sequence').strip().split('\n'))
        domain_seq_regex = ''.join([ aa + '-*' for aa in domain_seq ])
        UniProt_domain_aln_coords = re.search(domain_seq_regex, aln[0])
        for a in range(len(aln[0])):
            # print a, aln[1][a], UniProt_domain_aln_coords.start(), UniProt_domain_aln_coords.end()
            if (a < UniProt_domain_aln_coords.start() and aln[1][a] != '-') or (a >= UniProt_domain_aln_coords.end() and aln[1][a] != '-'):
                nextraneous_plasmid_residues[-1] += 1
    from operator import itemgetter
    domainID, nextraneous_plasmid_residues = min(enumerate(nextraneous_plasmid_residues), key=itemgetter(1))
    targetID = UniProt_entry_name + '_D' + str(domainID)


    # Add expression tag back into the aligned plasmid seq
    if expr_tag_seq != None:
        plasmid_seq_aln_aa_start = re.search('[A-Za-z]', aln[1]).start()
        UniProt_aln_list = list(aln[0])
        plasmid_aln_list = list(aln[1])
        plasmid_seq_aln_expr_tag_start = plasmid_seq_aln_aa_start - len(expr_tag_seq)
        # where the expression tag extends beyond the aligned sequence, just add '-' for now
        if plasmid_seq_aln_expr_tag_start < 0:
            for a in range(plasmid_seq_aln_expr_tag_start, 0):
                UniProt_aln_list.insert(0, '-')
                plasmid_aln_list.insert(0, '-')
            plasmid_seq_aln_expr_tag_start = 0
        # now that the alignments are the correct length, add in the expression tag sequence
        for a in range(len(expr_tag_seq)):
            plasmid_aln_list[plasmid_seq_aln_expr_tag_start + a] = expr_tag_seq[a].lower()

        aln[0] = ''.join(UniProt_aln_list)
        aln[1] = ''.join(plasmid_aln_list)

    # Make mismatching residues in plasmid sequence lower case
    plasmid_aln_list = list(aln[1])
    for a in range(len(aln[0])):
        if aln[1][a] != aln[0][a]:
            plasmid_aln_list[a] = aln[1][a].lower()
    aln[1] = ''.join(plasmid_aln_list)

    # find UniProt domains and generate custom CSS assignments to highlight target domains of UniProt sequence in red ('c4')
    aa_css_class_list = [None] * len(aln)
    aa_css_class_list[0] = ['bl'] * len(aln[0])
    nconflicts = []
    pctidentity = []
    for domain in domains:
        domain_seq = ''.join(domain.findtext('sequence').strip().split('\n'))
        domain_seq_regex = ''.join([ aa + '-*' for aa in domain_seq ])
        UniProt_domain_aln_coords = re.search(domain_seq_regex, aln[0])
        aa_css_class_list[0][slice(*UniProt_domain_aln_coords.span())] = ['c4'] * (UniProt_domain_aln_coords.end() - UniProt_domain_aln_coords.start())

        # Count conflicting residues within the target domain region
        nconflicts.append(0)
        for a in range(UniProt_domain_aln_coords.start(), UniProt_domain_aln_coords.end()):
            if aln[0][a] == '-' or aln[1][a] == '-':
                nconflicts[-1] += 1
            elif aln[0][a].upper() != aln[1][a].upper():
                nconflicts[-1] += 1

        # Calculate percent identity
        pctidentity.append((len(domain_seq) - nconflicts[-1]) * 100. / float(len(domain_seq)))

    nconflicts = nconflicts[domainID]
    pctidentity = pctidentity[domainID]


    additional_data = [[None, nconflicts],[None, nextraneous_plasmid_residues]]

    # Write to aligned sequences to text file
    ofile.write(aln[0] + '\n')
    ofile.write(aln[1] + '\n\n')

    # Construct AlnPlasmidData dict
    AlnPlasmidData['clone_seq_aln'][-1] = aln[0]
    AlnPlasmidData['UniProt_seq_aln'][-1] = aln[1]
    AlnPlasmidData['nconflicts_target_domain_region'][-1] = str(nconflicts)
    AlnPlasmidData['pctidentity_target_domain_region'][-1] = str(pctidentity)
    AlnPlasmidData['nextraneous_plasmid_residues'][-1] = str(nextraneous_plasmid_residues)
    AlnPlasmidData['matching_domainID'][-1] = str(domainID)
    AlnPlasmidData['matching_targetID'][-1] = str(targetID)

    # Generate html
    alnIDs = [UniProt_entry_name, cloneID]
    html_tree = gen_html(aln, alnIDs, additional_data=additional_data, aa_css_class_list=aa_css_class_list)

    # write html
    html_filepath = os.path.join(alignments_dirpath, cloneID + '.html')
    with open(html_filepath, 'w') as htmlfile:
        htmlfile.write(etree.tostring(html_tree, pretty_print=True))


ofile.close()

# write csv
AlnPlasmidData = pd.DataFrame(AlnPlasmidData)
AlnPlasmidData.set_index('cloneID', inplace=True)
merged = pd.concat([df, AlnPlasmidData], axis=1)
merged.to_csv('plasmid-data-aln.csv')

