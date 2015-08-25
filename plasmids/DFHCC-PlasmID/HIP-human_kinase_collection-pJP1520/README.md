## Notes

* Mehle\_Kinase\_VS1\_pJP1520\_new\_plates.xlsx - original plasmid data spreadsheet, sent to Choderalab by QB3 MacroLab
* extract-kinase-plasmids.py - matches spreadsheet plasmid entries against TargetExplorer XML database and outputs data to 'plasmid-data.csv'
* aln-against-UniProt-seq.py - each of the plasmids in 'plasmid-data.csv' is aligned against the matching UniProt sequence for comparison. Output is to 'plasmid-data-aln.csv', 'plasmid-data-aln.txt' (ASCII format), and 'alignments/' (pretty HTML).
    * plasmid-data-aln.csv is used for the final expression construct selection

