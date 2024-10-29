# %%
from time import sleep
import requests
import sqlite3
import pandas as pd

pd.set_option('display.max_columns', 50)

# %%
liberty_jet_db = sqlite3.connect("libertyJet.db")

# %%
while True:
    for aircraft in ['N270LE','N801PR', 'N45JE']:
        result = requests.get(
            f'https://opendata.adsb.fi/api/v2/callsign/{aircraft}'
        )
        if result.status_code == 200:
            print(f'found {aircraft}')
            result_json = result.json()

            df = pd.DataFrame(result_json['ac'])
            df.drop(
                ['nav_modes','mlat','tisb'],
                axis=1,
                inplace=True,
                errors='ignore'
            )
            df['now'] = result_json['now']
            df.to_sql('adsb', con=liberty_jet_db, if_exists='append')
        sleep(60)