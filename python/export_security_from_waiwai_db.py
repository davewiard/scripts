#!/usr/bin/env python3

import csv
import sqlite3
from uuid import uuid4

if __name__ == '__main__':
    with sqlite3.connect('waiwai.db') as conn:
        conn.isolation_level = None
        cur = conn.cursor()

        with open('security_202503052014.csv', 'w') as f:
            # f.write('uid,symbol,name,currency,exchange,full_exchange_name,instrument_type,regular_market_price,regular_market_time,regular_market_volume,regular_market_day_high,regular_market_day_low,chart_previous_close,previous_close,fifty_two_week_high,fifty_two_week_low,website,industry,sector,market_cap,ex_dividend_date,dividend_rate,dividend_yield,payout_ratio,beta,forward_pe,trailing_pe,ask,ask_size,bid,bid_size,long_business_summary,created_timestamp,modified_timestamp')

            try:
                cur.execute('SELECT * FROM security')
                rows = cur.fetchall()
                # rows = cur.fetchmany(10)
                for row in rows:
                    write_row = [
                        str(row[0]),
                        str(row[1]),
                        str('"' + row[2] + '"') if ',' in row[2] else str(row[2]),
                        str(row[3]),
                        str(row[4]),
                        str(row[5]),
                        str(row[6]),
                        str(row[7]),
                        str(row[8]),
                        str(row[9]),
                        str(row[10]),
                        str(row[11]),
                        str(row[12]),
                        str(row[13]),
                        str(row[14]),
                        str(row[15]),
                        str(row[16]),
                        str(row[17]),
                        str(row[18]),
                        str(row[19]),
                        str(row[20]),
                        str(row[21]),
                        str(row[22]),
                        str(row[23]),
                        str(row[24]),
                        str(row[25]),
                        str(row[26]),
                        str(row[27]),
                        str(row[28]),
                        str(row[29]),
                        str(row[30]),
                        str(row[31]),
                        str(row[32]),
                        str(row[33]),
                    ]
                    f.write(','.join(write_row) + "\n")
            except conn.Error:
                print('failed!')
