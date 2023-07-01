import json
import pandas as pd
import plotly.express as px
from urllib.request import urlopen

with urlopen(
        'https://gist.githubusercontent.com/carmoreira/49fd11a591e0ce2c41d36f9fa96c9b49/raw/e032a0174fc35a416cff3ef7cf1233973c018294/ukcounties.json') as response:
    counties = json.load(response)

names = []
for county in counties['features']:
    names.append(county['properties']['name'])

cols = ['tweet_id', 'date_time', 'user_id', 'sentiment_conf', 'sentiment_label', 'user_loc_toponyms',
        'user_loc_country_code', 'user_loc_state', 'user_loc_county', 'user_loc_city']

dtypes = {'user_id': 'Int64', 'user_loc_toponyms': str, 'user_loc_country_code': str, 'user_loc_state': str,
          'user_loc_county': str, 'user_loc_city': str}

df = pd.read_csv("united_kingdom_01.tsv", sep='\t', nrows=1000000, usecols=cols,
                 index_col='tweet_id', parse_dates=['date_time'])

df['county'] = pd.NA
for name in names:
    df.loc[df['user_loc_toponyms'].str.contains(name).fillna(False), ['county']] = name

df = df[df['county'].notna()]
sentiment = df[['county', 'sentiment_conf', 'sentiment_label']].groupby('county').mean()

fig = px.choropleth_mapbox(sentiment,
                           geojson=counties,
                           featureidkey='properties.name',
                           locations=sentiment.index,
                           color='sentiment_label',
                           color_continuous_scale="Viridis",
                           range_color=(-1, 0),
                           mapbox_style="carto-positron",
                           zoom=4, center={"lat": 55.3781, "lon": 3.4360},
                           opacity=0.5,
                           labels={'sent': 'sentiment'}
                           )
fig.update_layout(margin={"r": 0, "t": 0, "l": 0, "b": 0})
fig.show()
