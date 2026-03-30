CuratedBites | Server Side Dev Class Project
-
Flask REST API for restaurant discovery & review platform. Built using Python, Flask, and MySQL

Requirements
-
- Python
- MySQL

Setup
-
1. Clone repository
2. Install dependencies
   3. Using "pip install -r requirements.txt"
4. Setup MySQL DB updating config.py if necessary based on login
5. Run application
   6. Using "flask run" in the terminal

Data Flow Diagram
-
![DataFlowDiagram.png](DataFlowDiagram.png)

## Request Lifecycle
The client sends an HTTP request to the Curated Bites API, then at the Flask routing layer will match the URL and method/function to the correct blueprint handler. Which will either be: restaurants, reviews, or users. Then before any database interaction occurs the handler
will then validate the incoming data by checking that the required fields are present and the numerical values such as rating or price range will fall within the allowed ranges, and the reference foreign keys such as UserID, RestaurantID exist within the database. Which if it doesn't then validation fails and returns a 400 JSON error without having to touch the database.

But once the input is validated the handler will call the "executeQuery" function found within connection.py under the DB directory which then opens a mySQL connection, binds the user inputted values to the queries using '%s' placeholders, then executes the SQL statements.
Then the database returns a result set for reads or 'lastrowid' for inserts statements, which then Flask will serialize into JSON using jsonify(), which then returns the appropriate HTTP status code.
Although if a database error occurs at any point, it will be caught, logged on the server side, and then provide a generic 500 response which doesn't show database details to the end-user.

## Security

All of the SQL queries use parameterized statements using '%s' placeholder syntax which is supported using the 'mysql-connector-python' dependency. The user inputted values are then passed to 'cursor.execute()' and then are never concatenated into the query string directly
thus an attempted payload such as `'OR 1=1 --`, will then be treated as a literal string value rather than allowing executable SQL statements to be inputted, to stop the SQL injection attempt.
Although beyond using parameterization, all the endpoints validates its inputs before issuing any SQL query and that the required fields are present, and the numerical fields are then casted with 'int()' inside of try/except blocks which confirms weather the integer is valid in the domain, email addresses containing '@' character. 
The foreign keys are then confirmed with a preliminary `SELECT` before dependent inserts can proceed.
Lastly, global `'@app.errorhandler(RuntimeError)'` will catch the unhandled DB exceptions and then returns generic database error occurred messages to the client, so then that the MySQL error isn't displayed publicly.