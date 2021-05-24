from collections import Counter

from notmuch import Query, Database

db = Database(mode=Database.MODE.READ_ONLY)

def tag_counts(query: str) -> Counter:
    """counts messages by tag for given query"""
    q = db.create_query(query)
    messages = q.search_messages()

    tc = Counter()
    for msg in messages:
        tc["total"] += 1
        for tag in msg.get_tags():
            tc[tag] += 1

    return tc

