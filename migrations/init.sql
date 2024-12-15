-- migrations/init.sql

CREATE TABLE IF NOT EXISTS users (
    id SERIAL PRIMARY KEY,
    username VARCHAR(255) UNIQUE NOT NULL,
    hashed_password VARCHAR(255) NOT NULL,
    created_at TIMESTAMP DEFAULT NOW()
);

CREATE TABLE IF NOT EXISTS messages (
    id SERIAL PRIMARY KEY,
    sender_id INT REFERENCES users(id) ON DELETE CASCADE,
    recipient_id INT REFERENCES users(id) ON DELETE CASCADE,
    content TEXT NOT NULL,
    timestamp TIMESTAMP DEFAULT NOW(),
    status VARCHAR(50) DEFAULT 'sent'
);

CREATE INDEX IF NOT EXISTS idx_messages_recipient ON messages(recipient_id);
CREATE INDEX IF NOT EXISTS idx_messages_sender ON messages(sender_id);
