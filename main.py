from flask import Flask, render_template, request, url_for, redirect, jsonify
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import Column, Integer, Float, String, Boolean
from datetime import datetime

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///db.sqlite'
app.config['SQLALCHEMY_TRACK_MODIFICATION'] = False

db = SQLAlchemy(app)


@app.route("/")
def nav():
    return render_template("home.html")


@app.route("/tasks")
def create_tasks():

    # show all todos

    todo_list = TODO.query.all()
    return render_template("tasks.html", todo_list=todo_list)


class TODO(db.Model):
    __tableName__ = "To DO list"
    id = Column(Integer, primary_key=True)
    task = Column(String(100))
    complete = Column(Boolean)


# **************************** Route to add tasks ********************************
@app.route("/tasks/add_task", methods=["POST"])
def add():
    # Add items to db
    title = request.form.get('title')
    now = datetime.now()
    time = now.strftime("%H:%M:%S")
    add_todo = TODO(task=title, complete=False)
    db.session.add(add_todo)
    db.session.commit()
    return redirect(url_for("create_tasks"))


# **********************  ROUTE TO UPDATE(COMPLETE/NOT-COMPLETED) one's projects ****************************
@app.route("/tasks/update/<int:todo_id>")
def update(todo_id: int):
    # Add items to db
    todo = TODO.query.filter_by(id=todo_id).first()
    todo.complete = not todo.complete
    db.session.commit()
    return redirect(url_for("create_tasks"))


# **************************** Route to delete one's tasks ********************************
@app.route("/tasks/delete/<int:todo_id>")
def delete(todo_id: int):
    # Add items to db
    todo = TODO.query.filter_by(id=todo_id).first()
    db.session.delete(todo)
    db.session.commit()
    return redirect(url_for("create_tasks"))


if __name__ == "__main__":
    db.create_all()

    app.run(debug=True)