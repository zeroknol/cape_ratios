# This is a template for a Python scraper on morph.io (https://morph.io)
# including some code snippets below that you should find helpful

import scraperwiki
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
sqlite_connection.close()


# # Write out to the sqlite database using scraperwiki library
# scraperwiki.sqlite.save(unique_keys=['name'], data={"name": "susan", "occupation": "software developer"})
#
# # An arbitrary query against the database
# scraperwiki.sql.select("* from data where 'name'='peter'")

# You don't have to do things with the ScraperWiki and lxml libraries.
# You can use whatever libraries you want: https://morph.io/documentation/python
# All that matters is that your final data is written to an SQLite database
# called "data.sqlite" in the current working directory which has at least a table
# called "data".
