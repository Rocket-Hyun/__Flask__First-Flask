import os
from flask import Flask, request, current_app
from flaskext.mysql import MySQL
import json

UPLOAD_FOLDER = os.getcwd() + "/img/"
ALLOWED_EXTENSIONS = set(['png','jpg','jpeg','gif'])
def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1] in ALLOWED_EXTENSIONS

app = Flask(__name__)
mysql = MySQL()

app.config['MYSQL_DATABASE_USER'] = ''
app.config['MYSQL_DATABASE_PASSWORD'] = ''
app.config['MYSQL_DATABASE_DB'] = ''
app.config['MYSQL_DATABASE_HOST'] = ''

mysql.init_app(app)

@app.route("/")
def helloWorld():
    return ("Hello World!")

@app.route("/loaddata", methods=["GET", "POST"])
def loadData():
    cursor = mysql.connect().cursor()
    cursor.execute("SELECT * FROM users")

    result = []
    columns = tuple([d[0] for d in cursor.description])

    # 튜플을 딕셔너리로 변경
    for row in cursor:
        result.append(dict(zip(columns, row)))

    print(result)
    return (json.dumps(result))

@app.route("/register", methods=["POST"])
def register():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        print(username)

    con = mysql.connect()
    cursor = con.cursor()
    sql = """
      INSERT INTO users (username, password) VALUES (%s, %s);
    """
    to_db = (username,password)
    cursor.execute(sql, to_db)
    con.commit()

    return ("registered!")


@app.route("/upload", methods=["POST"])
def upload():
    if request.method == 'POST':
        file = request.files['profileimg']
        path = UPLOAD_FOLDER + file.filename

    if file and allowed_file(file.filename):
        file.save(path)
        return ("ok")

@app.route("/image/<fileName>", methods=["GET"])
def loadImage(fileName):
    print("fileName:" + fileName)
    return (current_app.send_static_file(fileName))

if (__name__ == "__main__"):
    app.run(debug=True, host='0.0.0.0', port=5009)
