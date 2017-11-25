from flask import Flask, render_template

app = Flask(__name__)

@app.route('/hello/')
@app.route('/hello/<name>')
def hello(name=None):
    name = name*2
    return render_template('index.html', username=name)


if (__name__ == "__main__"):
    app.run(debug=True, host='0.0.0.0', port=5009)