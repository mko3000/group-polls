from db import db
from sqlalchemy.sql import text
from flask import session

def get_all_groups():
    sql = text("SELECT id, name FROM polls_groups")
    return db.session.execute(sql).fetchall()

def get_all_groups_with_info(user_id):
    sql = text("""
                SELECT 
                    g.id AS group_id, 
                    g.name, 
                    g.creator, 
                    COUNT(m.user_id) AS member_count, 
                    BOOL_OR(m.user_id = :user_id) AS user_joined_group
                FROM 
                    polls_groups g
                LEFT JOIN 
                    polls_group_members m ON g.id = m.group_id
                GROUP BY 
                    g.id
               """)
    return db.session.execute(sql, {"user_id":user_id}).fetchall()

def add_group(name, creator):
    if creator == 0:
        return False
    sql = text("""
        INSERT INTO polls_groups (name, creator)
        VALUES (:name, :creator) RETURNING id
    """)
    
    group_id = db.session.execute(sql, {"name":name,"creator":creator}).fetchone()[0]
    db.session.commit()
    return group_id

def group_name(group_id):
    sql = text("SELECT name FROM polls_groups WHERE id=:group_id")
    result = db.session.execute(sql, {"group_id":group_id})
    return result.fetchone()[0]

def group_info(group_id):
    sql = text("SELECT name FROM polls_groups WHERE id=:group_id")
    name = db.session.execute(sql, {"group_id":group_id}).fetchone()[0]
    sql = text("SELECT COUNT(user_id) FROM polls_group_members WHERE group_id=:group_id")
    member_count = db.session.execute(sql, {"group_id":group_id}).fetchone()[0]
    return (name,member_count)

def join_group(user_id, group_id):
    print("JOINING USER ID:",user_id)
    if user_id == 0:
        return False
    sql = text("""
        INSERT INTO polls_group_members (group_id, user_id)
        SELECT * FROM (SELECT :group_id, :user_id) AS tmp
        WHERE NOT EXISTS (
            SELECT 1 FROM polls_group_members WHERE group_id = :group_id AND user_id = :user_id
        )
        """)
    db.session.execute(sql, {"group_id":group_id,"user_id":user_id})
    db.session.commit()

def in_group(user_id, group_id):
    sql = text("SELECT * FROM polls_group_members WHERE group_id = :group_id AND user_id = :user_id")
    result = db.session.execute(sql, {"group_id":group_id,"user_id":user_id}).fetchone()
    if result != None:
        return True
    return False

def leave_group(user_id, group_id):
    sql = text("DELETE FROM polls_group_members WHERE group_id = :group_id AND user_id = :user_id")
    db.session.execute(sql, {"group_id":group_id,"user_id":user_id})
    db.session.commit()

def start_group_session(group_id):
    session["group_id"]=group_id

def end_group_session():
    if "group_id" in session:
        del session["group_id"]

def get_group_id():
    return session.get("group_id", 0)