from fastapi import FastAPI, HTTPException, Request, Query
from pydantic import BaseModel, Field
from uuid import uuid4
from datetime import datetime, timezone
import json
import psycopg2
import psycopg2.extras
from typing import Optional
import logging
from contextlib import asynccontextmanager
from config import get_db_connection, redis_client, STREAM_KEY
from datetime import datetime, UTC

# Logging setup
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

@asynccontextmanager
async def lifespan(app: FastAPI):
    logger.info("🔄 App starting up...")

    try:
        redis_client.ping()
        logger.info("✅ Connected to Redis.")
    except Exception as e:
        logger.error("❌ Redis connection failed: " + str(e))

    try:
        conn = get_db_connection()
        conn.close()
        logger.info("✅ Connected to PostgreSQL.")
    except Exception as e:
        logger.error("❌ PostgreSQL connection failed: " + str(e))

    yield
    logger.info("🔚 App shutting down...")

app = FastAPI(lifespan=lifespan)

class UserEvent(BaseModel):
    user_id: str
    event_type: str
    page_url: Optional[str] = None
    device_type: Optional[str] = None
    metadata: dict = Field(default_factory=dict)
    timestamp: Optional[datetime] = None
    ip_address: Optional[str] = None

@app.post("/track-event")
async def track_event(event: UserEvent, request: Request):
    try:
        event_data = {
            "id": str(uuid4()),
            "user_id": event.user_id,
            "event_type": event.event_type,
            "page_url": event.page_url or "",
            "device_type": event.device_type or "",
            "metadata": json.dumps(event.metadata),
            "timestamp": event.timestamp.isoformat() if event.timestamp else datetime.now(timezone.utc).isoformat(),
            "ip_address": request.client.host
        }
        redis_client.xadd(STREAM_KEY, event_data)
        logger.info("Event queued successfully.")
        return {"message": "Event received and queued successfully."}
    except Exception as e:
        logger.error(str(e))
        raise HTTPException(status_code=500, detail="Failed to queue event.")

@app.get("/query-events")
async def query_events(user_id: Optional[str] = Query(None), event_type: Optional[str] = Query(None)):
    try:
        conn = get_db_connection()
        cur = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)
        query = "SELECT * FROM user_behavior WHERE 1=1"
        params = []
        if user_id:
            query += " AND user_id = %s"
            params.append(user_id)
        if event_type:
            query += " AND event_type = %s"
            params.append(event_type)
        cur.execute(query, params)
        rows = cur.fetchall()
        cur.close()
        conn.close()
        return {"results": [dict(row) for row in rows]}
    except Exception as e:
        logger.error(str(e))
        raise HTTPException(status_code=500, detail="Failed to query events.")

@app.get("/aggregate-events")
async def aggregate_events(user_id: Optional[str] = Query(None)):
    try:
        conn = get_db_connection()
        cur = conn.cursor()
        if user_id:
            cur.execute("""
                SELECT event_type, COUNT(*) 
                FROM user_behavior 
                WHERE user_id = %s 
                GROUP BY event_type
            """, (user_id,))
        else:
            cur.execute("""
                SELECT event_type, COUNT(*) 
                FROM user_behavior 
                GROUP BY event_type
            """)
        results = cur.fetchall()
        cur.close()
        conn.close()
        return {r[0]: r[1] for r in results}
    except Exception as e:
        logger.error(str(e))
        raise HTTPException(status_code=500, detail="Aggregation query failed.")

@app.get("/health")
async def health_check():
    try:
        redis_client.ping()
        conn = get_db_connection()
        conn.close()
        return {"status": "ok"}
    except Exception as e:
        logger.error(f"Health check failed: {str(e)}")
        raise HTTPException(status_code=503, detail="Service unavailable")