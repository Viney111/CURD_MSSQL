'''
@Author: Viney Khaneja
@Date: 2021-05-03 21:56
@Last Modified by: Viney Khaneja
@Last Modified time: None
@Title : CURD-Operations in MSSQL Through FLASK API
'''

from flask import Flask, request, make_response
from flask_restful import Api
from werkzeug.exceptions import HTTPException, Aborter
import pyodbc
import json
from decouple import config

print("Welcome to MSSQL Connection in Python")
app = Flask(__name__)
api = Api(app)
server = config('server')
database = config('database1')
username = config('username')

# Connection String for connecting MSSQL
try:
    connection_str = pyodbc.connect(
        'DRIVER={ODBC Driver 17 for SQL Server};SERVER='+server+';DATABASE='+database+';UID='+username+'; Trusted_Connection=yes;')
    mycursor = connection_str.cursor()
except Exception as ex:
    print(ex)


abort = Aborter()


@app.route("/customerdata", methods=['GET'])
def get():
    """
        Description: This function is to retrieve data from Specified URL
        Parameters: None, just defined router path.
        Returns: A dictionary of requested data and response code to client
    """
    try:
        mycursor.execute("SELECT * FROM customer_info FOR JSON AUTO")
        rows = mycursor.fetchall()
        if len(rows) == 0:
            abort(403, description="No Customer Details in DB")
        rows_data = json.loads(rows[0][0])
        return make_response({"customers": rows_data}, 200)
    except Exception as ex:
        print(ex)


@app.route("/customerdata/<int:cust_id>", methods=['GET'])
def get_by_customer_id(cust_id):
    """
        Description: This function is to retrieve data of customer by ID from MSSQL DB
        Parameters: None, just defined router path.
        Returns: A dictionary of requested data and response code to client
    """
    try:
        sql_query = "SELECT * FROM customer_info WHERE ID = ? FOR JSON AUTO"
        mycursor.execute(sql_query, cust_id)
        rows = mycursor.fetchall()
        if len(rows) == 0:
            abort(404, description="ID is not valid, Please enter correct ID")
        rows_data = json.loads(rows[0][0])
        return make_response({f"customer with ID- {cust_id}": rows_data}, 200)
    except HTTPException as ex:
        return handle_exception(ex)
    except Exception as ex:
        return ex


@app.route("/customerdata/post", methods=['POST'])
def post():
    """
        Description: This function is to post data to MSSQL Database
        Parameters: None, just defined router path.
        Returns: A descriptive message of posting and response code to client
    """
    posted_data = json.loads(request.data)
    try:
        name = posted_data['Name']
        address = posted_data['Address']
        phone = posted_data['Phone']
        email = posted_data['Email']
        zip = posted_data['Zip']
        insert_stored_proc = "EXEC dbo.sp_insert_record_tblcustomerinfo ?,?,?,?,?"
        params = [name, address, phone, email, zip]
        mycursor.execute(insert_stored_proc, params)
    except Exception as ex:
        print(ex)
    else:
        mycursor.commit()
        return make_response("Posted Successfully", 201)


@app.route("/customerdata", methods=['PATCH'])
def update():
    updated_data = json.loads(request.data)
    try:
        id = updated_data['ID']
        sql_query = "SELECT * FROM customer_info WHERE ID = ? FOR JSON AUTO"
        mycursor.execute(sql_query, id)
        rows = mycursor.fetchall()
        if len(rows) == 0:
            abort(404, description="ID is not valid, Please enter correct ID")
        name = updated_data['Name']
        address = updated_data['Address']
        phone = updated_data['Phone']
        email = updated_data['Email']
        zip = updated_data['Zip']
        update_stored_proc = "EXEC dbo.sp_update_record_tblcustomerinfo ?,?,?,?,?,?"
        params = [id, name, address, phone, email, zip]
        mycursor.execute(update_stored_proc, params)
    except HTTPException as ex:
        return handle_exception(ex)
    except Exception as ex:
        print(ex)
    else:
        mycursor.commit()
        return make_response("Updated Successfully", 202)


@app.route("/customerdata/<int:cust_id>", methods=['DELETE'])
def delete(cust_id):
    """
        Description: This function is to delete data from MSSQL Database
        Parameters: Customer ID
        Returns: A descriptive message of deleting(if id exists) and response code to client
    """
    try:
        sql_query = "SELECT * FROM customer_info WHERE ID = ? FOR JSON AUTO"
        mycursor.execute(sql_query, cust_id)
        rows = mycursor.fetchall()
        if len(rows) == 0:
            abort(404, description="ID is not valid, Please enter correct ID")
        deleting_stored_proc = "EXEC dbo.sp_delete_record_tblcustomerinfo ?"
        mycursor.execute(deleting_stored_proc, cust_id)
    except HTTPException as ex:
        return handle_exception(ex)
    except Exception as ex:
        print(ex)
    else:
        mycursor.commit()
        return make_response("Deleted Successfully", 202)


@app.errorhandler(HTTPException)
def handle_exception(e):
    """
        Description: This function is to handle abort statements
        Parameters: Abort Status Code HTTP Exceptions
        Returns: Return JSON instead of HTML for HTTP errors.
    """
    response = e.get_response()
    # replace the body with JSON
    response.data = json.dumps({
        "description": e.description,
    })
    response.content_type = "application/json"
    return response


if __name__ == '__main__':
    app.run(debug=True)
