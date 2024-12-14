# %%
from time import sleep
import requests
import sqlite3
import pandas as pd

pd.set_option('display.max_columns', 50)

cols_to_store = [
    'flight',
    'r',
    'type',
    'desc',
    'nav_qnh',
    'nav_altitude_mcp',
    'lat',
    'lon',
    'alt_baro',
    'alt_geom',
    'gs',
    'track',
    'baro_rate',
    'now'
]

# %%
while True:
    for aircraft in ['N270LE','N801PR', 'N45JE']:
        with requests.Session() as s:
            try:
                result = s.get(
                    f'https://opendata.adsb.fi/api/v2/callsign/{aircraft}'
                )
            except requests.exceptions.ConnectionError:
                print('connection error.')
                sleep(5)
        if result.status_code == 200:
            result_json = result.json()

            if result_json['ac']:
                liberty_jet_db = sqlite3.connect("libertyJet.db")

                df = pd.DataFrame(result_json['ac'])
                df.drop(
                    ['nav_modes','mlat','tisb'],
                    axis=1,
                    inplace=True,
                    errors='ignore'
                )
                df['now'] = result_json['now']
                for col in cols_to_store:
                    if col not in df.columns:
                        df[col] = None
                df[cols_to_store].to_sql('adsb', con=liberty_jet_db, if_exists='append')
                liberty_jet_db.close()
        sleep(60)