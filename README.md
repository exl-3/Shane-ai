# Shane - The Autonomous Companion

Shane is an AI companion with perfect, eternal memory.

## Features
- 🧠 **Perfect Memory**: Remembers every conversation forever
- 🔍 **Semantic Recall**: Finds related conversations by meaning
- 🤖 **Claude 3.5 Intelligence**: State-of-the-art conversational AI
- ☁️ **Cloud Native**: Runs entirely in the cloud
- 📱 **Mobile Ready**: REST API for any mobile app

## Deployment

1. **Set up Supabase**:
   - Create project at [supabase.com](https://supabase.com)
   - Run `supabase_setup.sql` in SQL Editor
   - Get URL and service_role key

2. **Get API Keys**:
   - [Anthropic Claude](https://console.anthropic.com)
   - [OpenAI](https://platform.openai.com/api-keys) (for embeddings)

3. **Deploy to Railway**:
   - Connect GitHub repo
   - Add environment variables
   - Deploy

## API Endpoints

- `GET /` - Service status
- `POST /converse` - Talk to Shane
- `GET /memory/stats` - Memory statistics
- `POST /memory/recall` - Search memories

## Environment Variables
