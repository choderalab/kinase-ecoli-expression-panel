import pandas as pd
import seaborn as sns

df = pd.read_csv('mutation_data.csv')

unique_targetids = list(set(df.targetid))

nmuts = []

for targetid in unique_targetids:
    nmuts.append(sum(df.targetid == targetid))

new_df = pd.DataFrame({
    'target': unique_targetids,
    'nmuts': nmuts,
})

g = sns.barplot('target', 'nmuts', data=new_df)

unique_targetids = [x.split('_')[0] for x in unique_targetids]
g.set_xticklabels(unique_targetids, rotation=90)

sns.plt.tight_layout()

sns.plt.savefig('barchart.jpg')
