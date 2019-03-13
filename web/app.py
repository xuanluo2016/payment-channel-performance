
from flask import Flask, render_template, request
from get_data import *
import json

app = Flask(__name__)


# @app.route("/,  methods=['GET', 'POST']")
@app.route("/")
def hello(name=None):
    return render_template('hello.html', name=name)

@app.route("/count", methods=['GET'])
def count():
    return str(get_count())

@app.route("/summary", methods=['GET'])
def summary(num=0):
    results = get_summary(num)
    return json.dumps(results)

@app.route("/stat", methods=['GET'])
def stat():
    results = get_stat()
    return json.dumps(results)

if __name__ == "__main__":
    
    # Save a copy of summary db whenever the summary container restarts
    file = '/data/test/data.json'
    results = get_summary_all()
    write_to_file(file, results)
    
    # Start flask application with access from localhost
    app.run(host='0.0.0.0')









