from functools import wraps
from flask import redirect,session,render_template

# Defines the login required function and if the user id is not in session it returns the user to the login page
def login_required(f):

    @wraps(f)
    def decorated_function(*args,**kwargs):
        if "user_id" not in session:
            return redirect("/login")
        return f(*args,**kwargs)
    return decorated_function

# Definition of the apology function
def apology(message,code=400):
    return render_template("apology.html",message=message,code=code)
