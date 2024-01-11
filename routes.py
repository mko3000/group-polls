from app import app
from flask import render_template, request, redirect
from datetime import date, timedelta
import users
import groups
import polls


@app.route("/")
def index():
    groups.end_group_session()
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
    if users.user_id() == 0:
        return render_template("error.html", message="Not logged in")
    
    if request.method == "GET":
        return render_template("newgroup.html")
    
    if request.method == "POST":
        users.check_csrf()

        name = request.form["name"]
        creator = users.user_id()
        group_id = groups.add_group(name, creator)

    return redirect(f'/group/{group_id}')

@app.route("/group/<int:group_id>")
def group(group_id):
    groups.start_group_session(group_id)
    name = groups.group_info(group_id)[0]
    members = groups.group_info(group_id)[1]
    in_group = groups.in_group(users.user_id(), group_id)
    return render_template(
        "group.html", 
        group_id=group_id, 
        name=name, 
        members=members, 
        in_group=in_group, 
        polls=polls.get_group_polls(group_id)
    )

@app.route("/join/<int:group_id>")
def join(group_id):
    if users.user_id() == 0:
        return render_template("error.html", message="Not logged in")
    groups.join_group(users.user_id(),group_id)
    return redirect(f'/group/{group_id}')

@app.route("/leave/<int:group_id>")
def leave(group_id):
    groups.leave_group(users.user_id(),group_id)
    return redirect(f'/group/{group_id}')

@app.route("/startnewpoll", methods=["POST"])
def startnewpoll():
    if request.method == "POST":
        pass

@app.route("/newpoll", methods=["get", "post"])
def newpoll():
    if users.user_id() == 0:
        return render_template("error.html", message="Not logged in")
    
    tomorrow = date.today() + timedelta(1)
    
    if request.method == "GET":
        return render_template(
            "newpoll.html", 
            day = tomorrow.strftime('%d'), 
            month = tomorrow.strftime('%m'), 
            year = tomorrow.year
        )
    
    if request.method == "POST":
        users.check_csrf()
        name = request.form["name"]
        creator = users.user_id()
        closes_at = request.form["poll_ends"]
        #closes_at = "2024-02-29 10:10:10"
        description = request.form["description"]
        group_id = groups.get_group_id()
        poll_id = polls.add_poll(name,group_id,creator,closes_at,description)

    return redirect(f'/poll/{poll_id}')

@app.route("/poll/<int:poll_id>")
def poll(poll_id): 
    info = polls.poll_info(poll_id)   
    return render_template(
        "poll.html",
        name = info[0],
        created_by = info[1],
        created_at = info[2],
        closes_at = info[3],
        description = info[4],
        group_id = info[5],
        choices = polls.get_choices(poll_id)
    )