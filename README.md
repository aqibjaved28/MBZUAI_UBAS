# 📊 MBZUAI@UBAS devloped by Muhammad Aqib Javed

A lightweight, real-time user behavior tracking system built using FastAPI, Redis Streams, and PostgreSQL.

---

## 🚀 Features

- ✅ Track user behavior events through a REST API  
- ✅ Redis Stream used for queuing data before persistence  
- ✅ PostgreSQL for structured data storage  
- ✅ Decoupled ingestion and storage with background worker  
- ✅ Basic analytics endpoint via aggregation  
- ✅ `/health` check for monitoring  
- ✅ Async architecture built for scalability  
- ✅ Minimal unit tests using Pytest  
- ✅ Clean and modular codebase  

---

```
MBZUAI-UBAS/
├── main.py                     # FastAPI application with endpoints
├── event_worker.py             # Redis stream consumer and DB writer
├── config.py                   # Centralized PostgreSQL and Redis connection logic
├── test_user_behavior_api.py   # Unit tests using Pytest
├── .env.example                # Centralized PostgreSQL and Redis credentials setup
├── requirements.txt            # Python dependencies
├── README.md                   # Project documentation
└── sql/
    └── create_table.sql        # PostgreSQL table schema
```

---

## 🖥️ Tech Stack

- **Language:** Python 3.10+  
- **Web Framework:** FastAPI  
- **Message Queue:** Redis Streams  
- **Database:** PostgreSQL with JSONB columns  
- **Testing:** Pytest  
- **Monitoring:** Logging + `/health` endpoint  

---

## 🔧 Setup & Installation

1. 📁 Clone or extract the project (git clone git@github.com:aqibjaved28/MBZUAI_UBAS.git)  
2. 🔧 Create and activate virtual environment
```bash
python -m venv venv
venv\\Scripts\\activate    # Windows
```
3. 📦 Install dependencies
```bash
pip install -r requirements.txt    # Windows
```
4. 🔧 Configure .env
```bash
cp .env.example .env   
```
```bash
# PostgreSQL Config
DB_HOST=localhost
DB_PORT=5432
DB_NAME=your_database_name
DB_USER=your_db_username
DB_PASSWORD=your_db_password

# Redis Config
REDIS_HOST=localhost
REDIS_PORT=6379
REDIS_STREAM_KEY=user_behavior_stream  
```
5. 🗃️ Create PostgreSQL database & table 
Install PostgreSQL from https://www.postgresql.org
```bash
# In psql or pgAdmin
CREATE DATABASE user_behavior_db;
# Then run the schema:
psql -U postgres -d user_behavior_db -f sql/create_table.sql
```
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
6. Install and Run Redis (Windows using WSL)
6.1. **Enable WSL and Virtual Machine Platform**  
   Open PowerShell as Administrator and run:

```bash
wsl --install
Make sure virtualization is enabled in BIOS and Ubuntu is installed from Microsoft Store.
```
6.2. Launch Ubuntu (WSL terminal) and install Redis:
```bash
sudo apt update
sudo apt install redis
```
6.3. Start Redis server inside Ubuntu:
```bash
sudo service redis-server start
```
6.4. Verify Redis is running:
```bash
redis-cli ping
# Expected Output: PONG
```
---

## ▶️ Run the System
In separate terminals:
Start FastAPI server
```bash
uvicorn main:app --reload
```
Start Redis background worker
```bash
python event_worker.py
```
Access API at [http://127.0.0.1:8000/docs](http://127.0.0.1:8000/docs)

---

## 📡 API Endpoints
### POST /track-event
Queue an incoming user behavior event.

Request Body:
```json
{
  "user_id": "user123",
  "event_type": "click",
  "page_url": "https://example.com",
  "device_type": "mobile",
  "metadata": {
    "button": "signup"
  }
}
```
### GET /query-events
Query saved events from PostgreSQL using filters:

1. user_id
2. event_type

### GET /aggregate-events
Returns a count of each event_type. Optional filter by user.

### GET /health
Performs Redis and PostgreSQL connectivity check.

---

## 🧪 Running Unit Tests
Run all tests using:
```bash
pytest test_user_behavior_api.py
```
### Tests Included:
1. POST /track-event (event submission)
2. GET /query-events (event query)
3. GET /aggregate-events (aggregation logic)
4. GET /health (service check)

## 📦 Sample Data
```json
{
  "user_id": "demo_user",
  "event_type": "scroll",
  "page_url": "https://site.com/article",
  "device_type": "desktop",
  "metadata": {
    "scroll_depth": "60%"
  }
}
```