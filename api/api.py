import flask
from flask import request, jsonify
import sqlite3
import calendar
import time
from flask_cors import CORS, cross_origin
import os.path

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
db_path = os.path.join(BASE_DIR, "customers.db")

app = flask.Flask(__name__)
CORS(app)
app.config["DEBUG"] = True

def dict_factory(cursor, row):
    d = {}
    for idx, col in enumerate(cursor.description):
        d[col[0]] = row[idx]
    return d


@app.route('/', methods=['GET'])
def home():
    return "<h1>Customer Information Management</h1><p>This site is a prototype API for Customer Information Management.</p>"


# A route to return all of the customer information.
@app.route('/api/customer/all', methods=['GET'])
def api_get_customer_all():
    conn = sqlite3.connect(db_path)
    conn.row_factory = dict_factory
    cur = conn.cursor()
    customers = cur.execute('SELECT * FROM customers;').fetchall()

    response = flask.jsonify(customers)
    response.headers.add('Access-Control-Allow-Origin', '*')
    return response


@app.route('/api/customer', methods=['GET'])
def api_get_customer_by_id():
    # Check if an ID was provided as part of the URL.
    # If ID is provided, assign it to a variable.
    # If no ID is provided, display an error in the browser.
    if 'id' in request.args:
        id = int(request.args['id'])
    else:
        return "Error: No id field provided. Please specify an id."

    query_parameters = request.args

    id = query_parameters.get('id')

    query = "SELECT * FROM customers WHERE"
    to_filter = []

    if id:
        query += ' id=? AND'
        to_filter.append(id)

    query = query[:-4] + ';'

    conn = sqlite3.connect(db_path)
    conn.row_factory = dict_factory
    cur = conn.cursor()

    results = cur.execute(query, to_filter).fetchall()
    # Create an empty list for our results
    res = {}

    # # Loop through the data and match results that fit the requested ID.
    # # IDs are unique, but other fields might return many results
    for result in results:
        res.update(result)

    # Use the jsonify function from Flask to convert our list of
    # Python dictionaries to the JSON format.
    response = flask.jsonify(res)
    response.headers.add('Access-Control-Allow-Origin', '*')
    return response


@app.route('/api/customer/query', methods=['GET'])
def api_get_customer_by_query():

    query_parameters = request.args

    name = query_parameters.get('name', "")
    gender = query_parameters.get('gender', "")
    age = query_parameters.get('age', "")

    query = "SELECT * FROM customers WHERE"
    to_filter = []

    if name:
        query += ' name LIKE ? AND'
        to_filter.append(name)
    if gender:
        query += ' gender = ? AND'
        to_filter.append(gender)
    if age:
        query += ' age = ? AND'
        to_filter.append(age)

    query = query[:-4] + ';'

    conn = sqlite3.connect(db_path)
    conn.row_factory = dict_factory
    cur = conn.cursor()

    results = cur.execute(query, to_filter).fetchall()

    # Use the jsonify function from Flask to convert our list of
    # Python dictionaries to the JSON format.
    response = flask.jsonify(results)
    response.headers.add('Access-Control-Allow-Origin', '*')
    return response

@app.route('/api/add-customer', methods=['POST'])
@cross_origin()
def api_add_customer():
    customer = request.get_json()

    # Current GMT time in a tuple format
    current_GMT = time.gmtime()

    # now stores timestamp
    now = calendar.timegm(current_GMT)

    conn = sqlite3.connect(db_path)
    conn.row_factory = dict_factory
    cur = conn.cursor()
    cur.execute("INSERT INTO customers (name, gender, age, createdAt, updatedAt) VALUES (?, ?, ?, ?, ?)", (customer['name'], customer['gender'], customer['age'], now, now))
    conn.commit()
    
    response = "Insert successfully"
    return response

@app.route('/api/update-customer', methods=['POST'])
@cross_origin()
def api_update_customer():
    # Check if an ID was provided as part of the URL.
    # If ID is provided, assign it to a variable.
    # If no ID is provided, display an error in the browser.
    if 'id' in request.args:
        id = int(request.args['id'])
    else:
        return "Error: No id field provided. Please specify an id."

    customer = request.get_json()

    # Current GMT time in a tuple format
    current_GMT = time.gmtime()

    # now stores timestamp
    now = calendar.timegm(current_GMT)

    conn = sqlite3.connect(db_path)
    conn.row_factory = dict_factory
    cur = conn.cursor()
    cur.execute("UPDATE customers SET name = ?, gender = ?, age = ?, updatedAt = ? where id = ?", (customer['name'], customer['gender'], customer['age'], now, id))
    conn.commit()
    
    response = "Update successfully"
    return response

@app.route('/api/delete-customer', methods=['POST'])
@cross_origin()
def api_delete_customer():
    customer = request.get_json()

    conn = sqlite3.connect(db_path)
    conn.execute("DELETE from customers WHERE id = ?", (customer['id'],))
    conn.commit()
    
    response = "Delete successfully"
    return response
    

@app.errorhandler(404)
def page_not_found(e):
    return "<h1>404</h1><p>The resource could not be found.</p>", 404

app.run()