# %%
import sqlite3
import pandas as pd

pd.set_option('display.max_columns', 50)

# %%
liberty_jet_db = sqlite3.connect("libertyJet.db")

df = pd.read_sql('SELECT * FROM adsb', con=liberty_jet_db)
df['now'] = df['now'].astype('datetime64[ms]')
# %%
df.shape
# %%
df
# %%
