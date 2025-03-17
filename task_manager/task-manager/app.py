import os
#importing necessary functions
from datetime import datetime
from cs50 import SQL
from flask import Flask, flash, redirect, render_template, request, session,jsonify
from flask_session import Session
from werkzeug.security import check_password_hash, generate_password_hash

from helper import apology, login_required

# Configure application
app = Flask(__name__)


# Configure session to use filesystem (instead of signed cookies)
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

# Configure CS50 Library to use SQLite database
db = SQL("sqlite:///app.db")

#handling the requests for the register route
@app.route("/register",methods=["GET","POST"])
def register():
    if request.method=="POST":
        username=request.form.get("username")
        password=request.form.get("password")
        confirmation=request.form.get("confirmation")

        if not username:
            return apology("must provide username",400)
        if not password:
            return apology("must provide password",400)
        if not confirmation or confirmation!=password:
            return apology("must confirm password",400)

        rows=db.execute("SELECT * FROM users WHERE username=?",username)
        if len(rows)>0:
            return apology("username already taken",400)
        hash_password=generate_password_hash(password)

        db.execute("INSERT INTO users (username,hash) VALUES (?,?)",username,hash_password)

        flash("Registration Successfull!Please Log In.")
        return redirect("/login")
    else:
        return render_template("register.html")

@app.route("/login",methods=["GET","POST"])
def login():
    if request.method=="POST":
        username=request.form.get("username")
        password=request.form.get("password")

        if not username:
            return apology("must provide username",400)

        if not password:
            return apology("must provide password",400)

        rows=db.execute("SELECT * FROM users WHERE username=?",username)
        if len(rows)!=1 or not check_password_hash(rows[0]["hash"],password):
            return apology("Invalid Username and/or Password!",400)

        session["user_id"]=rows[0]["id"]

        flash("Login Successful!")
        return redirect("/")
    else:
        return render_template("login.html")
# logs the user out by clearing the session
@app.route("/logout")
def logout():
    session.clear()
    return redirect("/login")

@app.route("/")
@login_required
def dashboard():
    search_query=request.args.get("search","")
    filter_by=request.args.get("filter")
    filter_priority=request.args.get("priority")
    sort_order=request.args.get("sort_by")
    user_id=session["user_id"]
    task_query="SELECT * FROM tasks WHERE user_id=? AND status!='completed'"
    params=[user_id]

    if search_query:
        task_query+=f" AND title LIKE ?"
        params.append(f"%{search_query}%")
    if filter_by:
        task_query+=f" AND status=?"
        params.append(filter_by)
    if filter_priority:
        task_query+=f" AND priority=?"
        params.append(filter_priority)

    if sort_order:
        task_query+=f" ORDER by due_date {sort_order.upper()}"



    tasks = db.execute(task_query, *params)


    completed_tasks=len([task for task in tasks if task['status']=='completed'])
    pending_tasks=len([task for task in tasks if task['status']=='pending'])
    overdue_tasks=len([task for task in tasks if datetime.strptime(task['due_date'],'%Y-%m-%d')<datetime.now() and task['status']!='completed'])

    return render_template("index.html",filter_by=filter_by,filter_priority=filter_priority,sort_order=sort_order,tasks=tasks,completed=completed_tasks,pending=pending_tasks,overdue=overdue_tasks)
#Route for handling the creation of the task
@app.route("/create",methods=["GET","POST"])
@login_required
def create():
    if request.method=="POST":
        title=request.form.get("title")
        description=request.form.get("description")
        due_date=request.form.get("due_date")
        priority=request.form.get("priority","medium")


        if not title:
            return apology("must provide task title",400)
        if not description:
            return apology("must provide task description",400)
        if not due_date:
            return apology("must provide due date",400)

        db.execute("INSERT INTO tasks (title,description,due_date,priority,user_id) VALUES (?,?,?,?,?)",title,description,due_date,priority,session["user_id"])

        flash("Task Created Successfully!")

        return redirect ("/")

    else:
        return render_template("create_task.html")
#Route for editing the task using task id when the edit button is clicked in the action column of the table
@app.route("/edit/<int:task_id>",methods=["GET","POST"])
@login_required
def edit(task_id):
    task=db.execute("SELECT * FROM tasks WHERE id=? AND user_id=?",task_id,session["user_id"])

    if len(task)!=1:
        return apology("Invalid Task",400)

    task=task[0]

    if request.method=="POST":
        title=request.form.get("title")
        description=request.form.get("description")
        due_date=request.form.get("due_date")
        priority=request.form.get("priority","medium")


        db.execute("UPDATE tasks SET title=?,description=?,due_date=?,priority=? WHERE id=? AND user_id=?",title,description,due_date,priority,task_id,session["user_id"])

        flash("Task Updated Successfully!")
        return redirect("/")

    else:
        return render_template("edit_task.html",task=task)
#This route would be used to delete the task from the dashboard table
@app.route("/delete/<int:task_id>",methods=["GET","POST"])
@login_required
def delete(task_id):
    task=db.execute("SELECT * FROM tasks WHERE id=? AND user_id=?",task_id,session["user_id"])

    if len(task)!=1:
        return apology("Invalid Task or you are not authorized to delete this task",400)

    db.execute("DELETE FROM tasks WHERE id=? AND user_id=?",task_id,session["user_id"])

    flash("Task Deleted Successfully!")
    return redirect ("/")
# For marking the task as completed
@app.route("/mark_completed/<int:task_id>",methods=["GET"])
@login_required
def mark_completed(task_id):
    task=db.execute("SELECT * FROM tasks WHERE id=? AND user_id=?",task_id,session["user_id"])

    if len(task)!=1:
        return apology("Invalid Operation",400)

    db.execute("UPDATE tasks SET status='completed' WHERE id=?",task_id)
    flash("Marked Completed Successfully!")
    return redirect("/")
#This route would display a table of all the tasks completed successfully by fetching them from data base
@app.route("/history")
@login_required
def history():
    user_id=session["user_id"]

    tasks= db.execute("SELECT * FROM tasks WHERE user_id=? AND status='completed'",user_id)
    return render_template("history.html",tasks =tasks)
#This route would provide the calender with the data of the due date and title of the task
@app.route("/get_tasks_calendar_data")
@login_required
def get_tasks():
    tasks = db.execute("SELECT * FROM tasks WHERE user_id=? AND status!='completed'", session["user_id"])
    events = []
    for task in tasks:
        due_date = task['due_date']
        if datetime.strptime(due_date, '%Y-%m-%d') >= datetime.now():
            event = {
                "title": task['title'],
                "start": due_date,
                "end": due_date,
                "allDay": True
            }
            events.append(event)
    return jsonify(events)
#Renders the calender.html template
@app.route("/get_tasks_calendar")
@login_required
def get_tasks_calender():
    return render_template("calender.html")

if __name__=="__main__":
    app.run(app.run(debug=True))

