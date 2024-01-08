from db import db
from sqlalchemy.sql import text

def get_all_groups():
    sql = text("SELECT id, name FROM polls_groups")
    return db.session.execute(sql).fetchall()

def add_group(name, creator):
    print(f'user {creator} creating group {name}')
    sql = text(
        """INSERT INTO polls_groups (name, creator)
            VALUES (:name, :creator) RETURNING id"""
    )
    
    group_id = db.session.execute(sql, {"name":name,"creator":creator}).fetchone()[0]
    db.session.commit()
    return group_id

def group_name(group_id):
    print(f'group_id: {group_id}')
    sql = text("SELECT name FROM polls_groups WHERE id=:group_id")
    print("SQL QUERY UPCOMMING",sql)
    result = db.session.execute(sql, {"group_id":group_id})
    print("SQL QUERY DONE")
    print(result)
    return result.fetchone()[0]