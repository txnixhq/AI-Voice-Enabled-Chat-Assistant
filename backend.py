import asyncio
import io
import json
import logging
import uuid
import os

from fastapi import FastAPI, WebSocket, WebSocketDisconnect
from fastapi.middleware.cors import CORSMiddleware
from openai import OpenAI
from dotenv import load_dotenv  # For securely loading environment variables

# ------------------------
# Configuration & Setup
# ------------------------

# Load environment variables from a .env file (Ensure you have a .env file with OPENAI_API_KEY)
load_dotenv()

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = FastAPI()

# Configure CORS (Adjust as needed)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Securely fetch the OpenAI API key from environment variables
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

if not OPENAI_API_KEY:
    raise ValueError("Missing OpenAI API key! Ensure it is set in the environment variables.")

# Initialize OpenAI client
client = OpenAI(api_key=OPENAI_API_KEY)

# ------------------------
# Helper Functions
# ------------------------

def generate_chat_completion(user_message: str) -> str:
    """
    Generates a response from OpenAI using the user_message as context.
    
    :param user_message: The user's message string
    :return: The response text from the LLM
    """
    try:
        messages = [
            {"role": "user", "content": user_message}
        ]

        response = client.chat.completions.create(
            model="gpt-4o",
            messages=messages,
            temperature=0.11,
            n=1
        )
        reply_text = response.choices[0].message.content.strip()
        logger.info(f"OpenAI response: {reply_text}")
        return reply_text

    except Exception as e:
        logger.error(f"OpenAI API error: {e}")
        return "I'm sorry, I couldn't process your request at the moment."

async def stream_tts_audio(reply_text: str, websocket: WebSocket):
    """
    Streams TTS audio (in chunks) to the WebSocket client using OpenAI TTS.

    :param reply_text: The text to be converted to speech
    :param websocket: The active WebSocket connection
    """
    try:
        with client.audio.speech.with_streaming_response.create(
            model="tts-1",
            voice="nova",
            input=reply_text,
            response_format="mp3"
        ) as response:
            for chunk in response.iter_bytes(1048):
                await websocket.send_bytes(chunk)
                await asyncio.sleep(0.01)

        logger.info("Converted text to speech successfully")

    except Exception as e:
        logger.error(f"TTS conversion error: {e}")
        return

# ------------------------
# WebSocket Endpoint
# ------------------------

@app.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    """
    WebSocket endpoint for handling user messages and returning TTS audio from OpenAI.

    Each message from the client is:
       1) Received via WebSocket
       2) Sent to the LLM for a response
       3) The LLM response is streamed back as audio chunks
    """
    await websocket.accept()
    logger.info("WebSocket connection accepted")

    try:
        while True:
            data = await websocket.receive_text()
            logger.info(f"Received data: {data}")

            try:
                message_data = json.loads(data)
                user_message = message_data.get('message', "")
                conversation_id = message_data.get('conversation_id', str(uuid.uuid4()))
            except json.JSONDecodeError:
                user_message = data
                conversation_id = str(uuid.uuid4())
                logger.warning("Failed to decode JSON. Generated a new conversation ID.")

            logger.info(f"Conversation ID: {conversation_id}, User Message: {user_message}")

            reply_text = generate_chat_completion(user_message)
            await stream_tts_audio(reply_text, websocket)

    except WebSocketDisconnect:
        logger.info("Client disconnected")
    except Exception as e:
        logger.error(f"Unhandled error: {e}")
