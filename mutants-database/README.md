# kinome-mutants
Mutants of kinases successfully expressed in E coli expression panel

## Results
- `mutation_data.csv`
    - Mutation data in CSV format. 
    - The GitHub website has a nice feature for rendering CSV files, which is a good way to look at and share the data (though non-Choderalab members won't be able to access it if it is inside this private repo):
        - https://github.com/choderalab/kinome-mutants/blob/master/mutation_data.csv
- `mutation_data.txt`
    - Same data in formatted table.
- `mutation_data-counts.csv`
    - Identical mutations (in terms of amino acid position, and variant alleles) are aggregated into a single row, with a `n_mutations` column.

## Notes on reproducing the data

- `selected-kinases.xlsx`
    - Excel spreadsheet containing results for kinase expression panel
    - See `kinase-ecoli-expression-panel` repo for further details
- `expressible_kinases.csv`
    - Data extracted from `selected-kinases.xlsx`

### Generation of TargetExplorer database

Use TargetExplorer v0.3

conda config --add channels http://anaconda.org/choderalab
conda install targetexplorer=0.3

```.sh
cd database
DoraInit.py --db_name expressed_kinases
```

Generate a UniProt query string for the proteins listed in `expressible_kinases.csv`:

```.sh
python ../scripts/gen-uniprot-query.py
```

Copy the printed output, then open `project_config.yaml` in a text editor and replace the `uniprot_query` field with the generated UniProt query.

Replace the `uniprot_domain_regex` field with `^Protein kinase(?!; truncated)(?!; inactive)`.

Now we populate the database with data from UniProt and cBioPortal:

```.sh
DoraGatherUniProt.py
DoraGathercBioPortal.py
```

And add in the private CMO mutation data from a MAF file (not included in repo):

```.sh
python ../scripts/parse_maf.py
```

### Running the mutant analysis script

```.sh
# script must be run from database directory
python ../scripts/analyze_mutations.py
```

This reads in the kinases listed in `expressible_kinases.csv`, queries the database for matching mutation data, and outputs the results files described above.

