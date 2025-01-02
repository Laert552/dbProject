import sqlite3

DB_NAME = "resources_mining.db"

CREATE_TABLES_SCRIPT = """
CREATE TABLE IF NOT EXISTS Mestorozhdenie (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL,
    sposob_razrabotki TEXT NOT NULL,
    zapasy REAL NOT NULL,
    stoimost_dobychi_ed REAL NOT NULL,
    punkt_id INTEGER NOT NULL,
    poleznoe_iskopaemoe_id INTEGER NOT NULL,
    FOREIGN KEY (punkt_id) REFERENCES Punkt (id),
    FOREIGN KEY (poleznoe_iskopaemoe_id) REFERENCES Poleznoe_iskopaemoe (id)
);
CREATE TABLE IF NOT EXISTS Punkt (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL,
    kolichestvo_personala INTEGER NOT NULL,
    propusknaya_sposobnost REAL NOT NULL,
    godovaya_dobycha REAL NOT NULL
);
CREATE TABLE IF NOT EXISTS Poleznoe_iskopaemoe (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL,
    tip TEXT NOT NULL,
    edinitsa_izmereniya TEXT NOT NULL,
    rynochnaya_tsena REAL NOT NULL
);
"""
def initialize_database():

    connection = sqlite3.connect(DB_NAME)
    cursor = connection.cursor()

    cursor.executescript(CREATE_TABLES_SCRIPT)
    print(f"База данных '{DB_NAME}' и таблицы успешно созданы!")

    connection.close()
if __name__ == "__main__":
    initialize_database()