# import sqlite3


# def create_database():
#     connection = sqlite3.connect('dict.db')
#     cursor = connection.cursor()
#     cursor.execute('''
#         CREATE TABLE IF NOT EXISTS proverbs (
#             id INTEGER PRIMARY KEY,
#             Rus TEXT,
#             Lak TEXT
#         )
#     ''')
#     connection.commit()
    # connection.close()