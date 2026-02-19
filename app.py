from flask import Flask, render_template, request, jsonify
import mysql.connector
import os

app = Flask(__name__)

# Railway MySQL connection using Environment Variables
db = mysql.connector.connect(
    host=os.environ.get("mysql.railway.internal"),
    user=os.environ.get("root"),
    password=os.environ.get("lgjZZsrmdBaRqCVSxZYCNIcxkwWesSBQ"),
    database=os.environ.get("railway"),
    port=int(os.environ.get("3306"))
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

    sender = data.get("sender")
    receiver = data.get("receiver")
    message = data.get("message")

    sql = "INSERT INTO messages (sender, receiver, message) VALUES (%s, %s, %s)"
    cursor.execute(sql, (sender, receiver, message))
    db.commit()

    return jsonify({"status": "success"})


# Get messages
@app.route("/messages", methods=["GET"])
def get_messages():

    user1 = request.args.get("user1")
    user2 = request.args.get("user2")

    sql = """
    SELECT * FROM messages
    WHERE (sender=%s AND receiver=%s)
    OR (sender=%s AND receiver=%s)
    ORDER BY time ASC
    """

    cursor.execute(sql, (user1, user2, user2, user1))

    messages = cursor.fetchall()

    return jsonify(messages)


# Run app
if __name__ == "__main__":

    port = int(os.environ.get("PORT", 5000))

    app.run(host="0.0.0.0", port=port)
