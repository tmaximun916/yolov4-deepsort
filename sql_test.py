import sqlite3
import logging
from flask import Flask


def create_connection(database_file):
    """ create a database connection to a SQLite database """
    conn = None
    try:
        conn = sqlite3.connect(database_file)
        return conn
    except sqlite3.Error as e:
        print(e)
    return conn


def create_table(conn, name):
    if 'temp' not in name:
        str = ' CREATE TABLE {} ( \
                name varchar(15) NOT NULL); '.format(name)
    else:
        str = " CREATE TABLE {} ( \
                name varchar(15) NOT NULL, \
                trackid INT NOT NULL ); ".format(name)
    try:
        conn.execute(str)
    except Exception:
        # logging.warning('create table error')
        pass


def insert_data(conn, table, *arg):
    """
    arg: (name, trackid)
    """
    try:
        for (name, trackid) in arg:
            str = ' insert into {} (name, trackid) values (?, ?); '.format(table)
            insert_query = [name, trackid]
    except ValueError:
        for (name) in arg:
            str = ' insert into {} (name) values (?); '.format(table)
            insert_query = [name]
    
    try:
        conn.execute(str, insert_query)
        conn.commit()
    except Exception as e:
        e = "insert operation error", e
        logging.warning(e)


def remove_data_by_id(conn, table, id):
    str = ' DELETE FROM {} WHERE rowid = ?; '.format(table)
    # str = "DELETE FROM artists_backup WHERE name LIKE '%Santana%';"

    try:
        conn.execute(str, (id,))
        conn.commit()
    except Exception:
        pass


def select_data_by_id(conn, table, past, present=""):
    cursor = conn.cursor()
    if present:
        str = "SELECT * FROM {} WHERE id BETWEEN ? AND ?".format(table)
        cursor.execute(str, (past,present,))
    else:
        str = "SELECT * FROM {} WHERE id >= ?".format(table)
        cursor.execute(str, (past,))
    rows = cursor.fetchall()
    return rows


def rows_query(conn, table, *search_condition):
    """
    arg: search condition = (column, value)
    example: WHERE column LIKE value
    """
    # row query
    if search_condition:
        try:
            for (column, name) in search_condition:
                query_str = " SELECT COUNT(*) \
                            FROM {} \
                            WHERE \
                            {} LIKE ? ".format(table, column)
                query_terms = [name]
        except ValueError:
            for (column) in search_condition:
                query_str = " SELECT COUNT(*) \
                            FROM {} \
                            WHERE \
                            {} IS NOT NULL ".format(table, column)
                query_terms = []
    else:
        query_str = " SELECT COUNT(*) \
                      FROM {} ".format(table)
        query_terms = []

    cursor = conn.execute(query_str, query_terms)
    return cursor.fetchone()[0]


def rows_query_2_conditions(conn, table, *search_condition):
    """
    arg: search condition = (column, value, column, value)
    example: WHERE column1 LIKE value1 AND column2 LIKE value2
    """
    # row query
    if search_condition:
        try:
            for (column1, value1, column2, value2) in search_condition:
                query_str = " SELECT COUNT(*) \
                            FROM {} \
                            WHERE \
                            {} LIKE ? \
                            AND \
                            {} LIKE ? ".format(table, column1, column2)
                query_terms = [value1,value2]
        except ValueError:
            logging.warning(ValueError)
            return
    else:
        query_str = " SELECT COUNT(*) \
                      FROM {} ".format(table)
        query_terms = []

    cursor = conn.execute(query_str, query_terms)
    return cursor.fetchone()[0]


def write_to_file(conn, table):
    select_all_str = ' select * from {}; '.format(table)
    cursor = conn.execute(select_all_str)

    try:
        f = open("object_count.txt", "x")
    except Exception:
        pass

    f = open("object_count.txt", "w")
    [f.write("id = {} sushi name = {} \n".format(row[0], row[1])) for row in cursor]
    f.close()


def print_data(conn, table):
    select_all_str = ' select rowid, * from {}; '.format(table)
    cursor = conn.execute(select_all_str)
    rows = cursor.fetchall()
    [print(row) for row in rows]
   

def main():
    # insert_data(conn,'outside_conveyor',('jason',1))
    # insert_data(conn,'outside_conveyor',('jason',2))
    # print(rows_query(conn, 'outside_conveyor', ('name', 'jason')))
    # create_table(conn, 'outside_conveyor') # create temporary table in database
    # print(rows_query(conn, 'outside_conveyor'))

    # cursor = conn.execute(' SELECT rowid,name,trackid FROM outside_conveyor')
    # rows = cursor.fetchall()
    # for row in rows:
    #     print(row)

    #conn = create_connection('sushi_database.db') # open connection to database
    # create_table(conn, 'all_sushi')
    # # insert_data(conn, 'test_table1', 'jason')
    # # insert_data(conn, 'test_table1', 'adam')
    # # insert_data(conn, 'test_table1', 'poleman')
    # # insert_data(conn, 'test_table2', 'jason')
    # # cursor = conn.execute('SELECT * FROM test_table1 INTERSECT SELECT * FROM test_table2')
    # cursor = conn.execute('SELECT rowid, * FROM test_table1 EXCEPT SELECT rowid, * FROM test_table2')
    # cursor = cursor.fetchall()
    # print_data(conn, 'test_table1')
    # print("====================")
    # print_data(conn, 'test_table2')
    # print("====================")
    # [print(row) for row in cursor]
    # conn.close()
    
    # import keyboard
    # while True:
    #     try:
    #         if keyboard.is_pressed('p'):
    #             print('smth')
    #             import ctypes
    #             output = ctypes.windll.user32.MessageBoxW(0,'description','title',1)
    #             if output == 1:
    #                 print('+')
    #             break
    #     except:
    #         break

    print('nth')
        

class list_class():
    database = 'sushi_database.db'
    table = 'sushi_table'
    all_sushi_list = []
    database_connection = create_connection('sushi_database.db') # open connection to database


    def __init__(self, table_name):
        logging.warning('created')
        self.table_name = table_name
        connection = create_connection(list_class.database)
        if table_name == 'kitchen_conveyor':
            connection.execute('DELETE FROM kitchen_conveyor')
            connection.commit()
        if table_name == 'outside_conveyor':
            connection.execute('DELETE FROM outside_conveyor')
            # this is taken out for testing/showing purpose
            connection.execute('DELETE FROM sushi_table')
            connection.commit()


    # when object is deleted, list is inserted into db
    def __del__(self):
        logging.warning('deleted')
        connection = create_connection(list_class.database)
        if self.table_name == 'kitchen_conveyor':
            # insert data from temp table to sushi table (sushi currently on belt)
            cursor = connection.execute('SELECT rowid, * FROM kitchen_conveyor')
            cursor = cursor.fetchall()
            [insert_data(connection, 'sushi_table', (row[1])) for row in cursor]

            cursor2 = connection.execute("SELECT rowid, name FROM sushi_table EXCEPT SELECT rowid, name FROM sushi_table WHERE name = '+add+' OR name = '-remove-'")
            cursor2 = cursor2.fetchall()

            for row in cursor2:
                try:
                    if list_class.all_sushi_list[cursor2.index(row)] == cursor2[cursor2.index(row)][1]:
                        pass
                    else:
                        list_class.all_sushi_list[cursor2.index(row)] = cursor2[cursor2.index(row)][1]
                        insert_data(connection, 'all_sushi', (cursor2[cursor2.index(row)][1]))
                except IndexError:
                    list_class.all_sushi_list.append(cursor2[cursor2.index(row)][1])
                    insert_data(connection, 'all_sushi', (cursor2[cursor2.index(row)][1]))

        if self.table_name == 'outside_conveyor':
            if rows_query(connection, 'sushi_table'):
                cursor = connection.execute("SELECT rowid, name FROM sushi_table EXCEPT SELECT rowid, name FROM sushi_table WHERE name = '+add+' OR name = '-remove-'")
                cursor = cursor.fetchall()
                cursor2 = connection.execute('SELECT rowid, name FROM outside_conveyor')
                cursor2 = cursor2.fetchall()
                difference = len(cursor) - len(cursor2)
                if difference != 0:
                    try:
                        # sushi table is bigger than outside conveyor
                        i = 0
                        while i != rows_query(connection, 'sushi_table'):
                            try:
                                # cursor[i][1] goes into popular sushi
                                if cursor[i][1] != cursor2[i][1]:
                                    insert_data(connection, 'popular_sushi', (cursor[i][1]))
                                    cursor.pop(i)
                                    i -=1
                            except IndexError:
                                insert_data(connection, 'popular_sushi', (cursor[i][1]))
                            i += 1
                    except Exception as e:
                        logging.warning(e)
                else:
                    try:
                        cursor = connection.execute('SELECT rowid, name FROM sushi_table EXCEPT SELECT rowid, name FROM outside_conveyor')
                        cursor = cursor.fetchall()
                        [insert_data(connection, 'popular_sushi', (row[1])) for row in cursor]
                    except Exception:
                        logging.warning(Exception)
                    # this 'else' is for testing/showing, under actual production, remove the 'else' portion
                    # else:
                    #     connection.execute('DELETE FROM sushi_table')
                    #     connection.commit()


if __name__ == "__main__":
    main()
        