# usertrack-lite

A lightweight real-time user behavior tracking system built with FastAPI, Redis Streams, and PostgreSQL.

## Features

- Track user behavior via API
- Redis Stream-based message queue
- Background consumer to insert into PostgreSQL
- Simple query endpoint
- Logging and error handling
- Minimal unit testing

## Project Structure

```
main.py               # FastAPI API
event_worker.py       # Redis stream consumer
test_user_behavior_api.py
requirements.txt
sql/create_table.sql  # DB schema
README.md
```

## PostgreSQL Table Schema

```sql
CREATE TABLE user_behavior (
  id UUID PRIMARY KEY,
  user_id VARCHAR NOT NULL,
  event_type VARCHAR NOT NULL,
  page_url TEXT,
  device_type VARCHAR,
  metadata JSONB,
  timestamp TIMESTAMP,
  ip_address VARCHAR
);
```

## How to Run

1. Create virtual environment:

```bash
python -m venv venv
source venv/bin/activate   # Windows: venv\Scripts\activate
```

2. Install dependencies:

```bash
pip install -r requirements.txt
```

3. Start PostgreSQL and Redis servers.

4. Run FastAPI server:

```bash
uvicorn main:app --reload
```

5. Start the background Redis consumer:

```bash
python event_worker.py
```

6. Access API at [http://127.0.0.1:8000/docs](http://127.0.0.1:8000/docs)

## ➕ Aggregation Endpoint

### GET /aggregate-events

Returns the count of events grouped by `event_type`. Optional filter by `user_id`.

**Example**: `/aggregate-events?user_id=user123`

**Response**:
```json
{
  "click": 4,
  "scroll": 2
}