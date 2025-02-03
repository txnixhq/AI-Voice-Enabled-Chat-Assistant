# AI-Voice-Enabled-Chat-Assistant

## Overview
This project is an AI-powered voice assistant that enables real-time interaction with users via a WebSocket-based interface. It leverages OpenAI's language models for text-based responses and text-to-speech (TTS) for voice output. The system is built to handle multi-turn conversations, process user messages efficiently, and return responses in both text and voice formats.

## Features
### Current Features:
- **Real-time WebSocket Communication:** Enables seamless bidirectional communication between the client and the backend.
- **Text-Based AI Responses:** Utilizes OpenAI's API to generate text responses based on user input.
- **Voice Output with TTS:** Converts AI-generated responses into speech using OpenAI's text-to-speech functionality.
- **Chunked Audio Streaming:** Streams audio in small chunks for smooth playback.
- **Interactive Web UI:** Built with Streamlit to facilitate an easy-to-use interface for message input and response playback.
- **FastAPI Backend:** Handles WebSocket connections, AI model interactions, and audio streaming.
- **Cross-Origin Resource Sharing (CORS) Support:** Allows secure communication across different platforms.

### Future Enhancements:
- **Neo4j Integration:** Implementing a graph-based database to retrieve relevant structured information for enhanced AI responses.
- **LangChain and Pinecone RAG Implementation:** Using retrieval-augmented generation (RAG) to provide highly contextual and accurate responses based on external knowledge bases.
- **Adaptive AI Responses:** Fine-tuning the AI to dynamically ask follow-up questions based on user queries.
- **Multi-Platform Interaction:** Expanding support to voice-based assistants and mobile applications.
- **Personalized AI Training:** Enabling customization and fine-tuning of responses based on specific user needs and requirements.

## Tech Stack
- **Frontend:** Streamlit (Python)
- **Backend:** FastAPI (Python)
- **AI & NLP:** OpenAI API (ChatGPT & TTS models)
- **Database (Future):** Neo4j for knowledge retrieval
- **Vector Search (Future):** Pinecone for efficient document retrieval
- **Model Chaining:** LangChain for enhanced query processing
- **WebSocket Communication:** Real-time messaging between frontend and backend
- **Deployment:** To be hosted on a cloud platform (TBD)

## How to Run
### Prerequisites:
- Python 3.8+
- OpenAI API key
- Streamlit
- FastAPI
- WebSockets
- LangChain, Pinecone (Future)

### Installation:
```bash
# Clone the repository
git clone https://github.com/your-repo-name.git
cd your-repo-name

# Install dependencies
pip install -r requirements.txt
```

### Running the Application:
#### Backend:
```bash
uvicorn backend:app --host 0.0.0.0 --port 8000
```

#### Frontend:
```bash
streamlit run frontend.py
```

### Usage:
1. Open the Streamlit app in a browser.
2. Type a message and send it.
3. The AI will generate a response and play the audio output.

## Contributing
Contributions are welcome! Feel free to submit issues or pull requests to improve the project.

## License
This project is licensed under the MIT License.
