## Notes

* oxford sgc clones for sbs\_020513.xlsx - plasmid data spreadsheet downloaded from Source Bioscience website:
  * http://www.lifesciences.sourcebioscience.com/clone-products/mammalian/genomic-clones-others/structural-genomics-consortium-expression-clones.aspx
* extract-kinase-plasmids.py - matches spreadsheet plasmid entries against TargetExplorer XML database and outputs data to 'plasmid-data.txt' (pretty-formatted) and 'plasmid-data.csv'
* aln-against-UniProt-seq.py - each of the plasmids in 'plasmid-data.csv' is aligned against the matching UniProt sequence for comparison. Output is to 'plasmid-data-aln.csv', 'plasmid-data-aln.txt' (ASCII format), and 'alignments/' (pretty HTML).
    * plasmid-data-aln.csv is used for the final expression construct selection
