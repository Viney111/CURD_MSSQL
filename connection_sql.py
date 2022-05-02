'''
@Author: Viney Khaneja
@Date: 2021-05-02 13:56
@Last Modified by: Viney Khaneja
@Last Modified time: None
@Title : CURD-Operations
'''
# Importing Module for setting connection with MSSQL
from email.headerregistry import Address
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


def update_data():
    """
        Description: This function is to update data in DB by taking inputs from console.
        Parameters: None
        Returns: None, Just Update DB with new records.
    """
    updated_customerID = int(
        input("Enter Customer ID for updating the record"))
    sql_query = "SELECT * FROM customer_info WHERE ID = ?"
    try:
        mycursor.execute(sql_query, updated_customerID)
        customer = mycursor.fetchall()
        for data in customer:
            Name = data[1]
            Address = data[2]
            Phone = data[3]
            Zip = data[4]
            Email = data[5]
        option = int(input(
            "Choose option for updating: \n\"1\" for Name\n\"2\" for Address\n\"3\" for Phone\n\"4\" for Phone\n\"5\" for Zip"))
        if option == 1:
            Name = input("Enter updated name: ")
        elif option == 2:
            Address = input("Enter updated Address: ")
        elif option == 3:
            Phone = int(input("Enter phone number: "))
        elif option == 4:
            Zip = int(input("Enter Zip Code: "))
        elif option == 5:
            Email = input("Enter updated mail: ")
        else:
            print("Enter valid choice")
        updated_data = [Name, Address,
                        Phone, Zip, Email, updated_customerID]
        sql_query = "UPDATE customer_info SET Name = ?,Address = ?,Phone = ?,Zip = ?,Email = ? WHERE ID = ?"
        mycursor.execute(sql_query, updated_data)
    except Exception as ex:
        print(ex)
    else:
        print("Updated Successfully")
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
    # inserting_data()
    update_data()
    reading_data()
