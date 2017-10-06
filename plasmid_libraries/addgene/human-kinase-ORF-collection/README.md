## Notes

* scrape.py - script used to scrape plasmid data from addgene human kinase ORF collection website, and match against TargetExplorer XML database
    * manual\_exceptions.yaml is used to skip certain plasmids with insufficient data
    * output: plasmid-data.csv
* aln-against-UniProt-seq.py - each of the plasmids in 'plasmid-data.csv' is aligned against the matching UniProt sequence for comparison. Output is to 'plasmid-data-aln.csv', 'plasmid-data-aln.txt' (ASCII format), and 'alignments/' (pretty HTML).
    * plasmid-data-aln.csv is used for the final expression construct selection

