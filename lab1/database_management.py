import psycopg2
from psycopg2 import Error

cursor = None
open_con = False
connection = None


def create_conn(dbname, user, password, host):
    pass


class DB:
    def __init__(self,
                 dbname='lab1_osn',
                 user='postgres',
                 password='123',
                 host='localhost'
                 ):
        self.cursor, self.connection, self.open_con = create_connection(dbname, user, password, host)

    def create(self, table_name, **kwargs):
        request_sql = f"CREATE TABLE {table_name}(\n\tid\tSERIAL PRIMARY KEY\n\t"
        for k, v in kwargs.items():
            request_sql += f',\n\t{str(k)}\t{str(v)}'
        request_sql += ');'
        try:
            self.cursor.execute(request_sql)
            self.connection.commit()
        except (Exception, Error) as error:
            print("Ошибка при работе с PostgresSQL", error)
            return False
        else:
            return True

    def get_name(self):
        return self.connection.get_dsn_parameters()['dbname']

    def delete(self, table_name, id_film):
        request_sql = f'DELETE FROM {table_name}\nWHERE id={id_film}'
        try:
            self.cursor.execute(request_sql)
            self.connection.commit()
        except (Exception, Error) as error:
            print("Ошибка при работе с PostgresSQL", error)
            return False
        else:
            return True

    def delete_table(self, table_name):
        request_sql = f'DROP TABLE {table_name} CASCADE;'
        try:
            self.cursor.execute(request_sql)
            self.connection.commit()
        except (Exception, Error) as error:
            print("Ошибка при работе с PostgresSQL", error)
            return False
        else:
            return True

    def get_all(self):
        request_sql = "SELECT table_name FROM information_schema.tables "
        request_sql += "WHERE table_schema NOT IN ('information_schema','pg_catalog');"
        try:
            self.cursor.execute(request_sql)
            name_db = []
            for record in self.cursor:
                name_db.append(record[0])
            self.connection.commit()
        except (Exception, Error) as error:
            print("Ошибка при работе с PostgresSQL", error)
            return []
        else:
            return name_db

    def select(self, table_name):
        request_sql = f'SELECT * FROM {table_name};'
        try:
            self.cursor.execute(request_sql)
            self.connection.commit()
        except (Exception, Error) as error:
            print("Ошибка при работе с PostgresSQL", error)
            return self.cursor.fetchall()
        else:
            return self.cursor.fetchall()

    def push(self, table_name, id_films, name, score):
        if name == '' and score != '':
            request_sql = f"UPDATE {table_name} SET score={score} WHERE id={id_films}"
        elif name != '' and score == '':
            request_sql = f"UPDATE {table_name} SET name='{name}' WHERE id={id_films}"
        else:
            request_sql = f"UPDATE {table_name} SET name='{name}', score={score} WHERE id={id_films}"
        try:
            self.cursor.execute(request_sql)
            self.connection.commit()
        except (Exception, Error) as error:
            print("Ошибка при работе с PostgresSQL", error)
            return False
        else:
            return True

    def insert(self, table_name, *args):
        request_sql = f"INSERT INTO {table_name} (name, score)\nVALUES ("
        for values in args:
            request_sql += f"'{str(values)}'"
            request_sql += ', '
        request_sql = request_sql[:-2]
        request_sql += ');'
        try:
            self.cursor.execute(request_sql)
            self.connection.commit()
        except (Exception, Error) as error:
            print("Ошибка при работе с PostgresSQL", error)
            return False
        else:
            return True

    def __del__(self):
        if self.open_con:
            try:
                self.cursor.close()
            except (Exception, Error) as error:
                print("Ошибка при работе с PostgresSQL", error)
            else:
                self.open_con = False
                return True
        else:
            print('Все подключения закрыты')


def create_connection(dbname, user, password, host):
    conn = psycopg2.connect(dbname=dbname, user=user,
                            password=password, host=host)
    return conn.cursor(), conn, True


def close_connection():
    global open_con
    if open_con:
        try:
            cursor.close()
        except:
            pass
        else:
            open_con = False
            return True
    else:
        print('Все подключения закрыты')

# def create_table(table_name, **kwargs):
#     global cursor
#     """
#     :param table_name: Имя таблицы
#     :param args:
#     :param kwargs: Название и тип
#     :return:
#     """
#     request_sql = f"CREATE TABLE {table_name}(\n\tid\tSERIAL PRIMARY KEY\n\t"
#     for k, v in kwargs.items():
#         request_sql += ',\n\t'
#         request_sql += str(k)
#         request_sql += '\t' + str(v)
#     request_sql += ');'
#     # print(request_sql)
#     try:
#         cursor.execute(request_sql)
#         connection.commit()
#     except (Exception, Error) as error:
#         print("Ошибка при работе с PostgreSQL", error)
#         return False
#     else:
#         return True
