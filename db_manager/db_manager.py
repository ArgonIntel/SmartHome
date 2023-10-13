import sqlite3

# TODO: dodati docstring
def create_database_connection(db_file: str) -> sqlite3.Connection:
    try:
        connection = sqlite3.connect(db_file)
        return connection
    except sqlite3.Error as error:
        return f"Greška kod kreiranja baze podataka - {error}"
        


# TODO: dodati docstring
def create_table(connection: sqlite3.Connection, create_table_sql: str) -> bool:
    try:
        cursor = connection.cursor()
        cursor.execute(create_table_sql)
        connection.commit()
        cursor.close()
        return True
    except sqlite3.Error as error:
        return f"Greška kod kreiranja tablice - {error}"
        


# TODO: dodati docstring
def insert_into_table(
    connection: sqlite3.Connection,
    insert_sql: str,
    data: list[tuple]
) -> bool:
    try:
        cursor = connection.cursor()

        for item in data:
            cursor.execute(insert_sql, item)

        connection.commit()

        cursor.close()
        return True
    except sqlite3.Error as error:
        return f"Greška kod umetanja u tablicu - {error}"
        
    

# TODO: dodati funkciju za select 
#         - dohvati sve i dohvati za neki ID
#         - napravit jednu f-ju ali default je dohvatit sve

#select_all = "SELECT * FROM ? WHERE ?"

def select_from_table(
        connection: sqlite3.Connection,
        select_query: str
) -> list:
    try:
        cursor = connection.cursor()
        cursor.execute(select_query)
        records = cursor.fetchall()
        cursor.close()
        return records
    except sqlite3.Error as error:
        return f"Dogodila se pogreska {error} u bazi"
    
def select_from_table_by_id(
    connection: sqlite3.Connection,
    select_query: str,
    id: tuple
) -> list:
    try:
        cursor = connection.cursor()
        cursor.execute(select_query, id)
        records = cursor.fetchall()
        cursor.close()
        return records
    except sqlite3.Error as error:
        return f"Dogodila se pogreska {error} u bazi"


# TODO: dodati funkciju za update

def update_data_in_table(
        conncetion: sqlite3.Connection,
        update_query: str,
        data: list[tuple]
) -> bool:
    
    try:
        cursor = conncetion.cursor()
        
        for item in data:
            print(f"{item} - db")
            cursor.execute(update_query, item)
        
        conncetion.commit()
        cursor.close()
        return True
    except sqlite3.Error as error:
        return f"Dogodila se pogreska {error} u bazi"



# TODO: dodati funkciju za delete

def delete_from_table(connection: sqlite3.Connection,
                      delete_query: str,
                      data: list[tuple]):
    try:
        cursor = connection.cursor()
        for item in data:
            cursor.execute(delete_query, item)
        connection.commit()
        cursor.close()

    except sqlite3.Error as error:
        return f"Dogodila se greska {error} priliko brisanja"