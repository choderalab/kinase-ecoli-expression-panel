Selection of PDB constructs suitable for E. coli expression
===========================================================

Description
-----------

These directories contain data generated using the script select-PDB-constructs.py.

The aim is to select construct sequences from the PDB which are likely to express well in in E. coli. Data extracted includes the expression host (from the `EXPRESSION_SYSTEM` annotation), alignment score (against the wild-type sequence), and the likely authenticity of the construct sequence. The latter feature is important because the `SEQRES` records in PDB files are frequently misannotated, usually with the resolved sequence instead of the sequence used for the experiment. The presence of terminal expression tags in the construct sequence is used as a crude measure of authenticity, since terminal expression tags are typically not resolved in crystal structures.

Manifest
--------

* `scripts/select-PDB-constructs.py`
    * selects PDB constructs based on various criteria and outputs data used to select suitable constructs for expression testing.
* `PDB_constructs-data.txt`, `PDB_constructs-data.csv`, and `PDB_constructs-data.xml`:
    * data output by the select-PDB-constructs.py script; displays various results for each target protein, including the top-ranked PDB chain and the target\_score from the database.
* `manual_exceptions.yaml`:
    * list of user-defined exceptions to be used for construct choices - this is read in by the select-PDB-constructs.py scripts and is used to downweight PDB construct sequences with known annotation errors, and in some cases to provide corrected data
* `alignments/`:
    * HTML files output by the select-PDB-constructs.py scripts; for each target protein domain which has PDB entries with the desired expression\_system annotation, an HTML file displays the sequence alignment of those PDB entries against the UniProt canonical isoform sequence, and a sequence from a plasmid library; the order of the PDB sequences is sorted based on the parameters described above.

