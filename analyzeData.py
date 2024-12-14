# %%
import sqlite3
import pandas as pd
import geopandas as gpd

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
gdf = gpd.GeoDataFrame(
    df[['flight','desc','alt_geom','gs','track','baro_rate','squawk','lat','lon','now']], 
    geometry=gpd.points_from_xy(
        df.lon,
        df.lat
    ),
    crs="EPSG:4326"
)

gdf.rename({'flight':'Aircraft'}, axis=1, inplace=True)
# %%
gdf.explore('Aircraft', cmap='Dark2')
# %%
