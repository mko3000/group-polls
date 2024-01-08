from app import app
from flask import render_template, request, redirect
import users
import groups

@app.route("/")
def index():
    return render_template("index.html", groups=groups.get_all_groups())

@app.route("/login", methods=["get", "post"])
def login():
    if request.method == "GET":
        return render_template("login.html")

    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]

        if not users.login(username, password):
            return render_template("error.html", message="Wrong user name or password")
        return redirect("/")

@app.route("/logout")
def logout():
    users.logout()
    return redirect("/")

@app.route("/register", methods=["get", "post"])
def register():
    if request.method == "GET":
        return render_template("register.html")

    if request.method == "POST":
        username = request.form["username"]
        if len(username) < 1:
            return render_template("error.html", message="Too short")

        password1 = request.form["password"]
        #password2 = request.form["password2"]
        #TODO: password2 confirmation for regeister.html
        password2 = password1
        if password1 != password2:
            return render_template("error.html", message="Passwords do not match")
        if password1 == "":
            return render_template("error.html", message="Empty password")

        if not users.register(username, password1):
            return render_template("error.html", message="Registeration failed")
        return redirect("/")

@app.route("/newgroup", methods=["get", "post"])
def newgroup():
    if request.method == "GET":
        return render_template("newgroup.html")
    
    if request.method == "POST":
        users.check_csrf()

        name = request.form["name"]
        creator = users.user_id()
        group_id = groups.add_group(name, creator)

    return redirect("/")

@app.route("/group/<int:group_id>")
def group(group_id):
    name = groups.group_name(group_id)
    return render_template("group.html",name=name)