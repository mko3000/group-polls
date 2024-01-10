import os
from db import db
from flask import abort, request, session
from werkzeug.security import check_password_hash, generate_password_hash
from sqlalchemy.sql import text

def login(username, password):
    sql = text("SELECT password, id FROM polls_users WHERE username=:username")
    result = db.session.execute(sql, {"username":username})
    user = result.fetchone()
    if not user:
        return False
    if not check_password_hash(user[0], password):
        return False
    session["user_id"] = user[1]
    session["user_name"] = username
    session["csrf_token"] = os.urandom(16).hex()
    print(f'session["user_id"]: {session["user_id"]}')
    return True

def logout():
    del session["user_id"]
    del session["user_name"]

def register(username, password):
    hash_value = generate_password_hash(password)
    try:
        sql = text(
            """INSERT INTO polls_users (username, password)
                 VALUES (:username, :password)"""
        )
        db.session.execute(sql, {"username":username, "password":hash_value})
        db.session.commit()
    except:
        return False
    return login(username, password)

def user_id():
    return session.get("user_id", 0)

def check_csrf():
    print("CHECKING CSRF")
    print(f'session["csrf_token"]: {session["csrf_token"]}')
    print(f'request.form["csrf_token"]: {request.form["csrf_token"]}')
    if session["csrf_token"] != request.form["csrf_token"]:
        abort(403)