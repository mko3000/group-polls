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
