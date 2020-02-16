import os
import pandas as pd

pd.set_option('large_repr', 'truncate')

all_files = os.listdir('data/raw')
all_files2 = os.listdir('data/raw/MDataFiles_Stage1')

for f in all_files:
    try:
        data = pd.read_csv(f'data/raw/{f}')
        f = f.replace('.csv', '').lower()
        data.to_pickle(f'data/imported/{f}.pkl')
    except:
        print(f'skip file: {f}')

for f in all_files2:
    try:
        data = pd.read_csv(f'data/raw/MDataFiles_Stage1/{f}')
        f = f.replace('.csv', '').lower()
        data.to_pickle(f'data/imported/{f}.pkl')
    except:
        print(f'skip file: {f}')


