import os
import psycopg2
from dotenv import load_dotenv


def create_state_table():
    conn = psycopg2.connect(os.getenv('DB_URL', default=''), sslmode = 'require')
    cursor = conn.cursor()

    create_table_query = '''
        CREATE TABLE state_table(
            id     serial   PRIMARY KEY,
            type   VARCHAR  NOT NULL,
            name   VARCHAR  NOT NULL,
            state  VARCHAR  NOT NULL
        );
    '''
    cursor.execute(create_table_query)
    conn.commit()
    print("Create state table successfully")

    cursor.close()
    conn.close()


def drop_state_table():
    conn = psycopg2.connect(os.getenv('DB_URL', default=''), sslmode = 'require')
    cursor = conn.cursor()

    drop_table_query = f"DROP TABLE state_table"
    cursor.execute(drop_table_query)
    conn.commit()
    print("Drop state table successfully")

    cursor.close()
    conn.close()



def insert_data(record):
    conn = psycopg2.connect(os.getenv('DB_URL', default=''), sslmode = 'require')
    cursor = conn.cursor()

    table_columns = '(type, name, state)'
    postgres_insert_query = f"""INSERT INTO state_table {table_columns} VALUES (%s,%s,%s)"""
    cursor.execute(postgres_insert_query, record);

    print(cursor.rowcount, "Record inserted successfully into database")
    conn.commit()

    cursor.close()
    conn.close()


def select_data():
    conn = psycopg2.connect(os.getenv('DB_URL', default=''), sslmode = 'require')
    cursor = conn.cursor()

    postgres_select_query = f"""SELECT * FROM state_table"""
    cursor.execute(postgres_select_query)

    res = cursor.fetchall()

    cursor.close()
    conn.close()

    return res


def find_data(name):
    conn = psycopg2.connect(os.getenv('DB_URL', default=''), sslmode = 'require')
    cursor = conn.cursor()

    postgres_find_query = f"""SELECT * FROM state_table WHERE name = %s"""
    cursor.execute(postgres_find_query, (name,))
    conn.commit()

    res = cursor.fetchall()
    
    cursor.close()
    conn.close()

    return res


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


# load_dotenv()
# drop_state_table()
# create_state_table()
# print(select_data())

