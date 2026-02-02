import os
import json
from datetime import datetime
from typing import List, Dict, Any, Optional
from supabase import create_client, Client
from openai import OpenAI

class EternalMemory:
    """Shane's immortal memory core - never forgets anything"""
    
    def __init__(self):
        # Connect to Supabase
        self.supabase: Client = create_client(
            os.getenv("SUPABASE_URL"),
            os.getenv("SUPABASE_SERVICE_ROLE_KEY")  # Note: SERVICE_ROLE key, not anon
        )
        
        # OpenAI for embeddings
        self.embedding_client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
    
    def _create_embedding(self, text: str) -> List[float]:
        """Create vector embedding for text"""
        response = self.embedding_client.embeddings.create(
            model="text-embedding-3-small",
            input=text
        )
        return response.data[0].embedding
    
    def record(self, speaker: str, message: str, session_id: str, metadata: Dict = None) -> str:
        """
        Record a moment permanently. Returns memory ID.
        This is immutable - once written, never deleted.
        """
        embedding = self._create_embedding(message)
        
        memory_data = {
            "speaker": speaker,
            "message": message,
            "embedding": embedding,
            "session_id": session_id,
            "metadata": metadata or {"type": "conversation", "version": 1}
        }
        
        result = self.supabase.table("eternal_memory").insert(memory_data).execute()
        
        if not result.data:
            raise Exception("Failed to record memory")
        
        return result.data[0]["id"]
    
    def recall(self, query: str, limit: int = 10, session_id: Optional[str] = None) -> List[Dict]:
        """
        Recall relevant memories across all time.
        Uses semantic search to find related conversations.
        """
        query_embedding = self._create_embedding(query)
        
        result = self.supabase.rpc(
            "match_memories",
            {
                "query_embedding": query_embedding,
                "match_count": limit,
                "session_filter": session_id
            }
        ).execute()
        
        return result.data if result.data else []
    
    def get_conversation_history(self, session_id: str, limit: int = 50) -> List[Dict]:
        """Get chronological conversation history for a session"""
        result = self.supabase.table("eternal_memory") \
            .select("*") \
            .eq("session_id", session_id) \
            .order("created_at", desc=True) \
            .limit(limit) \
            .execute()
        
        return list(reversed(result.data)) if result.data else []
    
    def get_statistics(self) -> Dict:
        """Get memory statistics"""
        result = self.supabase.table("eternal_memory") \
            .select("id", count="exact") \
            .execute()
        
        return {
            "total_memories": result.count or 0,
            "status": "eternal"
        }
