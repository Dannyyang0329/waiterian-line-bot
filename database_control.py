import os
import psycopg2
from dotenv import load_dotenv


def create_state_table():
    conn = psycopg2.connect(os.getenv('DB_URL', default=''), sslmode = 'require')
    cursor = conn.cursor()

    create_table_query = '''
        CREATE TABLE state_table(
            id     serial   PRIMARY KEY,
            name   VARCHAR  NOT NULL,
            state  VARCHAR  NOT NULL
        );
    '''
    cursor.execute(create_table_query)
    conn.commit()
    print("Create state table successfully")

    cursor.close()
    conn.close()


def insert_data(record, is_many):
    conn = psycopg2.connect(os.getenv('DB_URL', default=''), sslmode = 'require')
    cursor = conn.cursor()

    table_columns = '(name, state)'
    postgres_insert_query = f"""INSERT INTO state_table {table_columns} VALUES (%s,%s)"""
    cursor.execute(postgres_insert_query, record);

    if is_many:
        cursor.executemany(postgres_insert_query, record)
    else:
        cursor.execute(postgres_insert_query, record)
    print(cursor.rowcount, "Record inserted successfully into database")
    conn.commit()

    cursor.close()
    conn.close()


def select_data():
    conn = psycopg2.connect(os.getenv('DB_URL', default=''), sslmode = 'require')
    cursor = conn.cursor()

    postgres_select_query = f"""SELECT * FROM state_table"""
    cursor.execute(postgres_select_query)
    print(cursor.fetchall())

    cursor.close()
    conn.close()


def update_state(name, new_state):
    conn = psycopg2.connect(os.getenv('DB_URL', default=''), sslmode = 'require')
    cursor = conn.cursor()

    postgres_update_query = f"""UPDATE state_table set state = %s WHERE name = %s"""
    cursor.execute(postgres_update_query, (new_state, name))
    conn.commit()

    print(f"The state of 'ID {name}' is set to '{new_state}'")
    
    cursor.close()
    conn.close()


def delete_data(name):
    conn = psycopg2.connect(os.getenv('DB_URL', default=''), sslmode = 'require')
    cursor = conn.cursor()

    postgres_delete_query = f"""DELETE FROM state_table WHERE name = %s"""
    cursor.execute(postgres_delete_query, (name,))
    conn.commit()

    print(f"The data of 'ID {name}' is deleted")

    cursor.close()
    conn.close()

load_dotenv()
delete_data('my_id')
select_data()
