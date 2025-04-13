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