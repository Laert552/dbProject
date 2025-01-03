import sqlite3
import random

DB_NAME = "resources_mining.db"

# Функция для генерации случайных данных
def generate_random_data():
    """Генерация случайных данных для таблиц."""
    punkty = [
        {"name": "Пункт А", "kolichestvo_personala": random.randint(50, 200),
         "propusknaya_sposobnost": round(random.uniform(500, 2000), 2), "godovaya_dobycha": round(random.uniform(1000, 10000), 2)},
        {"name": "Пункт Б", "kolichestvo_personala": random.randint(50, 200),
         "propusknaya_sposobnost": round(random.uniform(500, 2000), 2), "godovaya_dobycha": round(random.uniform(1000, 10000), 2)},
        {"name": "Пункт В", "kolichestvo_personala": random.randint(50, 200),
         "propusknaya_sposobnost": round(random.uniform(500, 2000), 2), "godovaya_dobycha": round(random.uniform(1000, 10000), 2)}
    ]

    poleznye_iskopaemye = [
        {"name": "Золото", "tip": "металл", "edinitsa_izmereniya": "кг", "rynochnaya_tsena": round(random.uniform(3000, 6000), 2)},
        {"name": "Уголь", "tip": "топливо", "edinitsa_izmereniya": "тонна", "rynochnaya_tsena": round(random.uniform(50, 150), 2)},
        {"name": "Нефть", "tip": "энергия", "edinitsa_izmereniya": "баррель", "rynochnaya_tsena": round(random.uniform(60, 120), 2)}
    ]

    sposob_razrabotki = ["карьерный", "подземный", "шахтный", "буровой"]

    mestorozhdeniya = [
        {
            "name": f"Месторождение {i}",
            "sposob_razrabotki": random.choice(sposob_razrabotki),
            "zapasy": round(random.uniform(1000, 10000), 2),
            "stoimost_dobychi_ed": round(random.uniform(10, 500), 2),
            "punkt_id": random.randint(1, len(punkty)),
            "poleznoe_iskopaemoe_id": random.randint(1, len(poleznye_iskopaemye))
        }
        for i in range(1, 11)  # Генерация 10 месторождений
    ]

    return punkty, poleznye_iskopaemye, mestorozhdeniya

# Функция для вставки данных в базу
def insert_data(cursor, data, query):
    for row in data:
        # Проверяем, чтобы все значения в строке были корректными
        if all(value is not None for value in row.values()):
            cursor.execute(query, row)

# Функция для заполнения базы данных
def populate_database():
    connection = sqlite3.connect(DB_NAME)
    cursor = connection.cursor()

    # Генерация данных
    punkty, poleznye_iskopaemye, mestorozhdeniya = generate_random_data()

    # Вставка данных в таблицу Punkt
    punkt_query = """
    INSERT INTO Punkt (name, kolichestvo_personala, propusknaya_sposobnost, godovaya_dobycha)
    VALUES (:name, :kolichestvo_personala, :propusknaya_sposobnost, :godovaya_dobycha)
    """
    insert_data(cursor, punkty, punkt_query)

    # Вставка данных в таблицу Poleznoe_iskopaemoe
    iskopaemoe_query = """
    INSERT INTO Poleznoe_iskopaemoe (name, tip, edinitsa_izmereniya, rynochnaya_tsena)
    VALUES (:name, :tip, :edinitsa_izmereniya, :rynochnaya_tsena)
    """
    insert_data(cursor, poleznye_iskopaemye, iskopaemoe_query)

    # Вставка данных в таблицу Mestorozhdenie
    mestorozhdenie_query = """
    INSERT INTO Mestorozhdenie (name, sposob_razrabotki, zapasy, stoimost_dobychi_ed, punkt_id, poleznoe_iskopaemoe_id)
    VALUES (:name, :sposob_razrabotki, :zapasy, :stoimost_dobychi_ed, :punkt_id, :poleznoe_iskopaemoe_id)
    """
    insert_data(cursor, mestorozhdeniya, mestorozhdenie_query)

    # Сохранение изменений
    connection.commit()
    connection.close()
    print("База данных успешно заполнена случайными данными!")

if __name__ == "__main__":
    populate_database()
