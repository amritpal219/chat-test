from flask import Flask, render_template, request, jsonify
import mysql.connector

app = Flask(__name__)

# MySQL connection (LOCAL TESTING)
db = mysql.connector.connect(
    host="127.0.0.1",
    user="root",
    password="thindworld1d",
    database="chatdb",
    port=3306
)

cursor = db.cursor(dictionary=True)

# Home page
@app.route("/")
def home():
    return render_template("index.html")


# Send message
@app.route("/send", methods=["POST"])
def send():

    data = request.get_json()

    sender = data["sender"]
    receiver = data["receiver"]
    message = data["message"]

    sql = "INSERT INTO messages (sender, receiver, message) VALUES (%s, %s, %s)"
    cursor.execute(sql, (sender, receiver, message))
    db.commit()

    return jsonify({"status": "success"})


# Get messages
@app.route("/messages")
def messages():

    user1 = request.args.get("user1")
    user2 = request.args.get("user2")

    sql = """
    SELECT * FROM messages
    WHERE (sender=%s AND receiver=%s)
    OR (sender=%s AND receiver=%s)
    ORDER BY time ASC
    """

    cursor.execute(sql, (user1, user2, user2, user1))

    result = cursor.fetchall()

    return jsonify(result)


# Run
if __name__ == "__main__":
    app.run()
