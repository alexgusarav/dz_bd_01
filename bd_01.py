import psycopg2

def create_db(conn):
    with (conn.cursor() as cur):
        cur.execute('''
        CREATE TABLE IF NOT EXISTS users(
            id SERIAL PRIMARY KEY,
            first_name VARCHAR(40),
            last_name VARCHAR(40),
            email VARCHAR(40) UNIQUE)
        ''');
        cur.execute('''
        CREATE TABLE IF NOT EXISTS user_phone(
            id SERIAL PRIMARY KEY,
            user_id INTEGER REFERENCES users(id),
            phone INTEGER UNIQUE)
        ''');
        conn.commit()

def add_client(conn, first_name, last_name, email, phones=None):
    with (conn.cursor() as cur):
        cur.execute('''
        INSERT INTO users(first_name, last_name, email) VALUES(%s, %s, %s) RETURNING id;
        ''', (first_name, last_name, email));
        user_id = (cur.fetchone()[0])
        if phones != None:
            for phone in phones:
                cur.execute('''
                INSERT INTO user_phone(user_id, phone) VALUES(%s, %s)
                ''', (user_id, phone));
            conn.commit()

def add_phone(conn, user_id, phone):
    with (conn.cursor() as cur):
        cur.execute('''
        INSERT INTO user_phone(user_id, phone) VALUES(%s, %s)
        ''', (user_id, phone));
        conn.commit()

def change_client(conn, user_id, first_name=None, last_name=None, email=None, phones=None):
    with (conn.cursor() as cur):
        if first_name != None:
            cur.execute("""
            UPDATE users SET first_name=%s WHERE id=%s;
            """, (first_name, user_id));
        if last_name != None:
            cur.execute("""
            UPDATE users SET last_name=%s WHERE id=%s;
            """, (last_name, user_id));
        if email != None:
            cur.execute("""
            UPDATE users SET email=%s WHERE id=%s;
            """, (email, user_id));
        if phones != None:
            cur.execute('''
            DELETE FROM user_phone WHERE (user_id) = %s
            ''', (user_id,));
            for phone in phones:
                cur.execute('''
                INSERT INTO user_phone(user_id, phone) VALUES(%s, %s)
                ''', (user_id, phone));
        conn.commit()

def delete_phone(conn, user_id, phone):
    with (conn.cursor() as cur):
        cur.execute('''
        DELETE FROM user_phone WHERE (user_id, phone) = (%s, %s)
        ''', (user_id, phone));
        conn.commit()

def delete_client(conn, user_id):
    with (conn.cursor() as cur):
        cur.execute('''
        DELETE FROM user_phone WHERE user_id = %s
        ''', (user_id,));
        cur.execute('''
        DELETE FROM users WHERE id = %s
        ''', (user_id,));
        conn.commit()

def find_client(conn, first_name=None, last_name=None, email=None, phone=None):
    with (conn.cursor() as cur):
        find_zapros = ''
        if first_name != None:
            find_zapros += f"first_name = '{first_name}'"
        if last_name != None:
            if find_zapros !='':
                find_zapros +=' AND '
            find_zapros += f"last_name = '{last_name}'"
        if email != None:
            if find_zapros !='':
                find_zapros +=' AND '
            find_zapros += f"email = '{email}'"
        if phone != None:
            if find_zapros !='':
                find_zapros +=' AND '
            find_zapros += f"phone = {phone}"
        cur.execute(f'''
        SELECT u.id, first_name, Last_name, email, phone FROM users u
        LEFT JOIN user_phone p ON u.id=p.user_id
        WHERE {find_zapros}''');
        print(cur.fetchall())


with psycopg2.connect(database="neo_bd_01", user="postgres", password="12345") as conn:
    #create_db(conn)
    #add_client(conn, 'jask3', 'now1', 'j2123@dd.ru', [1,2,5,7,565])
    #add_phone(conn, 1, 354)
    #delete_phone(conn, 1, 354)
    #delete_client(conn, 9)
    #find_client(conn, email='j2123@dd.ru')
    #change_client(conn, 10, phones=[3,4,6])
conn.close()