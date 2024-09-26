from flask import Flask, render_template, request, redirect
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:///todo.db"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

class Todo(db.Model):
    sno = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(200), nullable=False)
    desc = db.Column(db.String(500), nullable=False)
    date_created = db.Column(db.DateTime, default=datetime.utcnow)

    def __repr__(self) -> str:
        return f"{self.sno} --- {self.title}"

@app.route('/', methods=["POST", "GET"])
def hello():
    if request.method == "POST":
        title = request.form["title"]
        desc = request.form["desc"]
        todo = Todo(title=title, desc=desc)
        db.session.add(todo)
        db.session.commit()
    
    allTodo = Todo.query.all()
    return render_template("index.html", allTodo=allTodo)
    # return "Hello World "

@app.route("/shreya")
def products():
    allTodo = Todo.query.all()
    print(allTodo)
    return "Shreya"

@app.route("/delete/<int:sno>")
def delete(sno):
    todo_to_delete = Todo.query.filter_by(sno=sno).first()
    if todo_to_delete:
        db.session.delete(todo_to_delete)
        db.session.commit()

    return redirect('/')

@app.route("/update/<int:sno>",methods=["POST", "GET"])
def update(sno):
    todo_to_upadte = Todo.query.filter_by(sno= sno).first()
    if request.method == "POST" :
        todo_to_upadte.title =request.form["title"]
        todo_to_upadte.desc  =request.form["desc"]
        db.session.commit()
        return redirect("/")
    return render_template("update.html", todo = todo_to_upadte)


if __name__ == "__main__":
    app.run(debug=True)
