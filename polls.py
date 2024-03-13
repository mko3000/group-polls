from db import db
from sqlalchemy.sql import text
from db_dataclass import Poll, PollChoice, PollStats


def get_group_polls(group_id):
    """
    Retrieve all polls associated with a specific group.

    Args:
        group_id (int): The ID of the group.

    Returns:
        list: A list of poll objects associated with the group.
    """
    sql = text("""
        SELECT * FROM polls_polls WHERE group_id=:group_id ORDER BY closes_at
        """) 
    return db.session.execute(sql,{"group_id":group_id}).fetchall()

def add_empty_poll(group_id, created_by):
    """
    Adds an empty poll to the database.

    Args:
        group_id (int): The ID of the group to which the poll belongs.
        created_by (str): The username of the user who created the poll.

    Returns:
        int: The ID of the newly created poll.
    """
    sql = text("INSERT INTO polls_polls (group_id, created_by) VALUES (:group_id, :created_by) RETURNING id")
    poll_id = db.session.execute(sql, {"group_id":group_id, "created_by":created_by}).fetchone()[0]
    db.session.commit()
    return poll_id

def delete_poll(poll_id):
    """
    Deletes a poll from the database.

    Args:
        poll_id (int): The ID of the poll to be deleted.
    """
    sql = text("DELETE FROM polls_polls WHERE poll_id=:poll_id")
    db.session.execute(sql, {"poll_id":poll_id})
    db.session.commit()

def add_poll(name, group_id, created_by, closes_at, description):
    """
    Adds a new poll to the database.

    Args:
        name (str): The name of the poll.
        group_id (int): The ID of the group the poll belongs to.
        created_by (str): The username of the user who created the poll.
        closes_at (datetime): The date and time when the poll closes.
        description (str): The description of the poll.

    Returns:
        int: The ID of the newly created poll.
    """
    sql = text("""
        INSERT INTO polls_polls (name, group_id, created_by, created_at, closes_at, description)
        VALUES (:name, :group_id, :created_by, NOW(), :closes_at, :description) RETURNING id
    """)
    poll_id = db.session.execute(sql, {"name":name, "group_id":group_id, "created_by":created_by, "closes_at":closes_at, "description":description}).fetchone()[0]
    db.session.commit()
    return poll_id

def add_poll_details(poll_id, name, description, closes_at):
    """
    Updates the details of a poll in the database.

    Args:
        poll_id (int): The ID of the poll.
        name (str): The name of the poll.
        description (str): The description of the poll.
        closes_at (datetime): The date and time when the poll closes.
    """
    sql = text("""
        UPDATE polls_polls (name, created_at, closes_at, description)
        VALUES (:name, NOW(), :closes_at, :description) 
        WHERE id=:poll_id
    """)
    db.session.execute(sql, {"name":name, "closes_at":closes_at, "description":description, "poll_id":poll_id})
    db.session.commit()

def poll_info(poll_id):
    """
    Retrieve the details of a specific poll.

    Args:
        poll_id (int): The ID of the poll.

    Returns:
        Poll: A poll object containing the details of the poll.
    """

    sql = text("""
        SELECT p.name, p.group_id, p.created_by, u.username AS creator_name, p.created_at, p.closes_at, p.description  
        FROM polls_polls p
        JOIN polls_users u ON p.created_by = u.id
        WHERE p.id = :poll_id
    """)
    out = db.session.execute(sql, {"poll_id":poll_id}).fetchone()
    return Poll(poll_id, *out)
    

def get_choices(poll_id):
    """
    Retrieve all choices associated with a specific poll.

    Args:
        poll_id (int): The ID of the poll.

    Returns:
        list: A list of poll choice objects associated with the poll.
    """
    sql = text("SELECT * FROM polls_choices WHERE poll_id=:poll_id ORDER BY added_at")
    out = db.session.execute(sql,{"poll_id":poll_id}).fetchall()
    return [PollChoice(*x) for x in out]


def add_choice(name, poll_id, added_by):
    """
    Adds a new choice to the database.

    Args:
        name (str): The name of the choice.
        poll_id (int): The ID of the poll the choice belongs to.
        added_by (int): The ID of the user who added the choice.

    Returns:
        int: The ID of the newly created choice.
    """

    sql = text("""
        INSERT INTO polls_choices (name, poll_id, added_by, added_at, votes)
        VALUES (:name, :poll_id, :added_by, NOW(), 0) RETURNING id
    """)
    choice_id = db.session.execute(sql, {"name":name, "poll_id":poll_id, "added_by":added_by}).fetchone()[0]    
    db.session.commit()
    return choice_id

def vote(choice_id, user_id):
    """
    Adds a vote.

    Args:
        choice_id (int): The ID of the choice.
        user_id (int): The ID of the user who voted.
    """
    choice_id = int(choice_id)
    sql = text("""
        INSERT INTO polls_user_votes (choice_id, user_id)
        SELECT * FROM (SELECT :choice_id, :user_id) AS tmp
        WHERE NOT EXISTS (
            SELECT 1 FROM polls_user_votes WHERE choice_id = :choice_id AND user_id = :user_id
        )
    """)
    db.session.execute(sql, {"choice_id":choice_id,"user_id":user_id})
    db.session.commit()
    sql = text("UPDATE polls_choices SET votes = votes + 1 WHERE id = :choice_id")
    db.session.execute(sql, {"choice_id":choice_id})
    db.session.commit()

def unvote(choice_id, user_id):
    """
    Removes a vote.

    Args:
        choice_id (int): The ID of the choice.
        user_id (int): The ID of the user who voted.
    """
    if get_choice_votes(choice_id) > 0:
        sql = text("DELETE FROM polls_user_votes WHERE choice_id = :choice_id AND user_id = :user_id")
        db.session.execute(sql, {"choice_id":choice_id,"user_id":user_id})
        db.session.commit()
        sql = text("UPDATE polls_choices SET votes = votes - 1 WHERE id = :choice_id")
        db.session.execute(sql, {"choice_id":choice_id})
        db.session.commit()

def has_voted(choice_id, user_id):
    """
    Checks if a user has voted for a specific choice.

    Args:
        choice_id (int): The ID of the choice.
        user_id (int): The ID of the user.
        
    Returns:
        bool: True if the user has voted for the choice, False otherwise.
    """
    sql = text("SELECT * FROM polls_user_votes WHERE choice_id = :choice_id AND user_id = :user_id")
    result = db.session.execute(sql, {"choice_id":choice_id,"user_id":user_id}).fetchone()
    if result != None:
        return True
    return False

def get_choice_votes(choice_id):
    """
    Retrieve the number of votes for a specific choice.

    Args:
        choice_id (int): The ID of the choice.

    Returns:
        int: The number of votes for the choice.
    """
    sql = text("SELECT COUNT (user_id) FROM polls_user_votes WHERE choice_id=:choice_id")
    return db.session.execute(sql, {"choice_id":choice_id}).fetchone()[0]

def poll_stats(poll_id):
    """
    Retrieve the statistics for a specific poll.

    Args:
        poll_id (int): The ID of the poll.

    Returns:
        PollStats: A poll stats object containing the statistics for the poll.
    """
    sql = text("""
        WITH TotalVotes AS (
            SELECT
                poll_id,
                COUNT(user_id) AS total_votes
            FROM
                polls_user_votes puv
            JOIN
                polls_choices pc ON puv.choice_id = pc.id
            WHERE
                pc.poll_id = :poll_id
            GROUP BY
                poll_id
        ),
        MaxVotes AS (
            SELECT
                poll_id,
                MAX(vote_count) AS max_votes
            FROM
                (SELECT
                    pc.poll_id,
                    pc.id AS choice_id,
                    COUNT(puv.user_id) AS vote_count
                FROM
                    polls_choices pc
                LEFT JOIN
                    polls_user_votes puv ON pc.id = puv.choice_id
                WHERE
                    pc.poll_id = :poll_id
                GROUP BY
                    pc.poll_id, pc.id) AS vote_counts
            GROUP BY
                poll_id
        )
        SELECT
            tv.poll_id,
            tv.total_votes,
            mv.max_votes,
            (tv.total_votes * 1.0 / (SELECT COUNT(*) FROM polls_choices WHERE poll_id = :poll_id)) AS average_votes_per_choice
        FROM
            TotalVotes tv
        JOIN
            MaxVotes mv ON tv.poll_id = mv.poll_id;
    """)
    out = db.session.execute(sql, {"poll_id":poll_id}).fetchall()[0]
    return PollStats(*out[0:3],round(out[3],2))


def poll_winner(poll_id):
    """
    Retrieve the winner of a specific poll.

    Args:
        poll_id (int): The ID of the poll.

    Returns:
        PollChoice: The choice that won the poll.
    """
    sql = text("""
        WITH ChoiceVotes AS (
            SELECT
                pc.poll_id,
                pc.id AS choice_id,
                pc.name AS choice_name,
                pc.added_by AS added_by,
                pc.added_at AS added_at,
                pc.votes AS votes,
                COUNT(puv.user_id) AS vote_count
            FROM
                polls_choices pc
            LEFT JOIN
                polls_user_votes puv ON pc.id = puv.choice_id
            WHERE
                pc.poll_id = :poll_id
            GROUP BY
                pc.poll_id, pc.id, pc.name
        ),
        MaxVotes AS (
            SELECT
                poll_id,
                MAX(vote_count) AS max_votes
            FROM
                ChoiceVotes
            GROUP BY
                poll_id
        )
        SELECT
            cv.choice_id,
            cv.choice_name,
            cv.added_by,
            cv.added_at,
            cv.votes
        FROM
            ChoiceVotes cv
        JOIN
            MaxVotes mv ON cv.poll_id = mv.poll_id AND cv.vote_count = mv.max_votes
        WHERE
            cv.poll_id = :poll_id
    """)
    out = db.session.execute(sql, {"poll_id":poll_id}).fetchall()
    return [PollChoice(*row[0:2],poll_id,*row[2:]) for row in out]

def get_poll_results(poll_id):
    """
    Retrieve the results of a specific poll.

    Args:
        poll_id (int): The ID of the poll.

    Returns:
        list: A list of poll choice objects containing the results of the poll.
    """
    choices = get_choices(poll_id)
    choices = sorted(choices, key=lambda x: x.votes, reverse=True)

    return choices