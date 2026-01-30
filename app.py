import flask
from flask import Flask, render_template
from model.repository import Repository
import os
from controllers.logbook import logbook_bp




app=flask.Flask(__name__)

repo=Repository(
    host="127.0.0.1",
    port=3306,
    user="root",
    password=os.getenv("MYSQL_PASSWORD"),
    database="journal_db",
    use_pool=True,
    pool_name="journal_pool",
    pool_size=5,
    ensure_schema=True
    )

app.register_blueprint(logbook_bp)

@app.route("/")
def home():
    return render_template('index.html')

@app.route("/calendar")
def calendar():
    return render_template('calendar.html')

@app.route("/music")
def music():
    return render_template('music.html')

@app.route("/insights")
def insights():
    return render_template('insights.html')

if __name__=="__main__":
    app.run(debug=True)


