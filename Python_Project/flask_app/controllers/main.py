from flask_app import app
from flask import Flask, render_template, request, redirect, session, flash
from flask_app.models.users import User
# from flask_app.models.recipes import Recipe
from flask_bcrypt import Bcrypt
bcrypt = Bcrypt(app)


@app.route("/")
def index():
    return render_template("index.html")


@app.route("/register", methods=["post"])
def register_user():
    # print("trying to register here")
    # print(request.form)
    data = {
        "first_name": request.form["first_name"],
        "last_name": request.form["last_name"],
        "email": request.form["email"],
        "password": request.form["password"],
        "confirm_password": request.form["confirm_password"],
    }
    this_user = User.find_one_by_email(data)
    if this_user:
        flash("Email is already in use!")
        return redirect("/")

    
    if not User.validate(data):
        print("not valid")
        return redirect("/")

    #information is valid
    pw_hash = bcrypt.generate_password_hash(request.form["password"])
    data["password"] = pw_hash
    # print(f"password: {request.form['password']}")
    # print(f"hashed password: {pw_hash}")


    user_id = User.save(data)
    session["logged_id"] = user_id
    
    return redirect("/main")

@app.route("/login", methods=["post"])
def login_user():
    
    data = {
        "email": request.form["email"]
    }
    
    this_user = User.find_one_by_email(data)
    if not this_user:
    #first thing we do is check if the user by that email exists 
    # and if they don't, flash message and redirect to form page
        flash("Invalid email/password")
        return redirect("/")
    #if it does exist
    #check the password, compare the hashed passwords to see if they are equal
    #if not equal then flash message and redirect to form page

    if not bcrypt.check_password_hash(this_user.password, request.form['password']):
        flash("Invalid email/password")
        return redirect("/")

    #if they are equal, you loggged in
    session["logged_id"] = this_user.id
    print("successful login")
    return redirect("/main")

@app.route("/logout")
def logout():
    session.clear()        #session.clear will clear absolutely everything in the session 
    #del session["logged_id"]      del session at the value of "logged_id will only get rid of that part of session"
    return redirect("/main")


@app.route("/main")
def success():
    
    
    return render_template("main.page.html")



@app.route("/create")
def new_post():
    return render_template("create.html")

@app.route("/reviews")
def view_review():
    return render_template("reviews.html")

@app.route("/user/posts")
def user_posts():
    return render_template("userposts.html")





