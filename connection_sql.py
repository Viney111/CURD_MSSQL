'''
@Author: Viney Khaneja
@Date: 2021-05-02 13:56
@Last Modified by: Viney Khaneja
@Last Modified time: None
@Title : CURD-Operations
'''
# Importing Module for setting connection with MSSQL
import pyodbc

print("Welcome to MSSQL Connection in Python")

server = "LAPTOP-IUMGL5A5"
database = "customer_services"
username = "LAPTOP-IUMGL5A5\Kashish Manchanda"

# Connection String for connecting MSSQL
connection_str = pyodbc.connect(
    'DRIVER={ODBC Driver 17 for SQL Server};SERVER='+server+';DATABASE='+database+';UID='+username+'; Trusted_Connection=yes;')
mycursor = connection_str.cursor()

# Reading Data from File
try:
    mycursor.execute("SELECT * FROM customer_info")
    for i in mycursor:
        print(i)
except Exception as ex:
    print(ex)
finally:
    # Closing the cursor and connection finally
    mycursor.close()
    connection_str.close()
