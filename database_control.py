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
            state  VARCHAR  NOT NULL,
            lat    FLOAT(8),
            lng    FLOAT(8),
            radius INT,
            min_p  INT,
            key_w  VARCHAR
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


def update_state(name, type, value):
    conn = psycopg2.connect(os.getenv('DB_URL', default=''), sslmode = 'require')
    cursor = conn.cursor()

    if type == 'state':
        postgres_update_query = f"""UPDATE state_table set state = %s WHERE name = %s"""
        cursor.execute(postgres_update_query, (value, name))
        conn.commit()
        print(f"The state of 'ID {name}' is set to '{value}'")
    if type == 'lat':
        postgres_update_query = f"""UPDATE state_table set lat = %s WHERE name = %s"""
        cursor.execute(postgres_update_query, (value, name))
        conn.commit()
        print(f"The lat of 'ID {name}' is set to '{value}'")
    if type == 'lng':
        postgres_update_query = f"""UPDATE state_table set lng = %s WHERE name = %s"""
        cursor.execute(postgres_update_query, (value, name))
        conn.commit()
        print(f"The lng of 'ID {name}' is set to '{value}'")
    if type == 'radius':
        postgres_update_query = f"""UPDATE state_table set radius = %s WHERE name = %s"""
        cursor.execute(postgres_update_query, (value, name))
        conn.commit()
        print(f"The radius of 'ID {name}' is set to '{value}'")
    if type == 'min_p':
        postgres_update_query = f"""UPDATE state_table set min_p = %s WHERE name = %s"""
        cursor.execute(postgres_update_query, (value, name))
        conn.commit()
        print(f"The min price of 'ID {name}' is set to '{value}'")
    if type == 'key_w':
        postgres_update_query = f"""UPDATE state_table set key_w = %s WHERE name = %s"""
        cursor.execute(postgres_update_query, (value, name))
        conn.commit()
        print(f"The keyword of 'ID {name}' is set to '{value}'")
    
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
# record = ('user', 'my_name', 'my_state')
# insert_data(record)
# update_state('Ua66deff62ba92155a59a3f1063f555b8', 'state', 'search_filter')
# update_state('Ua66deff62ba92155a59a3f1063f555b8', 'state', 'idle')
# update_state('my_name', 'lng', 122.345)
# update_state('my_name', 'radius', 1500)
# update_state('my_name', 'min_p', 2)
# update_state('my_name', 'key_w', 'beef')
# delete_data('my_name')

# print(find_data('Ua66deff62ba92155a59a3f1063f555b8')[0])
# print(type(find_data('my_name')))

# print(select_data())

