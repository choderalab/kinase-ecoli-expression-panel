import os
from openpyxl import load_workbook
import pandas as pd
from targetexplorer.flaskapp import models

scripts_dir = os.path.dirname(__file__)
expression_panel_kinases_workbook_filename = os.path.join(scripts_dir, '..', 'selected-kinases.xlsx')
expressible_kinases_list_filename = os.path.join(scripts_dir, '..', 'expressible_kinases.csv')
mutation_data_out_filepath = os.path.join(scripts_dir, '..', 'mutation_data.csv')
mutation_data_counts_out_filepath = os.path.join(scripts_dir, '..', 'mutation_data-counts.csv')
out_txt_filepath = os.path.join(scripts_dir, '..', 'mutation_data.txt')

expression_panel_kinases_worksheet = load_workbook(expression_panel_kinases_workbook_filename)['kinase constructs']
# 1-based
construct_aa_starts = {
    expression_panel_kinases_worksheet.range('A{0}'.format(r+2)).value: expression_panel_kinases_worksheet.range('H{0}'.format(r+2)).value for r in range(96)
}
construct_aa_ends = {
    expression_panel_kinases_worksheet.range('A{0}'.format(r+2)).value: expression_panel_kinases_worksheet.range('I{0}'.format(r+2)).value for r in range(96)
}

expressible_kinases_df = pd.read_csv(expressible_kinases_list_filename)
expressible_kinases_list_colnames = list(expressible_kinases_df.columns)
expressible_target_ids = [t for t in expressible_kinases_df['target_id']]

expressible_uniprot_domain_rows = [row for row in models.UniProtDomain.query.all() if row.target_id in expressible_target_ids]

cbioportal_mutation_table = models.CbioportalMutation.__table__
cbioportal_mutation_colnames = [c.name for c in cbioportal_mutation_table.columns]

data_dict = {colname: [] for colname in expressible_kinases_list_colnames + cbioportal_mutation_colnames + ['construct_aa_start', 'construct_aa_end']}

for uniprot_domain in expressible_uniprot_domain_rows:
    target_id = uniprot_domain.target_id
    mutation_rows = uniprot_domain.cbioportal_mutations.all()
    for mutation in mutation_rows:
        for colname in expressible_kinases_list_colnames:
            data_dict[colname].append(
                expressible_kinases_df[expressible_kinases_df['target_id'] == target_id][colname].values[0]
            )
        for colname in cbioportal_mutation_colnames:
            data_dict[colname].append(
                getattr(mutation, colname)
            )
        data_dict['construct_aa_start'].append(construct_aa_starts[target_id])
        data_dict['construct_aa_end'].append(construct_aa_ends[target_id])

df = pd.DataFrame(data_dict)

df.drop([
    'id',
    'db_entry_id',
    'cbioportal_case_id',
    'uniprot_domain_id',
    'crawl_number',
    'cbioportal_aa_change_string',
    'reference_dna_allele',
    'variant_dna_allele',
    'chromosome_index',
    'chromosome_startpos',
    'chromosome_endpos',
], axis=1, inplace=True)

out_columns = [
    'target_id',
    'conc_(ng/ul)',
    'expected_conc(mg/l)',
    'construct_aa_start',
    'construct_aa_end',
    'type',
    'oncotator_aa_pos',
    'oncotator_reference_aa',
    'oncotator_variant_aa',
    'validation_status',
    'functional_impact_score',
    'mutation_origin',
]

df.to_csv(mutation_data_out_filepath, columns=out_columns)

with open(out_txt_filepath, 'w') as out_txt_file:
    out_txt_file.write(df.to_string(columns=out_columns))

# now output another file which aggregates mutations at the same site

df['mutation_string'] = ['{}{}{}'.format(*zipped) for zipped in zip(df.oncotator_reference_aa, df.oncotator_aa_pos, df.oncotator_variant_aa)]

mut_counts_dict = {}

for df_index_row_tuple in df.iterrows():
    df_row = df_index_row_tuple[1]
    target_id = df_row.target_id
    mut_string = df_row.mutation_string
    target_mut_tuple = (target_id, mut_string)
    if target_mut_tuple in mut_counts_dict:
        mut_counts_dict[target_mut_tuple] += 1
    else:
        mut_counts_dict[target_mut_tuple] = 1

df_mut_counts_colnames = [
    'target_id',
    'mutation',
    'pos',
    'target_mut_tuple',
    'n_mutations',
    'conc_(ng/ul)',
    'expected_conc(mg/l)',
]

df_mut_counts = {colname: [] for colname in df_mut_counts_colnames}

for df_index_row_tuple in df.iterrows():
    df_row = df_index_row_tuple[1]
    target_id = df_row.target_id
    mut_string = df_row.mutation_string
    target_mut_tuple = (target_id, mut_string)

    if target_mut_tuple not in df_mut_counts['target_mut_tuple']:
        df_mut_counts['target_mut_tuple'].append(target_mut_tuple)
        df_mut_counts['target_id'].append(target_id)
        df_mut_counts['mutation'].append(mut_string)
        df_mut_counts['pos'].append(df_row['oncotator_aa_pos'])
        df_mut_counts['n_mutations'].append(mut_counts_dict[target_mut_tuple])
        df_mut_counts['conc_(ng/ul)'].append(df_row['conc_(ng/ul)'])
        df_mut_counts['expected_conc(mg/l)'].append(df_row['expected_conc(mg/l)'])

df_mut_counts = pd.DataFrame(df_mut_counts)
df_mut_counts.sort(columns=['target_id', 'n_mutations', 'pos'], ascending=[True, False, True], inplace=True)
df_mut_counts.reset_index(inplace=True)

df_mut_counts_colnames.remove('target_mut_tuple')
df_mut_counts_colnames.remove('pos')

df_mut_counts.to_csv(mutation_data_counts_out_filepath, columns=df_mut_counts_colnames)

