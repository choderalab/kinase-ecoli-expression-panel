from targetexplorer.cbioportal import AddCbioportalMAFData

cbpmaf = AddCbioportalMAFData('../data_mutations_extended.txt')
df = cbpmaf.maf_df
