import psycopg2 
import csv
#1 connect to postgres

def connect_to_postgres():
    try :
        return psycopg2.connect(dbname='postgres',
                                user='postgres',
                                password='postgres',
                                host='localhost',
                                port = 5432)
    except psycopg2.Error as e:
        print(f'Failed to connect to postgres {e}')
        return None
#2 create database
def create_pokemon_database():
    conn = connect_to_postgres()
    conn.autocommit = True #enable autocommit for db
    if conn is not None:
        try :
            cursor = conn.cursor()
            # dbname='pokemon_db'
            # cursor.execute(f'SELECT datname from pg_database where datname={dbname}')
            # existing_db = cursor.fetchone()
            # if not existing_db:
            cursor.execute('CREATE DATABASE pokemon_db')
            conn.close()
        except psycopg2.Error as e:
            print(f"Error creating or checking the database: {e}")
    
   

    
#3 connect to the database
def connect_to_pokemon_database():
    try:
        return psycopg2.connect(
        dbname="pokemon_db",
        user="postgres",
        password="postgres",
        host="localhost",
        port=5432
        )
    except psycopg2.Error as e:
        print(f"Error connecting to the Pokemon database: {e}")
        return None

    
def create_pokemon_table(conn):
    try:
        cursor = conn.cursor()
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS pokemon (
                id SERIAL PRIMARY KEY,
                name VARCHAR(255) NOT NULL,
                level INT,
                power DECIMAL(5, 2),
                is_legendary BOOLEAN
            );
        """)
        conn.commit()
    except psycopg2.Error as e:
        print(f"Failed to create the table {e}")

def insert_data_into_table(conn,csv_file):
    try:
        with open(csv_file,'r') as file:
            cursor = conn.cursor()
            reader = csv.DictReader(file)
            for row in reader:
                cursor.execute("""
                    INSERT INTO pokemon (name, level, power, is_legendary)
                    VALUES (%s, %s, %s, %s);
                """, (row['name'], int(row['level']), float(row['power']), row['is_legendary'].lower() == 'true'))
            conn.commit()
    except (psycopg2.Error,FileNotFoundError) as e:
        print(f"Error inserting data from CSV file: {e}")
        
def create_pokemon(conn, name, level, power, is_legendary):
    try :
        cur = conn.cursor()
        cur.execute("""
            INSERT INTO pokemon (name, level, power, is_legendary)
            VALUES (%s, %s, %s, %s)
            RETURNING id;
        """, (name, level, power, is_legendary))
        new_pokemon_id = cur.fetchone()[0]
        print(new_pokemon_id)
        conn.commit()
        return new_pokemon_id
    except psycopg2.Error as e:
        print(f"Error creating a new Pokemon: {e}")
        return None


def read_legendary_pokemon(conn):
    try :
        cur = conn.cursor()
        cur.execute("SELECT * FROM pokemon WHERE is_legendary = True;")
        legendary_pokemon = cur.fetchall()
        return legendary_pokemon
    except psycopg2.Error as e:
        print(f"Error reading legendary Pokemon: {e}")
        return None

# Update
def update_pokemon_level(conn, pokemon_id, new_level):
    try:
        cur = conn.cursor()
        cur.execute("UPDATE pokemon SET level = %s WHERE id = %s;", (new_level, pokemon_id))
        conn.commit()
    except psycopg2.Error as e:
        print(f"Error updating Pokemon level: {e}")

# Delete
def delete_pokemon(conn, pokemon_id):
    try:
        cur = conn.cursor()
        cur.execute("DELETE FROM pokemon WHERE id = %s;", (pokemon_id,))
        conn.commit()
    except psycopg2.Error as e:
        print(f"Error deleting a Pokemon: {e}")
        
def truncate_table(conn):
    try:
        cursor= conn.cursor()
        cursor.execute('TRUNCATE TABLE pokemon;')
        conn.commit()
    except psycopg2.Error as e:
        print('Failed to truncate the table')
   
def display_all_pokemon(conn):
    try :
        cur = conn.cursor()
        cur.execute("SELECT * FROM pokemon;")
        all_pokemon = cur.fetchall()
        for pokemon in all_pokemon:
            print(f"ID: {pokemon[0]}, Name: {pokemon[1]}, Level: {pokemon[2]}, Power: {pokemon[3]}, Legendary: {pokemon[4]}")
    except psycopg2.Error as e:
        print(f'Failed to display data {e}')
        
        
if __name__ == '__main__':
    create_pokemon_database()
    conn = connect_to_pokemon_database()
    if conn is not None:
        create_pokemon_table(conn)
        truncate_table(conn)
        insert_data_into_table(conn,'pokemon_50.csv')
        new_pokemon=create_pokemon(conn,'Chalizard',105,65.32,'true')
        new_pokemon1=create_pokemon(conn,'Bulbasor',90,74.32,'false')
        if new_pokemon is not None:
            update_pokemon_level(conn, new_pokemon, 60)
            delete_pokemon(conn, new_pokemon1)
            # print('deleted')
        legendary_pokemon=read_legendary_pokemon(conn)
        if legendary_pokemon is not None:
            for pokemon in legendary_pokemon:
                print(pokemon)
        
        display_all_pokemon(conn)
        conn.close()
        
    

    
    
    
