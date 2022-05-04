'''
@Author: Viney Khaneja
@Date: 2021-05-02 13:56
@Last Modified by: Viney Khaneja
@Last Modified time: None
@Title : Implementing Views in DB
'''
# Importing Module for setting connection with MSSQL
import pyodbc
from decouple import config
print("Welcome to MSSQL Connection in Python")

server = config('server')
database = config('database2')
username = config('username')

# Connection String for connecting MSSQL
try:
    connection_str = pyodbc.connect(
        'DRIVER={ODBC Driver 17 for SQL Server};SERVER='+server+';DATABASE='+database+';UID='+username+'; Trusted_Connection=yes;')
    mycursor = connection_str.cursor()
except Exception as ex:
    print(ex)


def view_confidential_data():
    try:
        sql_view = "SELECT * FROM dbo.vw_hide_salary_data"
        mycursor.execute(sql_view)
        for item in mycursor:
            print(item)
    except Exception as ex:
        print(ex)


def view_all_data():
    try:
        sql_view = "SELECT * FROM vw_display_all_data"
        mycursor.execute(sql_view)
        for item in mycursor:
            print(item)
    except Exception as ex:
        print(ex)


if __name__ == '__main__':
    view_confidential_data()
    view_all_data()
    mycursor.close()
