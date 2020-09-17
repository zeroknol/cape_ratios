import requests
import pandas as pd
from sqlalchemy import create_engine

r = requests.get('https://www.starcapital.de/fileadmin/charts/Res_Aktienmarktbewertungen_FundamentalKZ_Tbl.php?lang=en')
j = r.json()
df = pd.DataFrame([[d['v'] for d in x['c']] for x in j['rows']], columns=[d['label'] for d in j['cols']])

engine = create_engine('sqlite:///data.sqlite', echo=True)
sqlite_connection = engine.connect()
sqlite_table = "data"
df.to_sql(sqlite_table, sqlite_connection, if_exists='replace')

# Set up views for easier exports
sqlite_connection.execute('DROP VIEW IF EXISTS "countries"')
sqlite_connection.execute('CREATE VIEW "countries" AS select * from "data" where ("Score" is not NULL) ORDER BY Score ASC limit 40')
sqlite_connection.execute('DROP VIEW IF EXISTS "regions"')
sqlite_connection.execute('CREATE VIEW "regions" AS SELECT "Country" AS "Region", "Weight", "CAPE", "PE", "PC", "PB", "PS", "DY", "RS 26W", "RS 52W" from "data" WHERE ("index" > "0") AND ("Score" IS NULL) ORDER BY "Weight DESC"')
sqlite_connection.close()