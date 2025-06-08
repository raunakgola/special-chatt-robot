import streamlit as st
from ctransformers import AutoConfig, AutoModelForCausalLM, Config
from typing import List
import logging
import time

# Set up logging to save logs to a file
logging.basicConfig(
    filename='app.log',  # Save logs in app.log
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s"
)
logger = logging.getLogger(__name__)

# Constants
# MODEL_NAME = "TheBloke/Mistral-7B-Instruct-v0.1-GGUF"
# MODEL_FILE = "mistral-7b-instruct-v0.1.Q6_K.gguf"
MODEL_PATH = "/root/.cache/ctransformers/models/TheBloke/Mistral-7B-Instruct-v0.1-GGUF"
MODEL_FILE = "mistral-7b-instruct-v0.1.Q6_K.gguf"
# Initialize global dictionary for models
llms = {}

# Apply template to format chat history for the model
def apply_template(history: List[dict], system_instructions: str) -> str:
    """
    Formats the conversation history into a format compatible with the model's instructions.
    """
    prompt = f"<s>[INST]{system_instructions}"
    chat_history = history[-1]["message"]
    prompt += f" {chat_history}[/INST]"
    return prompt


# Load the model
def load_model():
    """
    Loads the Mistral LLM model using ctransformers. Returns the model instance.
    """
    config = AutoConfig(
        config=Config(
            temperature=st.session_state.temperature,
            max_new_tokens=st.session_state.max_new_tokens,
            context_length=st.session_state.context_length,
            gpu_layers=st.session_state.gpu_layers,
        )
    )
    model = AutoModelForCausalLM.from_pretrained(
        MODEL_PATH,
        model_file=MODEL_FILE,
        config=config,
    )
    return model


# Generate a response using the model
def generate_response(prompt: str):
    try:
        llm = st.session_state.llms["mistral"]
        response = llm(prompt, stream=True)
        message = "".join([token for token in response])
        return message
    except Exception as e:
        logger.error("Error generating response: %s", e)
        return "I'm sorry, I encountered an issue processing your request. Could you please rephrase?"

# Initialize Streamlit app state
if "conversation_history" not in st.session_state:
    st.session_state.conversation_history = []
if "llms" not in st.session_state:
    st.session_state.llms = {}
if "temperature" not in st.session_state:
    st.session_state.temperature = 0.7
if "max_new_tokens" not in st.session_state:
    st.session_state.max_new_tokens = 256
if "context_length" not in st.session_state:
    st.session_state.context_length = 2048
if "gpu_layers" not in st.session_state:
    st.session_state.gpu_layers = 0
if "system_instructions" not in st.session_state:
    st.session_state.system_instructions = "You're a coder assistant."


# Initialize chat history in session state
if "chat_history" not in st.session_state:
    st.session_state.chat_history = {}
if "current_chat" not in st.session_state:
    st.session_state.current_chat = []

# Function to start a new chat
def start_new_chat():
    chat_name = f"Chat {len(st.session_state.chat_history) + 1}"
    st.session_state.chat_history[chat_name] = []
    st.session_state.current_chat = chat_name

#  Steaming the text
def stream_data(_LOREM_IPSUM:str):
    for word in _LOREM_IPSUM.split(" "):
        yield word + " "
        time.sleep(0.02)

# Streamlit UI
st.set_page_config(page_title="ChatBot", page_icon="🤖", layout="wide")

# Sidebar Configuration
with st.sidebar:
    # Start a new chat
    if st.button("Start New Chat 💬"):
        start_new_chat()
    st.header("Configuration")
    st.session_state.system_instructions = st.text_input(
        "System Instructions",
        value=st.session_state.system_instructions,
        help="Set the system's instructions for the chatbot."
    )
    st.session_state.temperature = st.slider("Temperature", 0.1, 1.0, 0.7, 0.1)
    st.session_state.max_new_tokens = st.number_input("Max New Tokens", 50, 1024, 256, 50)
    st.session_state.context_length = st.number_input("Context Length", 1024, 4096, 2048, 256)
    st.session_state.gpu_layers = st.number_input("GPU Layers", 0, 12, 0, 1,
                                                  help="Set GPU layers (0 if no GPU available).",)

    # Load Model
    if "mistral" not in st.session_state.llms:
        with st.spinner("Downloading and loading the model..."):
            try:
                st.session_state.llms["mistral"] = load_model()
                st.success("Model loaded successfully!")
            except Exception as e:
                st.error(f"Failed to load model: {e}")

    # Display existing chats
    st.write("### Saved Chats")
    for chat_name in st.session_state.chat_history:
        if st.button(chat_name):
            st.session_state.current_chat = chat_name

# Main Chat Interface
st.title("Mistral Chatbot 🤖")
# Ensure a chat is initialized
if not st.session_state.current_chat:
    start_new_chat()

current_chat = st.session_state.current_chat
chat_history = st.session_state.chat_history[current_chat]

# Display chat history
for message in chat_history:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# Prompt for user input and save to chat history
if user_input := st.chat_input("Type your message..."):
    st.session_state.conversation_history.append({"user": "User", "message": user_input})
    # Immediately display the user's query
    with st.chat_message("user"):
        st.write(user_input)
    chat_history.append({"role": "user", "content": user_input})
    prompt = apply_template(st.session_state.conversation_history, st.session_state.system_instructions)

    # Generate the bot's response with error handling
    response = generate_response(prompt)
    with st.chat_message("assistant"):
        st.write_stream(stream_data(response))
    chat_history.append({"role": "assistant", "content": response})

    # Save chat history to a file
    try:
        with open("responses.txt", "w", encoding="utf-8") as file:
            for chat_name, messages in st.session_state.chat_history.items():
                file.write(f"{chat_name}:\n")
                for message in messages:
                    file.write(f"  {message}\n")
    except Exception as e:
        logger.error("Error saving chat history: %s", e)
