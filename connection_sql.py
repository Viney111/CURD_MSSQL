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
try:
    connection_str = pyodbc.connect(
        'DRIVER={ODBC Driver 17 for SQL Server};SERVER='+server+';DATABASE='+database+';UID='+username+'; Trusted_Connection=yes;')
    mycursor = connection_str.cursor()
except Exception as ex:
    print(ex)


def inserting_data():
    """
        Description: This function is to insert data in DB by taking inputs from console.
        Parameters: None
        Returns: None, Just Update DB with new records added.
    """
    try:
        records_list = []
        while(True):
            name = input("Enter name: ")
            address = input("Enter address details: ")
            phone = int(input("Enter phone number: "))
            zip = int(input("Enter Zip Code: "))
            email = input("Enter email Address: ")
            record = [name, address, phone, zip, email]
            records_list.append(record)
            user_choice = input(
                "Enter \"Y\" for entering more details;\n\"N\" for not entering Details")
            if user_choice.upper() == "N":
                break
        sql_query = "INSERT INTO customer_info (Name,Address,Phone,Zip,Email) VALUES (?,?,?,?,?)"
        for each_record in records_list:
            mycursor.execute(sql_query, each_record)
    except ValueError as ex:
        print("Please enter integer values for Phone and zip")
    except Exception as ex:
        print(ex)
    else:
        print("Records Inserted Successfully")
        mycursor.commit()


def reading_data():
    """
        Description: This function is to read data from DB by starting query
        Parameters: None
        Returns: None, Just Prints the records of DB in tuple form 
    """
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


if __name__ == '__main__':
    inserting_data()
    reading_data()
