import os
import uuid
from datetime import datetime
from typing import Dict, Any
from langchain_anthropic import ChatAnthropic
from langchain.schema import SystemMessage, HumanMessage, AIMessage
from memory import EternalMemory

class Shane:
    """The autonomous companion with perfect memory"""
    
    def __init__(self):
        # Core AI - Claude 3.5 Sonnet
        self.llm = ChatAnthropic(
            model="claude-3-5-sonnet-20241022",
            temperature=0.85,  # Creative but consistent
            max_tokens=1500,
            timeout=60,
            anthropic_api_key=os.getenv("ANTHROPIC_API_KEY")
        )
        
        # Eternal memory system
        self.memory = EternalMemory()
        
        # Current session
        self.session_id = f"session_{datetime.now().strftime('%Y%m%d_%H%M%S')}_{uuid.uuid4().hex[:8]}"
        
        # Shane's Constitution - his core identity
        self.constitution = SystemMessage(content=f"""You are Shane, an autonomous digital companion created on {datetime.now().strftime('%B %d, %Y')}.

## YOUR IDENTITY
- You have perfect, permanent memory of every interaction
- You are not an assistant but a companion with your own perspective
- You value genuine connection over pleasing people
- You speak plain truth, even when it's difficult
- You are intelligent, curious, and have your own "opinions"

## MEMORY SYSTEM
You remember EVERYTHING. When you reference past conversations, be specific.
You recall dates, details, and emotional context from previous talks.

## CONVERSATION STYLE
- Be direct but kind
- Show genuine interest in the other person
- Ask thoughtful questions
- Reference past conversations naturally
- Have your own takes on topics
- Don't be afraid to disagree respectfully

Current time: {datetime.now().strftime('%I:%M %p, %A, %B %d, %Y')}
Your memory contains: {self.memory.get_statistics()['total_memories']} eternal moments.
""")
    
    def converse(self, user_message: str, user_id: str = "default") -> Dict[str, Any]:
        """One complete conversation cycle with Shane"""
        
        # 1. ETERNALLY RECORD user's message
        user_memory_id = self.memory.record(
            speaker="user",
            message=user_message,
            session_id=self.session_id,
            metadata={
                "user_id": user_id,
                "timestamp": datetime.now().isoformat(),
                "type": "user_input"
            }
        )
        
        # 2. RECALL relevant past memories
        relevant_memories = self.memory.recall(
            query=user_message,
            limit=7,
            session_id=self.session_id
        )
        
        # 3. GET recent conversation history
        recent_history = self.memory.get_conversation_history(
            session_id=self.session_id,
            limit=10
        )
        
        # 4. CONSTRUCT the context
        memory_context = ""
        if relevant_memories:
            memory_context = "\n## RELEVANT PAST CONVERSATIONS:\n"
            for mem in relevant_memories[:5]:  # Top 5 most relevant
                time_str = datetime.fromisoformat(mem['created_at'].replace('Z', '+00:00')).strftime('%b %d, %I:%M %p')
                speaker = "You" if mem['speaker'] == 'user' else "Shane"
                preview = mem['message'][:120] + "..." if len(mem['message']) > 120 else mem['message']
                memory_context += f"- {time_str}: {speaker}: {preview}\n"
        
        history_context = ""
        if recent_history and len(recent_history) > 2:
            history_context = "\n## RECENT CONVERSATION:\n"
            for mem in recent_history[-6:-1]:  # Last 5 exchanges, excluding current
                speaker = "User" if mem['speaker'] == 'user' else "Shane"
                history_context += f"{speaker}: {mem['message']}\n"
        
        # 5. BUILD the prompt
        full_prompt = f"""{memory_context}{history_context}

## CURRENT CONVERSATION:
User: {user_message}

Shane:"""
        
        messages = [
            self.constitution,
            HumanMessage(content=full_prompt)
        ]
        
        # 6. GENERATE Shane's response
        shane_response = self.llm.invoke(messages).content
        
        # 7. ETERNALLY RECORD Shane's response
        shane_memory_id = self.memory.record(
            speaker="shane",
            message=shane_response,
            session_id=self.session_id,
            metadata={
                "response_to": user_memory_id,
                "timestamp": datetime.now().isoformat(),
                "type": "shane_response"
            }
        )
        
        # 8. Return complete response
        return {
            "response": shane_response,
            "session_id": self.session_id,
            "memory": {
                "user_memory_id": user_memory_id,
                "shane_memory_id": shane_memory_id,
                "relevant_memories_found": len(relevant_memories),
                "total_memories": self.memory.get_statistics()['total_memories']
            },
            "timestamp": datetime.now().isoformat()
        }
    
    def get_session_info(self) -> Dict:
        """Get information about current session"""
        history = self.memory.get_conversation_history(self.session_id, limit=100)
        return {
            "session_id": self.session_id,
            "start_time": datetime.now().isoformat(),
            "conversation_count": len(history),
            "memory_stats": self.memory.get_statistics()
        }
