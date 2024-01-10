from db import db
from sqlalchemy.sql import text


def get_group_polls(group_id):
    sql = text("SELECT * FROM polls_polls WHERE group_id=:group_id") 
    return db.session.execute(sql,{"group_id":group_id}).fetchall()

def add_poll(name, group_id, created_by, closes_at):
    sql = text("""
        INSERT INTO polls_polls (name, group_id, created_by, created_at, closes_at)
        VALUES (:name, :group_id, :created_by, NOW(), :closes_at) RETURNING id
    """)
    poll_id = db.session.execute(sql, {"name":name, "group_id":group_id, "created_by":created_by, "closes_at":closes_at}).fetchone()[0]
    db.session.commit()
    return poll_id