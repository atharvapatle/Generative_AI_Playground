# app.py
import streamlit as st
import os
from dotenv import load_dotenv
from conversation import ConversationManager
from models import ModelManager
from prompt import get_available_personas, get_persona_name
import pandas as pd
from datetime import datetime

# Load environment variables
load_dotenv()

# Page configuration
st.set_page_config(
    page_title="🤖 Conversational AI Playground",
    page_icon="🤖",
    layout="wide",
    initial_sidebar_state="expanded"
)

def initialize_session_state():
    """Initialize all session state variables"""
    # Core conversation manager
    if 'conversation_manager' not in st.session_state:
        st.session_state.conversation_manager = ConversationManager(
            persona_key="assistant",
            model_key="llama", 
            temperature=0.7,
            memory_window=10
        )
    
    # UI state
    if 'messages' not in st.session_state:
        st.session_state.messages = []
    
    # Current settings
    if 'current_model' not in st.session_state:
        st.session_state.current_model = "llama"
        
    if 'current_persona' not in st.session_state:
        st.session_state.current_persona = "assistant"
        
    if 'current_temperature' not in st.session_state:
        st.session_state.current_temperature = 0.7
        
    if 'current_memory_window' not in st.session_state:
        st.session_state.current_memory_window = 10
    
    # Stats tracking
    if 'conversation_stats' not in st.session_state:
        st.session_state.conversation_stats = {
            'total_conversations': 0,
            'total_messages': 0,
            'start_time': datetime.now()
        }

def update_model(new_model):
    """Update the current model"""
    if new_model != st.session_state.current_model:
        st.session_state.current_model = new_model
        st.session_state.conversation_manager.update_model(
            new_model, 
            st.session_state.current_temperature
        )
        st.success(f"✅ Switched to {new_model.upper()} model")

def update_persona(new_persona):
    """Update the current persona"""
    if new_persona != st.session_state.current_persona:
        st.session_state.current_persona = new_persona
        st.session_state.conversation_manager.update_persona(new_persona)
        st.success(f"✅ Switched to {get_persona_name(new_persona)} persona")

def update_temperature(new_temperature):
    """Update temperature setting"""
    if new_temperature != st.session_state.current_temperature:
        st.session_state.current_temperature = new_temperature
        st.session_state.conversation_manager.update_temperature(new_temperature)

def sidebar_configuration():
    """Render sidebar configuration panel"""
    
    with st.sidebar:
        st.header("⚙️ Configuration")
        
        # Model Selection
        st.subheader("🧠 Model Selection")
        model_manager = ModelManager()
        available_models = model_manager.get_available_models()
        
        model_options = list(available_models.keys())
        model_names = [available_models[key]["name"] for key in model_options]
        
        selected_model_idx = st.selectbox(
            "Choose Model:",
            range(len(model_options)),
            format_func=lambda x: model_names[x],
            index=model_options.index(st.session_state.current_model),
            key="model_selector"
        )
        
        selected_model = model_options[selected_model_idx]
        update_model(selected_model)
        
        # Display model info
        model_info = available_models[selected_model]
        st.info(f"**{model_info['name']}**\n\n{model_info['description']}")
        
        st.divider()
        
        # Persona Selection
        st.subheader("🎭 Persona Selection")
        personas = get_available_personas()
        
        selected_persona = st.selectbox(
            "Choose Persona:",
            options=list(personas.keys()),
            format_func=lambda x: personas[x]["name"],
            index=list(personas.keys()).index(st.session_state.current_persona),
            key="persona_selector"
        )
        
        update_persona(selected_persona)
        
        st.divider()
        
        # Parameter Controls
        st.subheader("🎛️ Parameters")
        
        # Temperature
        temperature = st.slider(
            "Temperature:",
            min_value=0.0,
            max_value=1.0,
            value=st.session_state.current_temperature,
            step=0.1,
            help="Controls creativity: Lower = focused, Higher = creative",
            key="temperature_slider"
        )
        update_temperature(temperature)
        
        # Memory Window
        memory_window = st.slider(
            "Memory Window:",
            min_value=1,
            max_value=50,
            value=st.session_state.current_memory_window,
            step=1,
            help="Number of previous messages to remember",
            key="memory_slider"
        )
        
        if memory_window != st.session_state.current_memory_window:
            st.session_state.current_memory_window = memory_window
            st.session_state.conversation_manager.update_memory_window(memory_window)
        
        st.divider()
        
        # Statistics
        st.subheader("📊 Statistics")
        stats = st.session_state.conversation_manager.get_stats()
        
        col1, col2 = st.columns(2)
        with col1:
            st.metric("Messages", stats["total_messages"])
            st.metric("Temperature", f"{stats['temperature']:.1f}")
        with col2:
            st.metric("Memory", f"{stats['memory_window']}")
            st.metric("Model", stats["current_model"].upper())
        
        st.divider()
        
        # Action Buttons
        st.subheader("🔧 Actions")
        
        col1, col2 = st.columns(2)
        
        with col1:
            if st.button("🗑️ Clear Chat", use_container_width=True):
                st.session_state.conversation_manager.reset_conversation()
                st.session_state.messages = []
                st.success("✅ Conversation cleared!")
                st.rerun()
        
        with col2:
            if st.button("📊 Export Chat", use_container_width=True):
                export_conversation()

def export_conversation():
    """Export conversation to downloadable format"""
    if st.session_state.messages:
        # Create DataFrame
        df = pd.DataFrame(st.session_state.messages)
        df['timestamp'] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        
        # Convert to CSV
        csv = df.to_csv(index=False)
        
        st.download_button(
            label="💾 Download CSV",
            data=csv,
            file_name=f"chat_export_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv",
            mime="text/csv"
        )
    else:
        st.warning("No conversation to export!")

def main_chat_interface():
    """Render the main chat interface"""
    
    # Header
    st.title("🤖 Conversational AI Playground")
    
    # Current configuration display
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.metric("Model", st.session_state.current_model.upper())
    with col2:
        st.metric("Persona", get_persona_name(st.session_state.current_persona))
    with col3:
        st.metric("Temperature", f"{st.session_state.current_temperature:.1f}")
    with col4:
        st.metric("Memory", f"{st.session_state.current_memory_window}")
    
    st.markdown("---")
    
    # Chat messages container
    chat_container = st.container()
    
    # Display chat messages
    with chat_container:
        for message in st.session_state.messages:
            with st.chat_message(message["role"]):
                st.markdown(message["content"])
    
    # Chat input
    if prompt := st.chat_input("Type your message here..."):
        # Add user message to chat history
        st.session_state.messages.append({"role": "user", "content": prompt})
        
        # Display user message
        with st.chat_message("user"):
            st.markdown(prompt)
        
        # Get AI response
        with st.chat_message("assistant"):
            with st.spinner("Thinking..."):
                try:
                    response = st.session_state.conversation_manager.get_response(prompt)
                    st.markdown(response)
                    
                    # Add assistant response to chat history
                    st.session_state.messages.append({"role": "assistant", "content": response})
                    
                    # Update stats
                    st.session_state.conversation_stats['total_messages'] += 2
                    
                except Exception as e:
                    error_msg = f"❌ Error: {str(e)}"
                    st.error(error_msg)
                    st.session_state.messages.append({"role": "assistant", "content": error_msg})

def main():
    """Main application entry point"""
    
    # Initialize session state
    initialize_session_state()
    
    # Custom CSS
    st.markdown("""
    <style>
    .stApp {
        max-width: 1200px;
        margin: 0 auto;
    }
    
    .chat-message {
        padding: 1rem;
        border-radius: 0.5rem;
        margin-bottom: 1rem;
    }
    
    .user-message {
        background-color: #e3f2fd;
        border-left: 4px solid #2196f3;
    }
    
    .assistant-message {
        background-color: #f1f8e9;
        border-left: 4px solid #4caf50;
    }
    
    .sidebar .stSelectbox {
        margin-bottom: 1rem;
    }
    </style>
    """, unsafe_allow_html=True)
    
    # Check API keys
    if not os.getenv("OPENAI_API_KEY") or not os.getenv("GOOGLE_API_KEY"):
        st.error("🔑 Missing API Keys! Please check your .env file.")
        st.stop()
    
    # Render sidebar
    sidebar_configuration()
    
    # Render main interface
    main_chat_interface()
    
    # Footer
    st.markdown("---")
    st.markdown(
        "🤖 **Conversational AI Playground** | "
        "Built with Streamlit, LangChain, OpenRouter & Google Gemini | "
        f"Session started: {st.session_state.conversation_stats['start_time'].strftime('%H:%M:%S')}"
    )

if __name__ == "__main__":
    main()
