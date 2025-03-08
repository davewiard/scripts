#!/usr/bin/env python3

import sys
import os
import csv
import sqlite3
import time
from uuid import uuid4

PROJECT_PATH = r'/home/kawika/Projects/Waiwai/Android/waiwai-android'

EVENT_TYPE_VALUES = {
    "Buy": "Shares bought",
    "Sell": "Shares sold",
    "Dividend Received": "Dividends received from the issuer",
    "Dividend Reinvestment Program (DRIP)": "Dividends automatically reinvested into the security issuing the dividend",
}

PORTFOLIO_VALUES = ('Cryptocurrencies', 'Mutual Funds', 'Stocks & ETFs')

COLUMNS_EVENT_TYPE = 'uid TEXT NOT NULL, name TEXT NOT NULL, description TEXT NOT NULL, created_timestamp INTEGER NOT NULL, modified_timestamp INTEGER NOT NULL, CONSTRAINT event_type_pk PRIMARY KEY (uid)'
COLUMNS_PORTFOLIO = 'uid TEXT NOT NULL, name TEXT NOT NULL, created_timestamp INTEGER NOT NULL, modified_timestamp INTEGER NOT NULL, CONSTRAINT portfolio_pk PRIMARY KEY (uid)'
COLUMNS_SECURITY = 'uid TEXT NOT NULL, symbol TEXT NOT NULL, name TEXT NOT NULL, currency TEXT DEFAULT (\'USD\') NOT NULL, exchange TEXT NOT NULL, full_exchange_name TEXT, instrument_type TEXT NOT NULL, remote_fetch_timestamp INTEGER, regular_market_price TEXT, regular_market_time INTEGER, regular_market_volume TEXT, regular_market_day_high TEXT, regular_market_day_low TEXT, chart_previous_close TEXT, previous_close TEXT, fifty_two_week_high TEXT, fifty_two_week_low TEXT, website TEXT, industry TEXT, sector TEXT, market_cap TEXT, ex_dividend_date INTEGER, dividend_rate TEXT, dividend_yield TEXT, payout_ratio TEXT, beta TEXT, forward_pe TEXT, trailing_pe TEXT, ask TEXT, ask_size TEXT, bid TEXT, bid_size TEXT, long_business_summary TEXT, created_timestamp INTEGER NOT NULL, modified_timestamp INTEGER NOT NULL, CONSTRAINT security_pk PRIMARY KEY (uid)'
SECURITY_CSV_PATH = PROJECT_PATH + r'/data/database/sqliteScripts'
TABLE_NAME_EVENT_TYPE = r'event_type'
TABLE_NAME_PORTFOLIO = r'portfolio'
TABLE_NAME_PORTFOLIO_SECURITY = r'portfolio_security'
TABLE_NAME_SECURITY = r'security'
TIMESTAMP = int(time.time())
WAIWAI_DB_PATH = PROJECT_PATH + r'/data/src/main/assets/waiwai.db'

def create_table(table_name, columns):
    print('Creating table: {}'.format(table_name))
    with sqlite3.connect(WAIWAI_DB_PATH) as conn:
        conn.isolation_level = None
        cur = conn.cursor()
        statement = 'CREATE TABLE "{}" ({})'.format(table_name, columns)
        try:
            cur.execute(statement)
        except conn.Error:
            print('Create table {} failed!'.format(table_name))
            print(conn.Error)
            exit()


def delete_records(table_name, query = None):
    print('Deleting records from: {}'.format(table_name))
    with sqlite3.connect(WAIWAI_DB_PATH) as conn:
        conn.isolation_level = None
        cur = conn.cursor()
        if query != None:
            statement = 'DELETE FROM "{}" WHERE '.format(table_name, query)
        else:
            statement = 'DELETE FROM "{}"'.format(table_name)
        try:
            cur.execute(statement)
        except conn.Error:
            print('Delete from {} failed!'.format(table_name))
            print(conn.Error)
            exit()


def drop_table(table_name):
    print('Dropping table: {}'.format(table_name))
    with sqlite3.connect(WAIWAI_DB_PATH) as conn:
        conn.isolation_level = None
        cur = conn.cursor()
        statement = 'DROP TABLE IF EXISTS "{}"'.format(table_name)
        try:
            cur.execute(statement)
        except conn.Error:
            print('Drop table {} failed!'.format(table_name))
            print(conn.Error)
            exit()


def insert_event_type_records():
    print('Inserting into table: {}'.format(TABLE_NAME_EVENT_TYPE))
    with sqlite3.connect(WAIWAI_DB_PATH) as conn:
        conn.isolation_level = None
        cur = conn.cursor()

        try:
            cur.execute('BEGIN')

            for key in EVENT_TYPE_VALUES.keys():
                uid = uuid4()
                name = key
                description = EVENT_TYPE_VALUES[key]

                statement = 'INSERT INTO event_type (uid, name, description, created_timestamp, modified_timestamp) VALUES (?, ?, ?, ? ,?)'
                cur.execute(statement, (str(uid), name, description, TIMESTAMP, TIMESTAMP))

            cur.execute('COMMIT')
        except conn.Error:
            print('Insert event type failed!')
            print(conn.Error)
            cur.execute('ROLLBACK')



def insert_portfolio_records():
    print('Inserting into table: {}'.format(TABLE_NAME_PORTFOLIO))
    with sqlite3.connect(WAIWAI_DB_PATH) as conn:
        conn.isolation_level = None
        cur = conn.cursor()

        try:
            cur.execute('BEGIN')

            for name in PORTFOLIO_VALUES:
                statement = 'INSERT INTO portfolio (uid, name, created_timestamp, modified_timestamp) VALUES (?, ?, ? ,?)'
                cur.execute(statement, (str(uuid4()), name, TIMESTAMP, TIMESTAMP))

            cur.execute('COMMIT')
        except conn.Error:
            print('Insert event type failed!')
            print(conn.Error)
            cur.execute('ROLLBACK')



def insert_portfolio_security_records():
    print('Inserting into table: {}'.format(TABLE_NAME_PORTFOLIO_SECURITY))
    with sqlite3.connect(WAIWAI_DB_PATH) as conn:
        conn.isolation_level = None
        cur = conn.cursor()

        try:
            cur.execute('SELECT uid, name FROM portfolio')
            portfolio_rows = cur.fetchall()
            print(portfolio_rows)

            cur.execute("SELECT uid, symbol, created_timestamp, modified_timestamp FROM security WHERE symbol IN ('AAPL', 'ALK', 'CEG', 'QQQ', 'TSLA', 'KINAX', 'BTC-USD', 'ETH-USD', 'SOL-USD') ORDER BY symbol")
            security_rows = cur.fetchall()
            print(security_rows)

            for row in security_rows:
                portfolio = None
                uid = uuid4()
                security_uid = row[0]
                created_timestamp = TIMESTAMP
                modified_timestamp = TIMESTAMP

                if row[1] in ('BTC-USD', 'ETH-USD', 'SOL-USD'):
                    portfolio = [u for u in portfolio_rows if u[1] == 'Cryptocurrencies']

                if row[1] in ('KINAX'):
                    portfolio = [u for u in portfolio_rows if u[1] == 'Mutual Funds']

                if row[1] in ('AAPL', 'ALK', 'CEG', 'QQQ', 'TSLA'):
                    portfolio = [u for u in portfolio_rows if u[1] == 'Stocks & ETFs']

                print('----------')
                print(f'uid           = {uid}')
                print(f'security_uid  = {security_uid}')
                # if portfolio:
                portfolio_uid = portfolio[0][0]
                print(f'portfolio_uid = {portfolio_uid}')

                columns = 'uid, portfolio_uid, security_uid, created_timestamp, modified_timestamp'
                statement = 'INSERT INTO {} ({}) VALUES (?, ?, ?, ?, ?)'.format(TABLE_NAME_PORTFOLIO_SECURITY, columns)
                cur.execute(statement, (str(uid), portfolio_uid, security_uid, created_timestamp, modified_timestamp))
        except conn.Error:
            print('Insert portfolio security failed!')
            print(conn.Error)
            cur.execute('ROLLBACK')


def insert_security_records(filename):
    print('Inserting into table: {}'.format(TABLE_NAME_SECURITY))
    with sqlite3.connect(WAIWAI_DB_PATH) as conn:
        conn.isolation_level = None
        cur = conn.cursor()

        # csv_path = SECURITY_CSV_PATH + r'\\' + filename
        csv_path = os.path.join(SECURITY_CSV_PATH, filename)

        with open(csv_path) as f:
            reader = csv.reader(f, delimiter=',', quotechar='"')
            index = 0
            for row in reader:
                if index == 0:
                    cur.execute('BEGIN')

                row[2] = row[2].replace('"', '')

                columns = 'uid, symbol, name, instrument_type, exchange, created_timestamp, modified_timestamp'
                statement = 'INSERT INTO {} ({}) VALUES (?, ?, ?, ?, ?, ?, ?)'.format(TABLE_NAME_SECURITY, columns)
                try:
                    cur.execute(statement, (row[0], row[1], row[2], row[3], row[4], TIMESTAMP, TIMESTAMP))
                    if index == 1000:
                        cur.execute('COMMIT')
                        index = -1
                except conn.Error:
                    print('Insert security records failed ({})!'.format(csv_path))
                    print(conn.Error)
                    cur.execute('ROLLBACK')

                index = index + 1


if __name__ == '__main__':
    filename = sys.argv[1]

    drop_table(TABLE_NAME_EVENT_TYPE)
    create_table(TABLE_NAME_EVENT_TYPE, COLUMNS_EVENT_TYPE)
    insert_event_type_records()

    drop_table(TABLE_NAME_PORTFOLIO)
    create_table(TABLE_NAME_PORTFOLIO, COLUMNS_PORTFOLIO)
    insert_portfolio_records()

    drop_table(TABLE_NAME_SECURITY)
    create_table(TABLE_NAME_SECURITY, COLUMNS_SECURITY)
    insert_security_records(filename)

    delete_records(TABLE_NAME_PORTFOLIO_SECURITY)
    insert_portfolio_security_records()
