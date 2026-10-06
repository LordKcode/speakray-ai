conversations = {}


def add_message(session_id: str, user_message: str, reply: str):
    if session_id not in conversations:
        conversations[session_id] = []

    conversations[session_id].append({
        "user_message": user_message,
        "reply": reply
    })


def get_conversation(session_id: str):
    return conversations.get(session_id, [])