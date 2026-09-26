#!/usr/bin/env python3

import sqlite3
import time
from uuid import uuid4

PROJECT_PATH = r'/home/kawika/Projects/EasyLists/easy-lists-android'

# with the current INSERT function below, this array must contain at least 2 items
# Python treats an array of 1 item as just the item, not an array
CATEGORY_VALUES = (
    'Alcohol',
    'Baby',
    'Bakery',
    'Baking',
    'Beverages',
    'Bread',
    'Candy',
    'Cereal',
    'Cleaning',
    'Clothing',
    'Coffee',
    'Condiments',
    'Dairy',
    'Deli',
    'Dry Goods',
    'Electronics',
    'Frozen',
    'Furniture',
    'Household',
    'Meat',
    'Office',
    'Pasta',
    'Personal Care',
    'Pet Care',
    'Produce',
    'Rice',
    'Sauces & Oils',
    'Snacks',
    'Tea',
    'Toiletries',
)

LIST_VALUES = {
    'Groceries': 'Weekly grocery list',
    'Travel Packing': None
}

LIST_ITEM_VALUES = {
    # groceries
    'apples': 'fuji, gala',
    'bread': 'wheat',
    'butter': None,
    'eggs': None,
    'kale': None,

    # travel packing
    'Hat': 'Make sure it\'s vented',
    'Socks': None,
    'Tablet': None,
    'Toothbrush': None,
    'Toothpaste': None,
}

TAG_VALUES = (
    'Cage Free',
    'Carry-on',
    'Checked Baggage',
    'Organic',
)

USER_VALUES = [{
    'first_name': 'Kawika',
    'last_name': 'Kawika',
    'email': 'demo@easy-lists.com',
    'last_sign_in_timestamp': int(time.time()),
    'created_timestamp': int(time.time()),
    'modified_timestamp': int(time.time()),
},]

COLUMNS_CATEGORY = (
    'uid TEXT NOT NULL,'
    #'user_uid TEXT NOT NULL,'
    'name TEXT NOT NULL,'
    'sort_order INTEGER,'
    'created_timestamp INTEGER NOT NULL,'
    'modified_timestamp INTEGER NOT NULL,'
    #'CONSTRAINT category_pk PRIMARY KEY (uid),'
    #'CONSTRAINT user_FK FOREIGN KEY (user_uid) REFERENCES user (uid) ON DELETE CASCADE'
    'CONSTRAINT category_pk PRIMARY KEY (uid)'
)
COLUMNS_LIST = (
    'uid TEXT NOT NULL,'
    #'user_uid TEXT NOT NULL,'
    'name TEXT NOT NULL,'
    'notes TEXT,'
    'sort_order INTEGER,'
    'created_timestamp INTEGER NOT NULL,'
    'modified_timestamp INTEGER NOT NULL,'
    #'CONSTRAINT list_pk PRIMARY KEY (uid),'
    #'CONSTRAINT user_FK FOREIGN KEY (user_uid) REFERENCES user (uid) ON DELETE CASCADE'
    'CONSTRAINT list_pk PRIMARY KEY (uid)'
)
COLUMNS_LIST_ITEM = (
    'uid TEXT NOT NULL,'
    #'user_uid TEXT NOT NULL,'
    'list_uid TEXT NOT NULL,'
    'category_uid TEXT,'
    'name TEXT NOT NULL,'
    'quantity INTEGER,'
    'crossed_off INTEGER,'
    'crossed_off_timestamp INTEGER,'
    'notes TEXT,'
    'photo_uri TEXT,'
    'photo_offset_x REAL,'
    'photo_offset_y REAL,'
    'photo_scale REAL,'
    'sort_order INTEGER,'
    'created_timestamp INTEGER NOT NULL,'
    'modified_timestamp INTEGER NOT NULL,'
    #'CONSTRAINT list_item_pk PRIMARY KEY (uid),'
    #'CONSTRAINT list_FK FOREIGN KEY (list_uid) REFERENCES list (uid) ON DELETE CASCADE,'
    #'CONSTRAINT category_FK FOREIGN KEY (category_uid) REFERENCES category (uid),'
    #'CONSTRAINT user_FK FOREIGN KEY (user_uid) REFERENCES user (uid) ON DELETE CASCADE'
    'CONSTRAINT list_item_pk PRIMARY KEY (uid),'
    'CONSTRAINT list_FK FOREIGN KEY (list_uid) REFERENCES list (uid) ON DELETE CASCADE,'
    'CONSTRAINT category_FK FOREIGN KEY (category_uid) REFERENCES category (uid)'
)
COLUMNS_TAG = (
    'uid TEXT NOT NULL,'
    #'user_uid TEXT NOT NULL,'
    'name TEXT NOT NULL, color TEXT,'
    'created_timestamp INTEGER NOT NULL,'
    'modified_timestamp INTEGER NOT NULL,'
    #'CONSTRAINT tag_pk PRIMARY KEY (uid),'
    #'CONSTRAINT user_FK FOREIGN KEY (user_uid) REFERENCES user (uid) ON DELETE CASCADE'
    'CONSTRAINT tag_pk PRIMARY KEY (uid)'
)
COLUMNS_TAG_LIST_ITEM = (
    'uid TEXT NOT NULL,'
    #'user_uid TEXT NOT NULL,'
    'tag_uid TEXT NOT NULL,'
    'list_item_uid TEXT NOT NULL,'
    'created_timestamp INTEGER NOT NULL,'
    'modified_timestamp INTEGER NOT NULL,'
    #'CONSTRAINT tag_list_item_pk PRIMARY KEY (uid),'
    #'CONSTRAINT tag_FK FOREIGN KEY (tag_uid) REFERENCES tag(uid) ON DELETE CASCADE,'
    #'CONSTRAINT tag_list_item_list_item_FK FOREIGN KEY (list_item_uid) REFERENCES list_item(uid) ON DELETE CASCADE,'
    #'CONSTRAINT user_FK FOREIGN KEY (user_uid) REFERENCES user (uid) ON DELETE CASCADE'
    'CONSTRAINT tag_list_item_pk PRIMARY KEY (uid),'
    'CONSTRAINT tag_FK FOREIGN KEY (tag_uid) REFERENCES tag(uid) ON DELETE CASCADE,'
    'CONSTRAINT tag_list_item_list_item_FK FOREIGN KEY (list_item_uid) REFERENCES list_item(uid) ON DELETE CASCADE'
)
COLUMNS_USER = (
    'uid TEXT NOT NULL,'
    'first_name TEXT NOT NULL,'
    'last_name TEXT NOT NULL,'
    'email TEXT NOT NULL,'
    'api_key TEXT NOT NULL,'
    'last_sign_in_timestamp INTEGER NOT NULL,'
    'created_timestamp INTEGER NOT NULL,'
    'modified_timestamp INTEGER NOT NULL,'
    'CONSTRAINT user_pk PRIMARY KEY (uid)'
)
TABLE_NAME_CATEGORY = r'category'
TABLE_NAME_LIST = r'list'
TABLE_NAME_LIST_ITEM = r'list_item'
TABLE_NAME_TAG = r'tag'
TABLE_NAME_TAG_LIST_ITEM = r'tag_list_item'
TABLE_NAME_USER = r'user'
TIMESTAMP = int(time.time())
EASYLISTS_DB_PATH = PROJECT_PATH + r'/data/src/main/assets/easy-lists.db'


#region create_table()
def create_table(table_name, columns):
    print('Creating table: {}'.format(table_name))
    print('    Columns: {}'.format(columns))
    with sqlite3.connect(EASYLISTS_DB_PATH) as conn:
        conn.isolation_level = None
        cur = conn.cursor()
        statement = 'CREATE TABLE "{}" ({})'.format(table_name, columns)
        try:
            cur.execute(statement)
        except conn.Error:
            print('Create table {} failed!'.format(table_name))
            print('    statement: {}'.format(statement))
            print(str(conn.Error))
            exit()
#endregion


#region delete_records()
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
#endregion


#region drop_table()
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
#endregion


#region insert_category_records()
def insert_category_records():
    print('Inserting into table: {}'.format(TABLE_NAME_CATEGORY))
    with sqlite3.connect(EASYLISTS_DB_PATH) as conn:
        conn.isolation_level = None
        # conn.set_trace_callback(print)
        cur = conn.cursor()

        cur.execute('SELECT uid FROM user')
        user_rows = cur.fetchall()
        # print('user_rows', user_rows)

        try:
            # cur.execute('BEGIN')

            for name in CATEGORY_VALUES:
                #statement = 'INSERT INTO category (uid, user_uid, name, created_timestamp, modified_timestamp) VALUES (?, ?, ?, ?, ?)'
                #cur.execute(statement, (str(uuid4()), user_rows[0][0], name, TIMESTAMP, TIMESTAMP))
                statement = 'INSERT INTO category (uid, name, created_timestamp, modified_timestamp) VALUES (?, ?, ?, ?)'
                cur.execute(statement, (str(uuid4()), name, TIMESTAMP, TIMESTAMP))

            # cur.execute('COMMIT')
        except conn.Error:
            print('Insert category failed!')
            print(conn.Error)
            cur.execute('ROLLBACK')
#endregion


#region insert_list_records()
def insert_list_records():
    print('Inserting into table: {}'.format(TABLE_NAME_LIST))
    with sqlite3.connect(EASYLISTS_DB_PATH) as conn:
        conn.isolation_level = None
        cur = conn.cursor()

        cur.execute('SELECT uid FROM user')
        user_rows = cur.fetchall()

        try:
            cur.execute('BEGIN')

            for key in LIST_VALUES.keys():
                name = key
                notes = LIST_VALUES[key]

                #statement = 'INSERT INTO list (uid, user_uid, name, notes, created_timestamp, modified_timestamp) VALUES (?, ?, ?, ?, ?, ?)'
                #cur.execute(statement, (str(uuid4()), user_rows[0][0], name, notes, TIMESTAMP, TIMESTAMP))
                statement = 'INSERT INTO list (uid, name, notes, created_timestamp, modified_timestamp) VALUES (?, ?, ?, ?, ?)'
                cur.execute(statement, (str(uuid4()), name, notes, TIMESTAMP, TIMESTAMP))

            cur.execute('COMMIT')
        except conn.Error:
            print('Insert list failed!')
            print(conn.Error)
            cur.execute('ROLLBACK')
#endregion


#region insert_list_item_records()
def insert_list_item_records():
    print('Inserting into table: {}'.format(TABLE_NAME_LIST_ITEM))
    with sqlite3.connect(EASYLISTS_DB_PATH) as conn:
        conn.isolation_level = None
        cur = conn.cursor()

        try:
            cur.execute('SELECT uid, name FROM list')
            list_rows = cur.fetchall()

            cur.execute('SELECT uid, name FROM category')
            category_rows = cur.fetchall()

            cur.execute('SELECT uid FROM user')
            user_rows = cur.fetchall()

            cur.execute('BEGIN')

            for key in LIST_ITEM_VALUES.keys():
                category_uid = None
                crossed_off = None
                list_uid = None
                name = key
                notes = LIST_ITEM_VALUES[key]

                if name in ('apples', 'bread', 'butter', 'eggs', 'kale'):
                    list_uid = [u for u in list_rows if u[1] == 'Groceries'][0][0]
                    if name in ('apples', 'kale'):
                        category_uid = [c for c in category_rows if c[1] == 'Produce'][0][0]

                    if name in ('bread'):
                        category_uid = [c for c in category_rows if c[1] == 'Bread'][0][0]

                    if name in ('butter', 'eggs'):
                        category_uid = [c for c in category_rows if c[1] == 'Dairy'][0][0]

                if name in ('Hat', 'Socks', 'Tablet', 'Toothbrush', 'Toothpaste'):
                    list_uid = [u for u in list_rows if u[1] == 'Travel Packing'][0][0]
                    if name in ('Hat', 'Socks'):
                        category_uid = [c for c in category_rows if c[1] == 'Clothing'][0][0]

                    if name in ('Toothbrush', 'Toothpaste'):
                        category_uid = [c for c in category_rows if c[1] == 'Toiletries'][0][0]

                    if name in ('Tablet'):
                        category_uid = [c for c in category_rows if c[1] == 'Electronics'][0][0]

                if name in ('butter'):
                    crossed_off = True

                print(name, crossed_off)

                #statement = 'INSERT INTO list_item (uid, user_uid, list_uid, category_uid, name, notes, crossed_off, created_timestamp, modified_timestamp) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)'
                #cur.execute(statement, (str(uuid4()), user_rows[0][0], list_uid, category_uid, name, notes, crossed_off, TIMESTAMP, TIMESTAMP))
                statement = 'INSERT INTO list_item (uid, list_uid, category_uid, name, notes, crossed_off, created_timestamp, modified_timestamp) VALUES (?, ?, ?, ?, ?, ?, ?, ?)'
                cur.execute(statement, (str(uuid4()), list_uid, category_uid, name, notes, crossed_off, TIMESTAMP, TIMESTAMP))

            cur.execute('COMMIT')
        except conn.Error:
            print('Insert list item failed!')
            print(conn.Error)
            cur.execute('ROLLBACK')
#endregion


#region insert_tag_records()
def insert_tag_records():
    print('Inserting into table: {}'.format(TABLE_NAME_TAG))
    with sqlite3.connect(EASYLISTS_DB_PATH) as conn:
        conn.isolation_level = None
        cur = conn.cursor()

        cur.execute('SELECT uid FROM user')
        user_rows = cur.fetchall()

        try:
            cur.execute('BEGIN')

            for name in TAG_VALUES:
                #statement = 'INSERT INTO tag (uid, user_uid, name, created_timestamp, modified_timestamp) VALUES (?, ?, ?, ?, ?)'
                #cur.execute(statement, (str(uuid4()), user_rows[0][0], name, TIMESTAMP, TIMESTAMP))
                statement = 'INSERT INTO tag (uid, name, created_timestamp, modified_timestamp) VALUES (?, ?, ?, ?)'
                cur.execute(statement, (str(uuid4()), name, TIMESTAMP, TIMESTAMP))

            cur.execute('COMMIT')
        except conn.Error:
            print('Insert tag failed!')
            print(conn.Error)
            cur.execute('ROLLBACK')
#endregion


#region insert_tag_list_item_records()
def insert_tag_list_item_records():
    print('Inserting into table: {}'.format(TABLE_NAME_TAG_LIST_ITEM))
    with sqlite3.connect(EASYLISTS_DB_PATH) as conn:
        conn.isolation_level = None
        cur = conn.cursor()

        cur.execute('SELECT uid, name FROM list_item')
        list_item_rows = cur.fetchall()

        cur.execute('SELECT uid, name FROM tag')
        tag_rows = cur.fetchall()

        cur.execute('SELECT uid FROM user')
        user_rows = cur.fetchall()

        try:
            cur.execute('BEGIN')

            for list_item in list_item_rows:
                list_item_uid = list_item[0]
                list_item_name = list_item[1]
                tag_uid = None

                if list_item_name in ('apples', 'kale'):
                    tag_uid = [u for u in tag_rows if u[1] == 'Organic'][0][0]

                if list_item_name in ('eggs'):
                    tag_uid = [u for u in tag_rows if u[1] == 'Cage Free'][0][0]

                if list_item_name in ('Tablet'):
                    tag_uid = [u for u in tag_rows if u[1] == 'Carry-on'][0][0]

                if list_item_name in ('Socks', 'Toothbrush', 'Toothpaste'):
                    tag_uid = [u for u in tag_rows if u[1] == 'Checked Baggage'][0][0]

                if tag_uid != None:
                    #statement = 'INSERT INTO tag_list_item (uid, user_uid, tag_uid, list_item_uid, created_timestamp, modified_timestamp) VALUES (?, ?, ?, ?, ?, ?)'
                    #cur.execute(statement, (str(uuid4()), user_rows[0][0], tag_uid, list_item_uid, TIMESTAMP, TIMESTAMP))
                    statement = 'INSERT INTO tag_list_item (uid, tag_uid, list_item_uid, created_timestamp, modified_timestamp) VALUES (?, ?, ?, ?, ?)'
                    cur.execute(statement, (str(uuid4()), tag_uid, list_item_uid, TIMESTAMP, TIMESTAMP))

            cur.execute('COMMIT')
        except conn.Error:
            print('Insert tag list item failed!')
            print(conn.Error)
            cur.execute('ROLLBACK')
#endregion


#region insert_user_records()
def insert_user_records():
    print('Inserting into table: {}'.format(TABLE_NAME_USER))
    with sqlite3.connect(EASYLISTS_DB_PATH) as conn:
        conn.isolation_level = None
        # conn.set_trace_callback(print)
        cur = conn.cursor()

        try:
            cur.execute('BEGIN')

            for user in USER_VALUES:
                statement = 'INSERT INTO user (uid, first_name, last_name, email, api_key, last_sign_in_timestamp, created_timestamp, modified_timestamp) VALUES (?, ?, ?, ?, ?, ?, ?, ?)'
                cur.execute(statement, (str(uuid4()), user['first_name'], user['last_name'], user['email'], str(uuid4()), TIMESTAMP, TIMESTAMP, TIMESTAMP))

            cur.execute('COMMIT')
        except conn.Error:
            print('Insert user failed!')
            print(conn.Error)
            cur.execute('ROLLBACK')
#endregion


if __name__ == '__main__':
    drop_table(TABLE_NAME_USER)
    create_table(TABLE_NAME_USER, COLUMNS_USER)
    insert_user_records()
    print('')

    drop_table(TABLE_NAME_CATEGORY)
    create_table(TABLE_NAME_CATEGORY, COLUMNS_CATEGORY)
    insert_category_records()
    print('')

    drop_table(TABLE_NAME_LIST)
    create_table(TABLE_NAME_LIST, COLUMNS_LIST)
    insert_list_records()
    print('')

    drop_table(TABLE_NAME_LIST_ITEM)
    create_table(TABLE_NAME_LIST_ITEM, COLUMNS_LIST_ITEM)
    insert_list_item_records()
    print('')

    drop_table(TABLE_NAME_TAG)
    create_table(TABLE_NAME_TAG, COLUMNS_TAG)
    insert_tag_records()
    print('')

    drop_table(TABLE_NAME_TAG_LIST_ITEM)
    create_table(TABLE_NAME_TAG_LIST_ITEM, COLUMNS_TAG_LIST_ITEM)
    insert_tag_list_item_records()

    print('')
    print('Created Projects/EasyLists/easy-lists-android/data/src/main/assets/easy-lists.db')
