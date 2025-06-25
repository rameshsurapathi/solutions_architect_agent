# AI Solutions Architect

AI Solutions Architect is an advanced web-based assistant that provides robust, scalable, secure, and reliable cloud infrastructure solutions. Powered by state-of-the-art AI and LLMs, it delivers expert guidance for AWS, Azure, and Google Cloud platforms, emulating the knowledge and reasoning of a 25+ year veteran cloud architect.

## Features

- **Conversational Web Interface:**
  - Modern, responsive chat UI for seamless interaction.
  - Quick-select sample questions and architecture topics.
  - Markdown and HTML rendering for clear, blog-style answers.

- **Expert Cloud Guidance:**
  - Detailed, actionable solutions for cloud architecture, security, disaster recovery, and more.
  - Explanations for any cloud service, with best practices and real-world examples.
  - Step-by-step architecture plans, CLI/console commands, and documentation references.

- **Multi-Cloud Support:**
  - AWS, Azure, and Google Cloud expertise.
  - Cross-cloud comparisons and migration advice.

- **AI-Powered Responses:**
  - Uses LLMs (OpenAI, Gemini, etc.) with a custom system prompt for expert, blog-style output.
  - Caches responses with Redis for speed and efficiency.
  - Rate-limits chat requests to prevent abuse.

- **Extensible Backend:**
  - Built with FastAPI for easy API integration and deployment.
  - Modular agent logic using LangChain and LangGraph.
  - Prompts and agent logic separated for easy customization.

## How It Works

1. **User submits a cloud architecture question via the chat UI.**
2. **The backend checks Redis for a cached answer.**
3. **If not cached, the AI agent generates a detailed, blog-style response using the latest LLMs and a custom prompt.**
4. **The response is rendered in the chat with beautiful formatting for easy reading.**

## Requirements

- Python 3.9+
- FastAPI
- Uvicorn
- LangChain, LangGraph
- Redis (for caching)
- Node.js (optional, for frontend tooling)

## Setup

1. Clone the repository.
2. Install Python dependencies:
   ```sh
   pip install -r requirements.txt
   ```
3. Start Redis server locally.
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

## Roadmap
- Image generation for architecture diagrams.
- User authentication and chat history.
- Integration with cloud provider APIs for live recommendations.
- More advanced multi-step reasoning and tool use.

## License
MIT
