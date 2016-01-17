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
    * `selected-kinases-sgc_and_hip.csv` - output data for the custom selection of kinase constructs
    * `selected-kinases-sgc_and_hip.txt` - ascii table showing the selected constructs with some basic data
* `scripts/mk_spreadsheet.py`
  * generates a spreadsheet with the data required to generate primers and start an expression project
  * outputs:
    * `selected-kinases-sgc_and_hip.xlsx` - spreadsheet
    * `selected-kinases-sgc_and_hip.fa` - for each kinase, contains an alignment of the UniProt seq, the selected plasmid, and the selected constructs (if different from the plasmid)
* `scripts/mk_alignments.py`
  * generates an html alignment (in alignments/) for each kinase, containing the UniProt seq, all matching plasmids (sorted), and all PDB constructs (sorted)
* Also: Spreadsheets and other material for exploring possible construct synthesis by gen9
* `additional-constructs/`
  * A few additional constructs, mostly related to collaboration projects.
  * Mostly manually curated.
  * Used to fill in slots in the 96-kinase panel following 11 plasmid cloning failures.
* `analysis/
  * only for sets which were actually expression tested
  * includes lists of identifiers (e.g. UniProt mnemonic; HUGO gene symbol) for successfully expressed kinases
