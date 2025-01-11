# special-chatt-robot 🤖

![UI of the ChatBot](https://github.com/raunakgola/special-chatt-robot/blob/main/MistralChatbot.mp4)

Mistral Chatbot is a conversational AI application built with Streamlit and the `ctransformers` library. It leverages the Mistral-7B-Instruct model to provide intelligent and interactive responses for various queries.

## Features
- Interactive chat interface with a user-friendly UI.
- Configurable system instructions, temperature, context length, and more.
- Saves chat history locally for easy access and review.
- Streamed response generation for real-time interaction.
- Supports GPU acceleration for faster inference (if available).

---

## Setup

### Prerequisites
- Python 3.8 or higher
- A compatible GPU (optional for GPU layers)
- Required Python libraries:
  - `streamlit`
  - `ctransformers`
  - `typing`
  - `logging`

### Installation

1. Clone the repository:
   ```bash
   git clone https://github.com/raunakgola/special-chatt-robot.git
   cd mistral-chatbot

2. Create a virtual environment:
   ```bash
   python -m venv venv
   source venv/bin/activate   # On Windows, use `venv\Scripts\activate`

3. Install dependencies:
   ```bash
   pip install -r requirements.txt

### Running the Application

1. Start the Streamlit app:
    ```bash
    streamlit run app.py

2. Open the app in your browser at http://localhost:8501.
   
3. Configure settings via the sidebar:
   -`System Instructions`
   -`Temperature`
   -`Max New Tokens`
   -`Context Length`
   -`GPU Layers`

4. Interact with the chatbot by typing messages in the input box.

### File Structure

mistral-chatbot/

├── app.py                # Main application file

├── app.log               # Log file for debugging

├── requirements.txt      # List of dependencies

├── responses.txt         # Chat history saved as text

└── mistral-7b-instruct-v0.1.Q6_K.gguf  # Model file (to be downloaded)

### Configuration Options
  -`System Instructions: Customize the chatbot's personality and behavior.`
  -`Temperature: Adjust randomness in responses (higher = more creative).`
  -`Max New Tokens: Set the maximum length of generated responses.`
  -`Context Length: Define how much context the chatbot retains.`
  -`GPU Layers: Specify the number of layers to offload to the GPU (set to 0 if no GPU is available).`

### Known Issues
  -`Long chat histories may impact performance due to context length limits.`
  -`GPU acceleration requires a compatible CUDA-enabled GPU.`

### Contributing
Contributions are welcome! Please fork the repository and create a pull request.


