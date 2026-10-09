from database.db import get_connection


def add_message(session_id: str, user_message: str, reply: str):
    connection = get_connection()

    connection.execute(
    """
    INSERT INTO messages (session_id, user_message, reply, created_at)
    VALUES (?, ?, ?, CURRENT_TIMESTAMP)
    """,
    (session_id, user_message, reply)
)

    connection.commit()
    connection.close()


def get_conversation(session_id: str):
    connection = get_connection()

    rows = connection.execute(
        """
        SELECT user_message, reply, created_at
        FROM messages
        WHERE session_id = ?
        ORDER BY id
        """,
        (session_id,)
    ).fetchall()

    connection.close()

    return [dict(row) for row in rows]