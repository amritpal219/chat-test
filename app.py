from flask import Flask, request, jsonify, render_template
import mysql.connector

app = Flask(__name__)

# MySQL connection
db = mysql.connector.connect(
    host="localhost",
    user="root",
    password="thindworld1d",
    database="chatdb"
)

# Home page
@app.route("/")
def home():
    return render_template("index.html")


# Send message
@app.route("/send", methods=["POST"])
def send():

    data = request.json

    cursor = db.cursor()

    cursor.execute(
        "INSERT INTO messages (sender, receiver, message) VALUES (%s,%s,%s)",
        (data["sender"], data["receiver"], data["message"])
    )

    db.commit()

    return "OK"


# Get messages
@app.route("/get")
def get():

    username = request.args.get("username")

    cursor = db.cursor()

    cursor.execute(
        "SELECT sender, message FROM messages WHERE receiver=%s ORDER BY time ASC",
        (username,)
    )

    result = cursor.fetchall()

    return jsonify(result)


app.run(host="0.0.0.0", port=5000)
