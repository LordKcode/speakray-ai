import sqlite3

DATABASE = "database/speakray.db"


def get_connection():
    connection = sqlite3.connect(DATABASE)
    connection.row_factory = sqlite3.Row
    return connection



def initialize_database():
    connection = get_connection()

    connection.execute("""
        CREATE TABLE IF NOT EXISTS messages (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            session_id TEXT NOT NULL,
            user_message TEXT NOT NULL,
            reply TEXT NOT NULL,
            created_at TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP
        )
    """)

    columns = connection.execute(
        "PRAGMA table_info(messages)"
    ).fetchall()

    column_names = [column["name"] for column in columns]

    if "created_at" not in column_names:
        connection.execute(
            "ALTER TABLE messages ADD COLUMN created_at TEXT"
        )

        connection.execute("""
            UPDATE messages
            SET created_at = CURRENT_TIMESTAMP
            WHERE created_at IS NULL
        """)

    connection.commit()
    connection.close()

def get_all_sessions():
    connection = get_connection()

    rows = connection.execute("""
        SELECT
            session_id,
            COUNT(*) AS message_count,
            MAX(created_at) AS last_message_at
        FROM messages
        GROUP BY session_id
        ORDER BY last_message_at DESC
    """).fetchall()

    connection.close()

    return [dict(row) for row in rows]

if __name__ == "__main__":
    initialize_database()
    print("SpeakRay database initialized successfully.")