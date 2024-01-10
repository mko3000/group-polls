from db import db
from sqlalchemy.sql import text

def get_all_groups():
    sql = text("SELECT id, name FROM polls_groups")
    return db.session.execute(sql).fetchall()

def add_group(name, creator):
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
    print(f'group name: {name}, members: {member_count}')
    return [name,member_count]

def join_group(user_id, group_id):
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
    print(f'check if user {user_id} in group {group_id}')
    sql = text("SELECT * FROM polls_group_members WHERE group_id = :group_id AND user_id = :user_id")
    result = db.session.execute(sql, {"group_id":group_id,"user_id":user_id}).fetchone()
    if result != None:
        return True
    return False

def leave_group(user_id, group_id):
    sql = text("DELETE FROM polls_group_members WHERE group_id = :group_id AND user_id = :user_id")
    db.session.execute(sql, {"group_id":group_id,"user_id":user_id})
    db.session.commit()