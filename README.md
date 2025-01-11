# special-chatt-robot

![UI of the ChatBot](chat-interface-app.png)

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
   git clone https://github.com//mistral-chatbot.git
   cd mistral-chatbot

