import threading
from types import SimpleNamespace

# Thread-local data container. Each instance of the bot processes
# one request at the time, so it is safe to store data here.
thread_local = threading.local()


def generate_tracking_container(user_id, chat_id, chat_type):
    thread_local.context = SimpleNamespace(
        user_id=user_id, chat_id=chat_id, chat_type=chat_type
    )

    return thread_local.context


def get_tracking_context():
    """Retrieve the context information for the current thread."""
    return getattr(thread_local, "context", None)
