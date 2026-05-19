import psycopg2
from psycopg2 import Error

try:
    # 1. Estabelecer a ligação à base de dados no Floci (Porta 7001)
    connection = psycopg2.connect(
        user="admin",
        password="supersecret",
        host="127.0.0.1",
        port="7001",
        database="local_db",
    )

    cursor = connection.cursor()
    print("Connection to PostgreSQL successfully established.")

    # 2. Criar a tabela 'countries'
    create_table_query = """
    CREATE TABLE IF NOT EXISTS countries (
        id SERIAL PRIMARY KEY,
        name VARCHAR(100) NOT NULL,
        code VARCHAR(3) UNIQUE NOT NULL
    );
    """
    cursor.execute(create_table_query)
    connection.commit()
    print("Table 'countries' created or validated successfully.")

    # 3. Insert 10 countries (using %s placeholders to prevent SQL Injection)
    countries_to_insert = [
        ("Portugal", "PT"),
        ("Brasil", "BR"),
        ("Angola", "AO"),
        ("Moçambique", "MZ"),
        ("Cabo Verde", "CV"),
        ("Guiné-Bissau", "GW"),
        ("São Tomé e Príncipe", "ST"),
        ("Timor-Leste", "TL"),
        ("Espanha", "ES"),
        ("França", "FR"),
    ]

    insert_query = "INSERT INTO countries (name, code) VALUES (%s, %s) ON CONFLICT (code) DO NOTHING;"
    cursor.executemany(insert_query, countries_to_insert)
    connection.commit()
    print(f"Successfully inserted {cursor.rowcount} new countries into the database.")

    # 4. Validar a inserção fazendo um SELECT rápido
    cursor.execute("SELECT * FROM countries;")
    records = cursor.fetchall()
    print("\n--- List of countries in the database ---")
    for row in records:
        print(f"ID: {row[0]} | Name: {row[1]} | Code: {row[2]}")

except (Exception, Error) as error:
    print("Error during SQL operations:", error)

finally:
    # 5. Garantir o fecho limpo das ligações
    if "connection" in locals() and connection:
        cursor.close()
        connection.close()
        print("\nConnection to PostgreSQL closed safely.")
