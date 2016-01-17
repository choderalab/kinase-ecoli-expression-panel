A panel of kinase constructs for expression testing.

Manifest
--------

* `addgene_hip_sgc/`
  * addgene, HIP and SGC plasmid libraries
  * constructs chosen from PDB constructs

The above directory has a structure as follows:

* `scripts/select-kinase-constructs.py`
  * takes plasmid and PDB construct data (from ../plasmids and ../PDB-constructs), and conducts a custom ranking and filtering protocol to select a suitable panel of expression constructs
  * outputs:
    * `selected-kinases.csv` - output data
    * `selected-kinases.txt` - summary table
* `scripts/mk_spreadsheet.py`
  * generates a spreadsheet with the data required to generate primers and start an expression project
  * outputs:
    * `selected-kinases.xlsx` - spreadsheet
    * `selected-kinases.fa` - for each kinase, contains an alignment of the UniProt seq, the selected plasmid, and the selected constructs (if different from the plasmid)
    * `selected-kinases-seqs.p` - Pickle-serialized DataFrame containing data necessary for `mk_alignments.py` script
* `scripts/mk_alignments.py`
  * generates an html alignment (in alignments/) for each kinase, containing the UniProt seq, all matching plasmids (sorted), and all PDB constructs (sorted)
  * Uses `selected-kinases-seqs.p` as input
* `additional-constructs/`
  * A few additional constructs, mostly related to collaboration projects.
  * Mostly manually curated.
  * Used to fill in slots in the 96-kinase panel following 11 plasmid cloning failures.
* `results-post_expression_testing/`
  * contains spreadsheet with results of expression testing by QB3 MacroLab
  * also includes lists of identifiers (e.g. UniProt mnemonic; HUGO gene symbol) for successfully expressed kinases
