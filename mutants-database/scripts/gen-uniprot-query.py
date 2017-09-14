import os
import re
import pandas as pd

scripts_dir = os.path.abspath(os.path.dirname(__file__))
project_toplevel_dir = os.path.abspath(os.path.join(scripts_dir, '..'))

df = pd.read_csv(os.path.join(project_toplevel_dir, 'expressible_kinases.csv'))

targetids = df['targetid']

uniprot_mnemonics = [re.match('([A-Z0-9]{3,}_HUMAN)_D[0-9]', targetid).groups()[0] for targetid in targetids]

query = ' OR '.join(['mnemonic:{}'.format(uniprot_mnemonic) for uniprot_mnemonic in uniprot_mnemonics])

print(query)
