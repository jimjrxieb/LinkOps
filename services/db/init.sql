CREATE TABLE IF NOT EXISTS orbs (
    id SERIAL PRIMARY KEY,
    title TEXT,
    category TEXT,
    agent TEXT,
    content JSONB,
    recurrence TEXT DEFAULT 'low',
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE IF NOT EXISTS runes (
    id SERIAL PRIMARY KEY,
    orb_id INT REFERENCES orbs(id),
    script TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE IF NOT EXISTS logs (
    id SERIAL PRIMARY KEY,
    task_id TEXT,
    agent TEXT,
    status TEXT,
    result JSONB,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE IF NOT EXISTS approvals (
    id SERIAL PRIMARY KEY,
    orb_id INT,
    rune_id INT,
    status TEXT DEFAULT 'pending',
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE IF NOT EXISTS capabilities (
    agent TEXT PRIMARY KEY,
    tools JSONB,
    last_updated TIMESTAMP DEFAULT CURRENT_TIMESTAMP
); 