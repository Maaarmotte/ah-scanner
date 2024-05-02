import datetime
import json
import sqlite3
from content import wakfu_items

conn = sqlite3.connect('db.sqlite')

cursor = conn.cursor()
cursor.execute("select distinct session from market_entry")
rows = cursor.fetchall()

for row in rows:
    session = row[0]
    nanos = int(session[1:])
    session_timestamp = datetime.datetime.fromtimestamp(nanos / 1000000000.0).strftime('%d/%m/%Y %H:%M:%S')

    cursor = conn.cursor()
    cursor.execute("select max(timestamp) from market_entry where session = '" + session + "'")
    max_nanos = int(cursor.fetchall()[0][0])
    max_timestamp = datetime.datetime.fromtimestamp(max_nanos / 1000000000.0).strftime('%d/%m/%Y %H:%M:%S')

    print('Session: %s [%s] - [%s]' % (row[0], session_timestamp, max_timestamp))
print()

cursor = conn.cursor()
cursor.execute("select entry from market_entry")
rows = cursor.fetchall()

all_items = []
for row in rows:
    item = json.loads(row[0])
    all_items.append(item)

for item in all_items:
    if item['seller_name'] == 'Naet':
        print('%sx [%s] at %d kamas' %
              (item['raw_item']['quantity'], wakfu_items[item['raw_item']['ref_id']], item['pack_price']))
    #if item['raw_item']['ref_id'] == 23698:
    #    print(item['pack_price'])

conn.close()