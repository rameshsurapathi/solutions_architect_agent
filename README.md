# AI Solutions Architect

AI Solutions Architect is an advanced web-based assistant that provides robust, scalable, secure, and reliable cloud infrastructure solutions. Powered by state-of-the-art AI and LLMs, it delivers expert guidance for AWS, Azure, and Google Cloud platforms, emulating the knowledge and reasoning of a 25+ year veteran cloud architect.

## Features

- **Conversational Web Interface:**
  - Modern, responsive chat UI for seamless interaction.
  - Quick-select sample questions and architecture topics.
  - Markdown and HTML rendering for clear, blog-style answers.
  - **NEW: Persistent Chat Memory** - Automatically loads last 5 chat interactions when users revisit the page.
  - **NEW: Chat History Management** - View, manage, and delete complete chat history with modal interface.
  - **NEW: Session Continuity** - "New Chat", "View Chat History", and "Delete Chat History" controls.
  - **NEW: PDF Export** - Save AI responses as formatted PDF documents.

- **Expert Cloud Guidance:**
  - Detailed, actionable solutions for cloud architecture, security, disaster recovery, and more.
  - Explanations for any cloud service, with best practices and real-world examples.
  - Step-by-step architecture plans, CLI/console commands, and documentation references.

- **Multi-Cloud Support:**
  - AWS, Azure, and Google Cloud expertise.
  - Cross-cloud comparisons and migration advice.

- **AI-Powered Responses:**
  - Uses LLMs (OpenAI, Gemini, etc.) with a custom system prompt for expert, blog-style output.
  - Intelligent response caching with Firestore for speed and efficiency.
  - **NEW: User-Specific Chat History** - Stores all conversations per user using browser fingerprinting.
  - **NEW: Context-Aware Conversations** - Uses previous chat history to provide contextual responses.
  - Rate-limits chat requests to prevent abuse.

- **Extensible Backend:**
  - Built with FastAPI for easy API integration and deployment.
  - Modular agent logic using LangChain and LangGraph.
  - Prompts and agent logic separated for easy customization.
  - **NEW: RESTful Chat History APIs** - GET, POST, DELETE endpoints for chat history management.
  - **NEW: Browser Fingerprinting** - Anonymous user identification without registration.
  - **NEW: Firestore Chat Storage** - Persistent chat history stored in `sa-chat-history` collection.

## How It Works

1. **User visits the page** - Last 5 chat interactions are automatically loaded for session continuity
2. **User submits a question** - Via the modern chat UI with quick-select topics
3. **Backend checks cache** - Firestore is queried for existing responses to improve speed
4. **AI generates response** - If not cached, the AI agent creates a detailed, blog-style answer
5. **Response is stored** - All conversations are saved to user-specific chat history
6. **Beautiful rendering** - Markdown-formatted responses with syntax highlighting

## Requirements

- Python 3.9+
- FastAPI
- Uvicorn
- LangChain, LangGraph
- Google Firestore (for caching)
- Node.js (optional, for frontend tooling)

## Setup

1. Clone the repository.
2. Install Python dependencies:
   ```sh
   pip install -r requirements.txt
   ```
3. Set up Google Firestore and authentication (see Google Cloud docs).
4. Set your LLM API keys in `.env` (e.g., `OPENAI_API_KEY`).
5. Run the FastAPI server:
   ```sh
   uvicorn app:app --reload
   ```
6. Open your browser at [http://localhost:8000](http://localhost:8000)

## Customization

- **Prompts:** Edit `src/prompts.py` to change the agent’s style or expertise.
- **Agent Logic:** Extend `src/ai_agent.py` for tool use, retrieval, or multi-step workflows.
- **Frontend:** Update `templates/index.html` and `static/` for UI/UX changes.

## Architecture

- **Frontend:** Pure HTML, CSS, and JavaScript with a modern, responsive design
- **Backend:** FastAPI with RESTful endpoints for chat and history management
- **AI Engine:** LangChain/LangGraph for intelligent conversation flow
- **Database:** Google Firestore for persistent chat history and response caching
- **User Identity:** Browser fingerprinting for anonymous user identification

## API Endpoints

- `POST /chat` - Send a message and get AI response
- `GET /chat/history` - Retrieve user's chat history
- `DELETE /chat/history` - Delete all chat history for user
- `GET /` - Serve the main chat interface

## Technical Features

- **Persistent Chat Memory:** Automatically loads last 5 conversations on page revisit
- **Context-Aware Responses:** AI maintains conversation context across sessions
- **Intelligent Caching:** Firestore-based response caching for improved performance
- **Browser Fingerprinting:** Anonymous user identification using SHA-256 hashing
- **Error Handling:** Robust error handling with user-friendly fallbacks
- **Rate Limiting:** Built-in protection against abuse
- **Debug Logging:** Comprehensive logging for troubleshooting and monitoring

## Roadmap
- Image generation for architecture diagrams
- Integration with cloud provider APIs for live recommendations
- More advanced multi-step reasoning and tool use
- Advanced user analytics and conversation insights

## License
MIT
