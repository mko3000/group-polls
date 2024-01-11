from db import db
from sqlalchemy.sql import text


def get_group_polls(group_id):
    sql = text("SELECT * FROM polls_polls WHERE group_id=:group_id") 
    return db.session.execute(sql,{"group_id":group_id}).fetchall()

def add_empty_poll(group_id, created_by):
    sql = text("INSERT INTO polls_polls (group_id, created_by) VALUES (:group_id, :created_by) RETURNING id")
    poll_id = db.session.execute(sql, {"group_id":group_id, "created_by":created_by}).fetchone()[0]
    db.session.commit()
    return poll_id

def delete_poll(poll_id):
    sql = text("DELETE FROM polls_polls WHERE poll_id=:poll_id")
    db.session.execute(sql, {"poll_id":poll_id})
    db.session.commit()

def add_poll(name, group_id, created_by, closes_at, description):
    sql = text("""
        INSERT INTO polls_polls (name, group_id, created_by, created_at, closes_at)
        VALUES (:name, :group_id, :created_by, NOW(), :closes_at) RETURNING id
    """)
    poll_id = db.session.execute(sql, {"name":name, "group_id":group_id, "created_by":created_by, "closes_at":closes_at}).fetchone()[0]
    db.session.commit()
    return poll_id

def add_poll_details(poll_id, name, description, closes_at):
    sql = text("""
        UPDATE polls_polls (name, created_at, closes_at, description)
        VALUES (:name, NOW(), :closes_at, :description) 
        WHERE id=:poll_id
    """)
    db.session.execute(sql, {"name":name, "closes_at":closes_at, "description":description, "poll_id":poll_id})
    db.session.commit()

def poll_info(poll_id):
    sql = text("SELECT name, created_by, created_at, closes_at, description, group_id FROM polls_polls WHERE id=:poll_id")
    return db.session.execute(sql, {"poll_id":poll_id}).fetchone()

def get_choices(poll_id):
    sql = text("SELECT * FROM polls_choices WHERE poll_id=:poll_id")
    return db.session.execute(sql,{"poll_id":poll_id}).fetchall()

def add_choice(name, poll_id, added_by):
    sql = text("""
        INSERT INTO polls_choices (name, poll_id, added_by, votes)
        VALUES (:name, :poll_id, :added_by, 0)
    """)
    choice_id = db.session.execute(sql, {"name":name, "poll_id":poll_id, "added_by":added_by}).fetchone()[0]    
    db.session.commit()
    return choice_id

def vote(choice_id, user_id):
    sql = text("""
        INSERT INTO polls_user_votes (choice_id, user_id)
        SELECT * FROM (SELECT :choice_id, :user_id) AS tmp
        WHERE NOT EXISTS (
            SELECT 1 FROM polls_user_votes WHERE choice_id = :choice_id AND user_id = :user_id
        )
    """)
    db.session.execute(sql, {"choice_id":choice_id,"user_id":user_id})
    db.session.commit()

def unvote(choice_id, user_id):
    sql = text("DELETE FROM polls_user_votes WHERE choice_id = :choice_id AND user_id = :user_id")
    db.session.execute(sql, {"choice_id":choice_id,"user_id":user_id})
    db.session.commit()

def has_voted(choice_id, user_id):
    sql = text("SELECT * FROM polls_user_votes WHERE choice_id = :choice_id AND user_id = :user_id")
    result = db.session.execute(sql, {"choice_id":choice_id,"user_id":user_id}).fetchone()
    if result != None:
        return True
    return False