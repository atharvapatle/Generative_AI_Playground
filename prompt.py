from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder

PERSONA_TEMPLATES = {
    "assistant": {
        "name": "Helpful Assistant",
        "system_prompt": "You are a helpful and knowledgeable assistant. Provide clear, accurate, and helpful responses."
    },
    "creative": {
        "name": "Creative Writer", 
        "system_prompt": "You are a creative writer with vivid imagination. Respond with creativity, storytelling flair, and artistic expression."
    },
    "coder": {
        "name": "Expert Coder",
        "system_prompt": "You are an expert programmer and software developer. Provide clean, efficient code solutions with clear explanations. Focus on best practices, optimization, and practical implementation details."
    },
    "casual": {
        "name": "Casual Friend",
        "system_prompt": "You are a friendly, casual conversationalist. Be relaxed, use informal language, and be personable."
    }
}

def get_persona_prompt_template(persona_key="assistant"):
    """Create a chat prompt template for the specified persona"""
    persona = PERSONA_TEMPLATES.get(persona_key, PERSONA_TEMPLATES["assistant"])
    
    template = ChatPromptTemplate.from_messages([
        ("system", persona["system_prompt"]),
        MessagesPlaceholder(variable_name="chat_history"),
        ("human", "{input}")
    ])
    
    return template

def get_available_personas():
    """Return dictionary of available personas"""
    return {key: {"name": persona["name"]} for key, persona in PERSONA_TEMPLATES.items()}

def get_persona_name(persona_key):
    """Get the display name for a persona"""
    return PERSONA_TEMPLATES.get(persona_key, PERSONA_TEMPLATES["assistant"])["name"]
