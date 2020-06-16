from flask import Flask, render_template, url_for, request, redirect

# render_template to render html
# url for to use static file in html
from flask_sqlalchemy import SQLAlchemy

from datetime import datetime

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///test.db"
# telling our db where is our db, 'sqlite:///' is relative path which says our db is in current directory.
# if pass sqlite://// then we can give the exact location where it is.
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
db = SQLAlchemy(app)  # Initialising DB

# making model
class Todo(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    content = db.Column(db.String(200), nullable=False)
    date_created = db.Column(db.DateTime, default=datetime.utcnow)

    # creating the str funtion to return the task ID
    def __repr__(self):
        return "<Task %r" % self.id


@app.route("/", methods=["POST", "GET"])
# Creating the root url with get and post method
def index():
    if request.method == "POST":
        task_content = request.form["content"]
        new_task = Todo(content=task_content)
        # Getting data from index.html form

        try:
            db.session.add(new_task)
            db.session.commit()
            return redirect("/")
        # adding and saving data to db and redirect to root url
        except:
            return "There was an issue adding your task"

    else:
        # for get Return to url and show all data.
        tasks = Todo.query.order_by(Todo.date_created).all()
        return render_template("index.html", tasks=tasks)


@app.route("/delete/<int:id>")
def delete(id):
    task_to_delete = Todo.query.get_or_404(id)
    # get data with passed if and if data with id is not available return 404

    try:
        db.session.delete(task_to_delete)
        db.session.commit()
        return redirect("/")
    except:
        return "There was a problem deleting that task"


@app.route("/update/<int:id>", methods=["GET", "POST"])
def update(id):
    task = Todo.query.get_or_404(id)

    # Get data with specfic id and update the content of it and save it back.
    if request.method == "POST":
        task.content = request.form["content"]

        try:
            db.session.commit()
            return redirect("/")
        except:
            return "There was an issue updating your task"

    else:
        return render_template("update.html", task=task)


if __name__ == "__main__":
    app.run(debug=True)
