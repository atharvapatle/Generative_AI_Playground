# 🤖 Multi-Model Conversational AI Playground

Welcome to the **Conversational AI Playground**, an interactive and highly customizable chat application built with Python, Streamlit, and LangChain. This project allows you to experiment with various leading Large Language Models (LLMs) like Google's **Gemini**, Meta's **LLaMA**, and **Mistral**, all within a single, intuitive interface.

What sets this playground apart is its dynamic nature. You can switch between different AI models and "personas" on the fly, adjusting parameters like creativity (temperature) and conversational memory to tailor the AI's behavior to your specific needs. It’s the ultimate sandbox for exploring the frontiers of conversational AI\!


## ✨ Key Features

  * **🧠 Multi-Model Integration:** Seamlessly switch between different LLMs (`Gemini`, `LLaMA`, `Mistral`) powered by Google and OpenRouter.
  * **🎭 Dynamic Persona Switching:** Change the AI's personality instantly. Choose from a helpful `Assistant`, a `Creative` writer, an expert `Coder`, or a `Casual` friend.
  * **🎛️ Real-Time Parameter Control:**
      * **Temperature:** Fine-tune the AI's creativity, from focused and deterministic to imaginative and random.
      * **Memory Window:** Control how many past messages the AI remembers, allowing for deeper contextual conversations.
  * **📊 Live Statistics:** Keep an eye on the conversation's stats, including the current model, persona, temperature, and total messages.
  * **🔧 Effortless Configuration:** A clean, user-friendly sidebar allows for easy configuration of all settings.
  * **📥 Chat Export:** Download your conversation history as a CSV file for analysis or record-keeping.
  * **✅ Robust Backend:** Built with LangChain for powerful and maintainable conversation management.

## 🛠️ Tech Stack

This project is built with a modern, powerful stack:

  * **Backend:** Python
  * **Application Framework:** Streamlit
  * **AI/LLM Orchestration:** LangChain
  * **LLM Providers:** Google Gemini API, OpenRouter API
  * **Core Libraries:** `langchain-openai`, `langchain-google-genai`, `python-dotenv`

## 📂 Project Structure

The project is organized into modular and easy-to-understand files:

```
Gemini/
│
├── .env                # For storing your secret API keys
├── app.py              # Main Streamlit application file (UI and logic)
├── conversation.py     # Core ConversationManager class for handling chat logic
├── models.py           # ModelManager class for integrating and switching LLMs
├── prompt.py           # Manages the persona-based system prompts
└── requirements.txt    # List of all Python dependencies
```

## 🚀 Getting Started

Follow these simple steps to get the Conversational AI Playground running on your local machine.

### 1\. Prerequisites

  * Python 3.8 or higher
  * An IDE like VS Code
  * API keys for Google and OpenRouter

### 2\. Clone the Repository

```bash
git clone https://your-repository-url.git
cd Gemini
```

### 3\. Set Up a Virtual Environment

It's highly recommended to use a virtual environment to keep dependencies isolated.

```bash
# For Windows
python -m venv venv
venv\Scripts\activate

# For macOS/Linux
python3 -m venv venv
source venv/bin/activate
```

### 4\. Install Dependencies

Install all the required packages using the `requirements.txt` file.

```bash
pip install -r requirements.txt
```

### 5\. Configure Your API Keys

Create a file named `.env` in the root directory of the project. Copy the contents of the `.env.example` (or the file you provided) and paste in your actual API keys.

Your `.env` file should look like this:

```
GOOGLE_API_KEY='YOUR_GOOGLE_API_KEY'
OPENAI_API_KEY="YOUR_OPENROUTER_API_KEY"
OPENAI_API_BASE="https://openrouter.ai/api/v1"
# ... other keys if needed
```

### 6\. Run the Application

You're all set\! Launch the Streamlit application with the following command:

```bash
streamlit run app.py
```

Your web browser should automatically open to the application's interface. Now you can start chatting\!

## 💡 How to Use

1.  **Select a Model:** Use the "Choose Model" dropdown in the sidebar to pick between Gemini, LLaMA, or Mistral.
2.  **Choose a Persona:** Select a personality for the AI from the "Choose Persona" dropdown.
3.  **Adjust Parameters:** Use the sliders to set the desired **Temperature** and **Memory Window**.
4.  **Start Chatting:** Type your message in the input box at the bottom and press Enter\!
