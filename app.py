import streamlit as st
import streamlit.components.v1 as components

# ------------------
# Helper Functions
# ------------------

def generate_websocket_html(conversation_id: str, expected_chunks: int = 5) -> str:
    """
    Returns an HTML string containing JavaScript that:
      - Establishes a WebSocket connection
      - Sends user messages to the server
      - Buffers and concatenates audio chunks
      - Plays audio when all expected chunks are received
      
    :param conversation_id: Unique conversation identifier sent to the server
    :param expected_chunks: Number of audio chunks expected from the server
    :return: A formatted HTML + JS string
    """
    return f"""
    <div id="websocket-status">Connecting to WebSocket...</div>
    <div id="js-status"></div>
    <input type="text" id="user-message" placeholder="Type your message here"
           style="width: 100%; padding: 8px; margin-top: 10px;">
    <button onclick="sendMessage()">Send Message</button>
    <div id="audio-section"></div>
    <button id="play-audio" style="margin-top: 10px;" onclick="playConcatenatedAudio()" disabled>
        Play Concatenated Audio
    </button>
    
    <script>
        let audioChunks = []; // Buffer to store audio chunks
        let receivedChunksCount = 0;
        const expectedChunks = {expected_chunks};  

        console.log("Initializing WebSocket...");
        const ws = new WebSocket("ws://localhost:8000/ws");
        ws.binaryType = 'arraybuffer';

        ws.onopen = () => {{
            console.log("WebSocket connection established");
            document.getElementById("websocket-status").innerText = "WebSocket connected";
            document.getElementById("js-status").innerText = "JavaScript is running.";
            window.myWebSocket = ws;
        }};
        
        ws.onmessage = (event) => {{
            if (typeof event.data === 'string') {{
                console.log("Received text message:", event.data);
                document.getElementById("js-status").innerText = "Received message: " + event.data;
            }} else {{
                console.log("Received binary audio data chunk of length: " + event.data.byteLength);
                bufferAudioChunk(event.data);
            }}
        }};
        
        ws.onclose = () => {{
            console.log("WebSocket connection closed");
            document.getElementById("websocket-status").innerText = "WebSocket disconnected";
            document.getElementById("js-status").innerText = "JavaScript detected WebSocket closure.";
        }};
        
        ws.onerror = (error) => {{
            console.error("WebSocket error:", error);
            document.getElementById("websocket-status").innerText = "WebSocket error";
            document.getElementById("js-status").innerText = "JavaScript detected an error.";
        }};
        
        function sendMessage() {{
            const userMessage = document.getElementById('user-message').value;
            if (window.myWebSocket && window.myWebSocket.readyState === WebSocket.OPEN) {{
                const payload = {{
                    "message": userMessage,
                    "conversation_id": "{conversation_id}"
                }};
                window.myWebSocket.send(JSON.stringify(payload));
                console.log("Sent message:", payload);
                document.getElementById("js-status").innerText = "Message sent: " + userMessage;
            }} else {{
                console.error("WebSocket is not open. ReadyState:", window.myWebSocket.readyState);
                document.getElementById("js-status").innerText = "Cannot send message: WebSocket not open.";
            }}
        }}

        function bufferAudioChunk(audioChunk) {{
            audioChunks.push(audioChunk);
            receivedChunksCount++;
            console.log("Buffered audio chunk, total chunks: " + receivedChunksCount);

            if (receivedChunksCount < expectedChunks) {{
                document.getElementById("play-audio").disabled = true;
            }} else {{
                document.getElementById("play-audio").disabled = false;
            }}
        }}

        function playConcatenatedAudio() {{
            console.log("Concatenating audio chunks...");
            const blob = new Blob(audioChunks, {{ type: 'audio/wav' }});
            const url = URL.createObjectURL(blob);
            console.log("Blob URL created:", url);

            const audioSection = document.getElementById('audio-section');
            audioSection.innerHTML = "";  
            
            const audioElement = document.createElement('audio');
            audioElement.src = url;
            audioElement.controls = true;

            audioSection.appendChild(audioElement);

            audioElement.addEventListener('canplaythrough', () => {{
                audioElement.play().catch((error) => {{
                    console.error("Error playing audio:", error);
                }});
            }});
            
            audioChunks = [];
            receivedChunksCount = 0;
        }}
    </script>
    """


def initialize_websocket_ui(conversation_id: str, height: int = 400, expected_chunks: int = 5):
    """
    Renders the WebSocket HTML/JS snippet within Streamlit, ensuring it's loaded only once.
    
    :param conversation_id: Unique ID used for sending messages to the server
    :param height: The height of the HTML component
    :param expected_chunks: Number of audio chunks expected for each message
    """
    if 'ws_initialized' not in st.session_state:
        components.html(
            generate_websocket_html(conversation_id, expected_chunks=expected_chunks),
            height=height
        )
        st.session_state['ws_initialized'] = True


# ------------------
# Main App
# ------------------

def main():
    st.set_page_config(page_title="WebSocket Test", layout="wide")
    st.title("🔗 OpenAI TTS Test")
    
    # Unique conversation ID for testing
    conversation_id = "test-conversation"
    
    # Initialize the WebSocket UI only once
    initialize_websocket_ui(conversation_id=conversation_id, height=400, expected_chunks=5)
    
    # Inform the user about how to interact
    st.write("Enter a message in the text box (above) and click 'Send Message' to send it to the backend.")

if __name__ == "__main__":
    main()
