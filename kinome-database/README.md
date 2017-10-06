## Building a kinome database for selection of human protein kinase domains for expression

Human protein kinases were selected by querying the UniProt API (query date 30 May 2014) for
any human protein with a domain containing the string "protein kinase", and which was manually
annotated and reviewed (i.e. a Swiss-Prot entry). Kinome database was built using the following parameters:

uniprot\_query\_string = 'domain:"protein kinase" AND reviewed:yes'  
uniprot\_domain\_regex = '^Protein kinase(?!; truncated)(?!; inactive)'

Data was returned by the UniProt API in XML format and contained protein sequences and relevant PDB structures, along with many other types of genomic and functional information. To select active protein kinase domains, the UniProt domain annotations were searched using the regular expression `ˆProtein kinase(?!; truncated)(?!; inactive)`, which excludes certain domains annotated "Protein kinase; truncated" and "Protein kinase; inactive". Sequences for the selected domains were then stored. The sequences were derived from the canonical isoform as determined by UniProt.
