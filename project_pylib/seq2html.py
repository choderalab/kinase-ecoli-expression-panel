from lxml.builder import E

aa_css_classes = {
    'A': 'c1',   # aromatic
    'C': 'c2',   # cysteine
    'H': 'c0',   # hydrophobic
    '+': 'c5',   # positive
    '-': 'c4',   # negative
    'P': 'c7',   # polar
    '0': 'gr',   # gap
    'x': 'bl'
}

aa_types = {
    'A': 'H',   # hydrophobic
    'C': 'C',   # cysteine
    'D': '-',   # negative
    'E': '-',
    'F': 'A',   # aromatic
    'G': 'P',   # polar
    'H': '+',   # positive
    'I': 'H',
    'K': '+',
    'L': 'H',
    'M': 'H',
    'N': 'P',
    'P': 'H',
    'Q': 'P',
    'R': '+',
    'S': 'P',
    'T': 'P',
    'V': 'H',
    'W': 'A',
    'Y': 'A',
    'X': 'x',
    '-': '0',   # gap
    'x': 'x',   # UNK (unknown) - present in 3LZB
    'a': 'x',   # lower case represents conflicting residues
    'c': 'x',
    'd': 'x',
    'e': 'x',
    'f': 'x',
    'g': 'x',
    'h': 'x',
    'i': 'x',
    'k': 'x',
    'l': 'x',
    'm': 'x',
    'n': 'x',
    'p': 'x',
    'q': 'x',
    'r': 'x',
    's': 'x',
    't': 'x',
    'v': 'x',
    'w': 'x',
    'y': 'x'
}


def gen_html(aln, aln_ids, additional_data=None, aa_css_class_list=None, css_path='seqlib.css'):
    """
    Parameters
    ----------
    aln: list of str
        List of aligned sequence strings. Each sequence should be stored as a separate list element.
    aln_ids:
        Identifiers for each sequence.
    additional_data: list
        [[data_for_first_field], [data_for_second_field], ...] where data_for_first_field is of
        length len(aln). Column headers not required.
    aa_css_class_list: list
        Can be used to override the CSS classes assigned to each residue.
        Should be given as a list of lists, with shape: (len(alignment), len(alignment[0])).
    css_path:
        Path to the CSS file for these alignments.
    """
    if additional_data is None:
        additional_data = []

    html_tree = E.html(
        E.head(
            E.link()
        ),
        E.body(
            E.table(
            )
        )
    )

    html_body = html_tree.find('body')
    css_link = html_tree.find('head/link')
    css_link.set('type', 'text/css')
    css_link.set('href', css_path)
    css_link.set('rel', 'stylesheet')

    html_table = html_body.find('table')
    html_table.set('style', 'margin-bottom: 1cm; border-collapse:separate; border-spacing:15px 3px;')

    for r in range(len(aln)):
        row = E.tr()
        row.append(E.td(E.div(str(aln_ids[r]), CLASS='ali'), nowrap=''))

        for data_field in additional_data:
            if data_field[r] != None:
                row.append(E.td(E.div(str(data_field[r]), CLASS='ali'),nowrap=''))
            else:
                row.append(E.td(E.div('', CLASS='ali'), nowrap=''))

        if aa_css_class_list != None:
            if aa_css_class_list[r] != None:
                prettyseq = seq2pretty_html(aln[r], aa_css_class_list=aa_css_class_list[r])
            else:
                prettyseq = seq2pretty_html(aln[r])
        else:
            prettyseq = seq2pretty_html(aln[r])
        seq_div = E.div(id='sequence', CLASS='ali')
        seq_div.set('style', 'background-color:#dddddd;letter-spacing:-5px')
        for span in prettyseq:
            seq_div.append(span)
        row.append(E.td(seq_div, nowrap=''))
        html_table.append(row)

    return html_tree


def seq2pretty_html(seq, aa_css_class_list=None):
    """
    Pass a sequence string.
    Returns a list of lxml html spans elements, colored according to residue type.
    Use the aa_css_class_list option to pass a list of custom aa_css_classes. Must be the same length as the seq list.
    """
    if aa_css_class_list != None and len(aa_css_class_list) != len(seq):
        raise Exception('aa_css_class_list must be list of same length as seq list.')

    spans = []

    for i, aa in enumerate(seq):
        styled_aa = E.span(aa)
        aatype = aa_types[aa]
        if aa_css_class_list is None:
            aacolor = aa_css_classes[aatype]
        else:
            aacolor = aa_css_class_list[i]
        styled_aa.set('class', str(aacolor))
        spans.append(styled_aa)
    return spans


def write_css_stylesheet(filepath):
    """
    Write a CSS stylesheet containing classes with custom colors for displaying alignments.
    """
    css_text = '''.ali {
    font-family:Lucida Console,monospace;
    font-size:16px;
    font-weight:normal;
    line-height:97%;
}
.tblheader {
    font-family:Trebuchet MS, Verdana;
    letter-spacing: -0.06em;
    line-height: 96%; 
    font-size:14px;
    font-weight:normal;
}
.tc0 { color: #3e3f61; margin-right:-0.5em }
.tc1 { color: #585989 }
.tc2 { color: #7792ba }
.tc3 { color: #a1b4cc }
.tc4 { color: #b1c4dc }
.tc0bg { background: #3e3f61 }
.tc1bg { background: #585989 }
.tc2bg { background: #7792ba }
.tc3bg { background: #a1b4cc }
.tc4bg { background: #d7e4f7 }

circle.node {
    cursor: pointer;
    stroke: #3182bd;
    stroke-width: 1.5px;
}
line.link {
    fill: none;
    stroke: #9ecae1;
    stroke-width: 1.5px;
}

/* mview / multalin / tailor coloring */
.gr  { color:grey;    }
.bl  { color:black;   }
.m0  { color:blue;    }
.m1  { color:red;     }
.c0  { color:#33cc00; }
.c1  { color:#009900; }
.c2  { color:#ffff00; }
.c3  { color:#33cc00; }
.c4  { color:#cc0000; }
.c5  { color:#0033ff; }
.c6  { color:#6600cc; }
.c7  { color:#0099ff; }
.c8  { color:#666666; }
.c9  { color:#999999; }
.t0  { color:#5858a7; }
.t1  { color:#6b6b94; }
.t2  { color:#64649b; }
.t3  { color:#2121de; }
.t4  { color:#9d9d62; }
.t5  { color:#8c8c73; }
.t6  { color:#0000ff; }
.t7  { color:#4949b6; }
.t8  { color:#60609f; }
.t9  { color:#ecec13; }
.t10 { color:#b2b24d; }
.t11 { color:#4747b8; }
.t12 { color:#82827d; }
.t13 { color:#c2c23d; }
.t14 { color:#2323dc; }
.t15 { color:#4949b6; }
.t16 { color:#9d9d62; }
.t17 { color:#c0c03f; }
.t18 { color:#d3d32c; }
.t19 { color:#ffff00; }

/* charged - positive */
.pc1 { background-color:red; }
/* charged - negative */
.pc2 { background-color:blue; }
/* polar- uncharged */
.pc3 { background-color:red; }
/* special cases */
.pc4 { background-color:yellow; }
/* hydrophobic */
.pc5 { background-color:green; }
'''
    with open(filepath, 'w') as fileobj:
        fileobj.write(css_text)

