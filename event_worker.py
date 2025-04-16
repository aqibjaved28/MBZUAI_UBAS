import json
from psycopg2.extras import Json
from config import get_db_connection, redis_client, STREAM_KEY

def write_to_postgres(event):
    conn = get_db_connection()
    cur = conn.cursor()
    query = """
        INSERT INTO user_behavior (id, user_id, event_type, page_url, device_type, metadata, timestamp, ip_address)
        VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
        ON CONFLICT (id) DO NOTHING
    """
    cur.execute(query, (
        event["id"],
        event["user_id"],
        event["event_type"],
        event["page_url"],
        event["device_type"],
        Json(event["metadata"] if isinstance(event["metadata"], dict) else json.loads(event["metadata"])),
        event["timestamp"],
        event["ip_address"]
    ))
    conn.commit()
    cur.close()
    conn.close()

def consume():
    last_id = '0-0'
    while True:
        entries = redis_client.xread({STREAM_KEY: last_id}, block=0, count=1)
        for stream, messages in entries:
            for msg_id, msg in messages:
                decoded_msg = {k.decode(): v.decode() for k, v in msg.items()}
                write_to_postgres(decoded_msg)
                last_id = msg_id

if __name__ == "__main__":
    consume()