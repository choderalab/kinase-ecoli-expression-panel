from targetexplorer.cbioportal import AddCbioportalMAFData

cbpmaf = AddCbioportalMAFData('./external-data/data_mutations_extended.txt')
df = cbpmaf.maf_df
