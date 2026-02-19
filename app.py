from flask import Flask, render_template, request, jsonify
import mysql.connector
import os

app = Flask(__name__)

# FIXED MySQL connection
db = mysql.connector.connect(
    host=os.environ.get("mysql.railway.internal"),
    user=os.environ.get("root"),
    password=os.environ.get("lgjZZsrmdBaRqCVSxZYCNIcxkwWesSBQ"),
    database=os.environ.get("railway"),
    port=int(os.environ.get("MYSQLPORT", 3306))  # default 3306
)

cursor = db.cursor(dictionary=True)


@app.route("/")
def home():
    return render_template("index.html")


@app.route("/send", methods=["POST"])
def send():

    data = request.get_json()

    sql = "INSERT INTO messages (sender, receiver, message) VALUES (%s,%s,%s)"

    cursor.execute(sql, (
        data["sender"],
        data["receiver"],
        data["message"]
    ))

    db.commit()

    return jsonify({"status":"ok"})


@app.route("/messages")
def messages():

    user1=request.args.get("user1")
    user2=request.args.get("user2")

    cursor.execute("""

    SELECT * FROM messages

    WHERE (sender=%s AND receiver=%s)

    OR (sender=%s AND receiver=%s)

    ORDER BY time ASC

    """,(user1,user2,user2,user1))

    return jsonify(cursor.fetchall())


if __name__ == "__main__":

    app.run(host="0.0.0.0",port=5000)

