from app import app
from flask import render_template, request, redirect
from datetime import date, timedelta, datetime
import users
import groups
import polls


@app.route("/")
def index():
    groups.end_group_session()
    return render_template("index.html", groups=groups.get_all_groups(), group_info=groups.get_all_groups_with_info(users.user_id()))

@app.route("/login", methods=["get", "post"])
def login():
    if request.method == "GET":
        return render_template("login.html")

    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]

        if not users.login(username, password):
            return render_template("error.html", message="Wrong user name or password", link="/login", link_text="Try again")
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
            return render_template("error.html", message="Too short", link="/register", link_text="Try again")

        password1 = request.form["password"]
        #password2 = request.form["password2"]
        #TODO: password2 confirmation for regeister.html
        password2 = password1
        if password1 != password2:
            return render_template("error.html", message="Passwords do not match",link="/register", link_text="Try again")
        if password1 == "":
            return render_template("error.html", message="Empty password",link="/register", link_text="Try again")

        if not users.register(username, password1):
            return render_template("error.html", message="Registeration failed",link="/register", link_text="Try again")
        return redirect("/")

@app.route("/newgroup", methods=["get", "post"])
def newgroup():
    if users.user_id() == 0:
        return render_template("error.html", message="Not logged in", link="/login", link_text="Log in")
    
    if request.method == "GET":
        return render_template("newgroup.html")
    
    if request.method == "POST":
        users.check_csrf()

        name = request.form["name"]
        creator = users.user_id()
        group_id = groups.add_group(name, creator)
        groups.join_group(users.user_id(),group_id)

    return redirect(f'/group/{group_id}')

@app.route("/group/<int:group_id>")
def group(group_id):
    groups.start_group_session(group_id)
    group_info = groups.group_info(group_id)
    name = group_info[0]
    members = group_info[1]
    in_group = groups.in_group(users.user_id(), group_id)
    poll_list = polls.get_group_polls(group_id)
    for poll in poll_list:
        if poll.closes_at < datetime.now():
            print("expired poll")
    return render_template(
        "group.html", 
        group_id=group_id, 
        name=name, 
        members=members, 
        in_group=in_group, 
        polls=poll_list,
        current_time = datetime.now()
    )

@app.route("/join/<int:group_id>")
def join(group_id):
    if users.user_id() == 0:
        return render_template("error.html", message="Not logged in", link="/login", link_text="Log in")
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
        return render_template("error.html", message="Not logged in", link="/login", link_text="Log in")
    
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
        description = request.form["description"]
        group_id = groups.get_group_id()
        poll_id = polls.add_poll(name,group_id,creator,closes_at,description)

    return redirect(f'/poll/{poll_id}')

@app.route("/poll/<int:poll_id>")
def poll(poll_id): 
    group_id = groups.get_group_id()
    group_name = groups.group_name(group_id)
    info = polls.poll_info(poll_id)  
    choices = polls.get_choices(poll_id)
    user_choices = []
    time_left = info.closes_at - datetime.now()
    time_left_str = f"{time_left.days}d {time_left.seconds // 3600}h {(time_left.seconds // 60) % 60}m {time_left.seconds % 60}s"
    poll_stats = polls.poll_stats(poll_id)
    poll_winners = None  
    results = polls.get_poll_results(poll_id) 
    poll_results = []
    for result in results: 
        poll_results.append({"name":result.name, "votes":result.votes})
    if time_left < timedelta(0):
        time_left_str = "EXPIRED"
        poll_winners = polls.poll_winner(poll_id)


    for choice in choices:
        user_choices.append({            
            "details":choice, 
            "has_voted":polls.has_voted(choice.id,users.user_id()),
            "choice_votes":polls.get_choice_votes(choice.id)
        })

    return render_template(
        "poll.html",
        name = info.name,
        created_by = info.creator_name,
        created_at = info.created_at,
        closes_at = info.closes_at,
        description = info.description,
        time_left = time_left_str,
        closed = int(datetime.now() > info.closes_at),
        group_id = group_id,
        group_name = group_name,
        choices = user_choices,
        poll_id = poll_id,
        poll_stats = poll_stats,
        poll_winners = poll_winners,
        poll_results = poll_results
    )

@app.route("/newchoice", methods=["post"])
def newchoice():
    users.check_csrf()
    if users.user_id() == 0:
        return render_template("error.html", message="Not logged in", link="/login", link_text="Log in")

    poll_id = request.args.get("poll_id")
    new_choice = request.form["new_choice"]
    if len(new_choice) < 1:
        return render_template("error.html", message="Too short", link=f"/poll/{poll_id}", link_text="Try again")
    else:
        choice_id = polls.add_choice(new_choice, poll_id, users.user_id())

    return redirect(f'/poll/{poll_id}')

@app.route("/upvote", methods=["post"])
def upvote():
    users.check_csrf()
    if users.user_id() == 0:
        return render_template("error.html", message="Not logged in", link="/login", link_text="Log in")

    poll_id = request.args.get("poll_id")
    choice_id = request.form["choice_id"]
    polls.vote(choice_id,users.user_id())    

    return redirect(f'/poll/{poll_id}')

@app.route("/downvote", methods=["post"])
def downvote():
    users.check_csrf()
    if users.user_id() == 0:
        return render_template("error.html", message="Not logged in", link="/login", link_text="Log in")

    poll_id = request.args.get("poll_id")
    choice_id = request.form["choice_id"]
    polls.unvote(choice_id,users.user_id())    

    return redirect(f'/poll/{poll_id}')
