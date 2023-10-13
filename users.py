import sqlite3
from db_manager.db_manager import (
    create_database_connection,
    create_table,
    insert_into_table,
    select_from_table,
    update_data_in_table,
    delete_from_table,
    select_from_table_by_id
)

class User():
    def __init__(self, user) -> None:
        self.name = user[1]
        self.surname = user[2]
        self.pin = user[4]
        self.active = user[3]
        self.id = user[0]

    def __str__(self) -> str:
        return f"{self.name} {self.surname}"
    

    


create_db_query = """
CREATE TABLE IF NOT EXISTS Users (
    id INTEGER PRIMARY KEY,
    Ime TEXT NOT NULL,
    Prezime TEXT NOT NULL,
    Active INTEGER,
    pin INTEGER NOT NULL UNIQUE
    
);
"""

id_search_query = """
SELECT * FROM Users WHERE id = ?;
"""

pin_search_query = """
SELECT * FROM Users WHERE pin = ?;
"""

select_all_from_db = """
SELECT * FROM Users;
"""

add_new_user_query = """
INSERT INTO Users (Ime, Prezime, Active, pin)
VALUES (?, ?, ?, ?)
"""

update_existing_user_query = """
UPDATE Users 
    SET Ime = ?,
        Prezime = ?, 
        Active = ?,
        pin = ?
WHERE id = ?;
"""

delete_user_query = """
DELETE FROM Users WHERE pin = ?;
"""
def create_db():
    connection = create_database_connection("Users.db")
    rez = create_table(connection, create_db_query)
    rezi = insert_into_table(connection, add_new_user_query, [("Goran", "Perisic", 1, 1234),])
    connection.close()

def delete_entry_from_db(pin: int):
    connection = create_database_connection("Users.db")
    delete_from_table(connection, delete_user_query, [(pin,)])
    connection.close()

def select_user(pin: int) -> User:
    connection = create_database_connection("Users.db")
    user = select_from_table_by_id(connection, pin_search_query, (pin,))
    connection.close()
    user = user[0]
    return User(user)


def save_entry_into_db(user: tuple):
    # name: str, surname: str, pin: int, active: int
    connection = create_database_connection("Users.db")
    if len(user) == 5:
        update_data_in_table(connection, update_existing_user_query, [user])
    else:
        insert_into_table(connection, add_new_user_query, [user])
    connection.close()

def select_all() -> list[User]:
    connection = create_database_connection("Users.db")
    users = select_from_table(connection, select_all_from_db)
    connection.close()
    return [User(x) for x in users]
 

def main():
    create_db()

if __name__ == "__main__":
    main()

users_list = [
    ("ADMIN", " ", "1234", "active"),
    ("Mihovil", "Nikolic", "2222", "active"),
    ("Alen", "Zuskic", "3333", "inactive"),
    ("Dorijan", "Sneler", "4444", "inactive"),
    ("Goran", "Perisic", "5555", "active"),
    ("Romina", "Flam", "6666", "inactive"),
]