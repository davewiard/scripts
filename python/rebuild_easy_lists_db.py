#!/usr/bin/env python3

import sqlite3
import time
from uuid import uuid4

PROJECT_PATH = r'/home/kawika/Projects/EasyLists/easy-lists'

CATEGORY_VALUES = (
    "Dairy"
)

LIST_VALUES = {
    "Groceries": "Weekly grocery list",
    "Travel": "Bucket list travel destinations",
}

LIST_ITEM_VALUES = {
    # groceries
    "bread": "wheat",
    "eggs": "too expensive",

    # travel
    "Japan": "Spend at least two weeks in Japan",
    "Mexico": "Travel to Mexico to scope out retirement options",
}

COLUMNS_CATEGORY = 'uid TEXT NOT NULL, name TEXT NOT NULL, sort_order INTEGER, created_timestamp INTEGER NOT NULL, modified_timestamp INTEGER NOT NULL, CONSTRAINT category_pk PRIMARY KEY (uid)'
COLUMNS_LIST = 'uid TEXT NOT NULL, name TEXT NOT NULL, notes TEXT, sort_order INTEGER, created_timestamp INTEGER NOT NULL, modified_timestamp INTEGER NOT NULL, CONSTRAINT list_pk PRIMARY KEY (uid)'
COLUMNS_LIST_ITEM = 'uid TEXT NOT NULL, list_uid TEXT NOT NULL, category_uid TEXT, name TEXT NOT NULL, quantity INTEGER, crossed_off INTEGER, notes TEXT, sort_order INTEGER, created_timestamp INTEGER NOT NULL, modified_timestamp INTEGER NOT NULL, CONSTRAINT list_item_pk PRIMARY KEY (uid), CONSTRAINT list_FK FOREIGN KEY (list_uid) REFERENCES list (uid) ON DELETE CASCADE, CONSTRAINT category_FK FOREIGN KEY (category_uid) REFERENCES category (uid)'
TABLE_NAME_CATEGORY = r'category'
TABLE_NAME_LIST = r'list'
TABLE_NAME_LIST_ITEM = r'list_item'
TIMESTAMP = int(time.time())
EASYLISTS_DB_PATH = PROJECT_PATH + r'/data/src/main/assets/easy-lists.db'

def create_table(table_name, columns):
    print('Creating table: {}'.format(table_name))
    with sqlite3.connect(EASYLISTS_DB_PATH) as conn:
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
    with sqlite3.connect(EASYLISTS_DB_PATH) as conn:
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
    with sqlite3.connect(EASYLISTS_DB_PATH) as conn:
        conn.isolation_level = None
        cur = conn.cursor()
        statement = 'DROP TABLE IF EXISTS "{}"'.format(table_name)
        try:
            cur.execute(statement)
        except conn.Error:
            print('Drop table {} failed!'.format(table_name))
            print(conn.Error)
            exit()


def insert_category_records():
    print('Inserting into table: {}'.format(TABLE_NAME_CATEGORY))
    with sqlite3.connect(EASYLISTS_DB_PATH) as conn:
        conn.isolation_level = None
        cur = conn.cursor()

        try:
            cur.execute('BEGIN')

            print(CATEGORY_VALUES)
            for name in CATEGORY_VALUES:
                statement = 'INSERT INTO category (uid, name, created_timestamp, modified_timestamp) VALUES (?, ?, ?, ?)'
                cur.execute(statement, (str(uuid4()), name, TIMESTAMP, TIMESTAMP))

            cur.execute('COMMIT')
        except conn.Error:
            print('Insert category failed!')
            print(conn.Error)
            cur.execute('ROLLBACK')



def insert_list_records():
    print('Inserting into table: {}'.format(TABLE_NAME_LIST))
    with sqlite3.connect(EASYLISTS_DB_PATH) as conn:
        conn.isolation_level = None
        cur = conn.cursor()

        try:
            cur.execute('BEGIN')

            for key in LIST_VALUES.keys():
                name = key
                notes = LIST_VALUES[key]
            
                statement = 'INSERT INTO list (uid, name, notes, created_timestamp, modified_timestamp) VALUES (?, ?, ?, ? ,?)'
                cur.execute(statement, (str(uuid4()), name, notes, TIMESTAMP, TIMESTAMP))

            cur.execute('COMMIT')
        except conn.Error:
            print('Insert list failed!')
            print(conn.Error)
            cur.execute('ROLLBACK')



def insert_list_item_records():
    print('Inserting into table: {}'.format(TABLE_NAME_LIST_ITEM))
    with sqlite3.connect(EASYLISTS_DB_PATH) as conn:
        conn.isolation_level = None
        cur = conn.cursor()

        try:
            cur.execute('SELECT uid, name FROM list')
            list_rows = cur.fetchall()
            print(list_rows)
        
            cur.execute('BEGIN')

            for key in LIST_ITEM_VALUES.keys():
                list_uid = None
                name = key
                notes = LIST_ITEM_VALUES[key]

                if name in ('bread', 'eggs'):
                    list_uid = [u for u in list_rows if u[1] == 'Groceries']

                if name in ('Japan', 'Mexico'):
                    list_uid = [u for u in list_rows if u[1] == 'Travel']

                statement = 'INSERT INTO list_item (uid, list_uid, name, notes, created_timestamp, modified_timestamp) VALUES (?, ?, ?, ?, ?, ?)'
                cur.execute(statement, (str(uuid4()), list_uid[0][0], name, notes, TIMESTAMP, TIMESTAMP))

            cur.execute('COMMIT')
        except conn.Error:
            print('Insert list item failed!')
            print(conn.Error)
            cur.execute('ROLLBACK')


if __name__ == '__main__':
    drop_table(TABLE_NAME_CATEGORY)
    create_table(TABLE_NAME_CATEGORY, COLUMNS_CATEGORY)
    insert_category_records()

    drop_table(TABLE_NAME_LIST)
    create_table(TABLE_NAME_LIST, COLUMNS_LIST)
    insert_list_records()

    drop_table(TABLE_NAME_LIST_ITEM)
    create_table(TABLE_NAME_LIST_ITEM, COLUMNS_LIST_ITEM)
    insert_list_item_records()
