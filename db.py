import sqlite3

con = sqlite3.connect('database.db')
cur = con.cursor()

def create_db():
    with con:
        con.execute("""create table if not exists users (
                        id bigint(20) NOT NULL primary key,
                        is_blocked boolean default false)""")
        con.execute("""create table if not exists channels (
                        title text NOT NULL,
                        ref text NOT NULL unique)""")
        con.execute("""create table if not exists messages (
                        id integer NOT NULL primary key,
                        user_id integer NOT NULL)""")
        con.commit()

def create_user(user_id):
    cur.execute('insert into users (id) values (?) on conflict (id) do update set is_blocked = 0 where id = (?)', (user_id, user_id))
    con.commit()

def create_channel(ref, title):
    cur.execute('insert into channels (title, ref) values (?, ?) on conflict do nothing', (title, ref))
    con.commit()

def create_message(message_id, user_id):
    con.execute('insert into messages (id, user_id) values (?, ?)', (message_id, user_id))
    con.commit()

def create_batch_messages(message_id_array: list, user_id_array: list):
    for i, j in list(zip(message_id_array, user_id_array)):
        con.execute('insert into messages (id, user_id) values (?, ?)', (i, j))
    con.commit()

def get_unblocked_users():
    return cur.execute('select id from users where is_blocked = 0').fetchall()

def get_batch_users(offset, limit):
    return cur.execute(f'select id from users where is_blocked = 0 limit {offset}, {limit}').fetchall()

def get_batch_messages(offset, limit):
    return cur.execute(f'select id, user_id from messages limit {offset}, {limit}').fetchall()

def get_channels():
    return cur.execute('select title, ref from channels').fetchall()

def get_messages():
    return con.execute('select id, user_id from messages').fetchall()

def get_count_channels():
    return con.execute('select count(*) from channels').fetchall()

def set_blocked(user_id):
    cur.execute('update users set is_blocked = 1 where id = (?)', (user_id,))
    con.commit()

def set_batch_blocked(user_id_array: list):
    for i in user_id_array:
        cur.execute('update users set is_blocked = 1 where id = (?)', (i,))
    con.commit()

def delete_channel(ref):
    cur.execute('delete from channels where ref = (?)', (ref,))
    con.commit()

def delete_channel_by_id(id):
    cur.execute('delete from channels where id = (?)', (id,))
    con.commit()

def delete_messages():
    con.execute('delete from messages')
    con.commit()

#  testing
def create_test_user(user_id):
    cur.execute('insert into users (id) values (?) ', (user_id,))

def create_test_message(id):
    con.execute('insert into messages (id, user_id) values (?, ?)', (id, id))   

def get_count_users():
    return con.execute('select count(*) from users').fetchall()

def get_count_messages():
    return con.execute('select count(*) from messages').fetchall()

def get_channels_count():
    return con.execute('select count(*) from channels').fetchall()