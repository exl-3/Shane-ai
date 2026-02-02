-- Enable vector extension
CREATE EXTENSION IF NOT EXISTS vector;

-- Eternal memory table
CREATE TABLE eternal_memory (
    id BIGSERIAL PRIMARY KEY,
    created_at TIMESTAMPTZ DEFAULT NOW() NOT NULL,
    speaker TEXT NOT NULL CHECK (speaker IN ('user', 'shane')),
    message TEXT NOT NULL,
    embedding vector(1536),
    session_id TEXT,
    metadata JSONB DEFAULT '{}'::jsonb
);

-- Function for semantic search
CREATE OR REPLACE FUNCTION match_memories(
    query_embedding vector(1536),
    match_count INT DEFAULT 10,
    session_filter TEXT DEFAULT NULL
)
RETURNS TABLE (
    id BIGINT,
    speaker TEXT,
    message TEXT,
    created_at TIMESTAMPTZ,
    similarity FLOAT,
    session_id TEXT
)
LANGUAGE SQL STABLE
AS $$
    SELECT
        id,
        speaker,
        message,
        created_at,
        1 - (embedding <=> query_embedding) AS similarity,
        session_id
    FROM eternal_memory
    WHERE (session_filter IS NULL OR session_id = session_filter)
    ORDER BY embedding <=> query_embedding
    LIMIT match_count;
$$;

-- Index for performance
CREATE INDEX idx_eternal_memory_embedding ON eternal_memory USING ivfflat (embedding vector_cosine_ops);
CREATE INDEX idx_eternal_memory_created ON eternal_memory (created_at DESC);
CREATE INDEX idx_eternal_memory_session ON eternal_memory (session_id);
