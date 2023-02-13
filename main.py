import psycopg2
import psycopg2 as psycopg2


def create_db(conn):
    with conn.cursor() as cur:
        cur.execute("""
        DROP TABLE IF EXISTS Phone;
        DROP TABLE IF EXISTS Client;
        """)

        cur.execute("""
                CREATE TABLE IF NOT EXISTS Client(
                client_id SERIAL PRIMARY KEY,
                name VARCHAR(60) NOT NULL,
                surname VARCHAR(60) NOT NULL,
                e_mail VARCHAR(60) NOT NULL UNIQUE
                );
                """)

        cur.execute("""
                CREATE TABLE IF NOT EXISTS Phone(
                number_id SERIAL NOT NULL,
                number DECIMAL UNIQUE CHECK(number <= 99999999999),
                client_id INTEGER REFERENCES Client(client_id 
                ));
                """)
        conn.commit()


def add_client(conn, name, surname, e_mail):
    conn.execute("""
        INSERT INTO Client(name, surname, e_mail)
        VALUES(%s, %s, %s)
        RETURNING client_id, name, surname, e_mail;
        """, (name, surname, e_mail))
    print(cur.fetchone())


def add_phone(conn, client_id, number):
    conn.execute("""
        INSERT INTO Phone(client_id, number)
        VALUES(%s, %s)
        RETURNING client_id, number;
        """, (client_id, number))
    print(cur.fetchall())


def change_client(conn, client_id, name=None, surname=None, e_mail=None):
    conn.execute("""
        UPDATE Client
        SET name=%s, surname=%s, e_mail=%s
        WHERE client_id=%s
        RETURNING client_id, name, surname, e_mail;
        """, (name, surname, e_mail, client_id))


def delete_phone(conn, client_id):
    conn.execute("""
        DELETE FROM Phone
        WHERE client_id=%s;
        """, (client_id))


def delete_client(conn, client_id):
    conn.execute("""
            DELETE FROM Phone
            WHERE client_id=%s;
            """, (client_id))

    conn.execute("""
        DELETE FROM Client
        WHERE client_id=%s;
        """, (client_id))


def find_client(conn, name=None, surname=None, e_mail=None, number=None):
    conn.execute("""
        SELECT c.name, c.surname, c.e_mail, p.number FROM Client AS c
        LEFT JOIN Phone AS p ON c.client_id = p.client_id
        WHERE c.name=%s OR c.surname=%s OR c.e_mail=%s OR p.number=%s;
        """, (name, surname, e_mail, number,))
    return cur.fetchall()


with psycopg2.connect(database="HW", user="postgres", password="880901w") as conn:
    with conn.cursor() as cur:
        create_db(conn)
        add_client(cur, 'Petr', 'Mameev', 'petr-mameev@mail.ru')
        add_client(cur, 'Andrey', 'Bobrov', 'bobr@mail.ru')
        conn.commit()
        add_phone(cur, '1', '89139139132')
        add_phone(cur, '1', '89139139133')
        add_phone(cur, '2', '89139133333')
        conn.commit()
        change_client(cur, '1', 'Andrey', 'Bobrov2', 'bobbi@mail.ru')
        conn.commit()
        delete_phone(cur, '1')
        conn.commit()
        delete_client(cur, '1')
        conn.commit()
        print(find_client(cur, '', 'Bobrov'))

conn.close()
