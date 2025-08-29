# conversation.py
from langchain.chains import ConversationChain
from langchain.memory import ConversationBufferWindowMemory
from models import ModelManager
from prompt import get_persona_prompt_template

class ConversationManager:
    """Manages LangChain conversation with memory and persona switching"""
    
    def __init__(self, persona_key="assistant", memory_window=10, temperature=0.7, model_key="llama"):
        # Initialize model manager
        self.model_manager = ModelManager()
        self.model_manager.set_current_model(model_key)
        
        # Get LLM instance
        self.llm = self.model_manager.get_current_llm(temperature=temperature)
        
        # Get prompt template for the persona
        self.prompt_template = get_persona_prompt_template(persona_key)
        
        # Initialize memory
        self.memory = ConversationBufferWindowMemory(
            memory_key="chat_history",
            k=memory_window,
            return_messages=True
        )
        
        # Create conversation chain
        self.conversation = ConversationChain(
            llm=self.llm,
            prompt=self.prompt_template,
            memory=self.memory,
            verbose=False
        )
        
        # Store settings
        self.persona_key = persona_key
        self.memory_window = memory_window
        self.temperature = temperature
        self.model_key = model_key
    
    def get_response(self, user_input):
        """Get AI response for user input"""
        try:
            response = self.conversation.predict(input=user_input)
            return response
        except Exception as e:
            return f"Error: {str(e)}"
    
    def update_model(self, model_key, temperature=None):
        """Switch to different model"""
        self.model_key = model_key
        self.model_manager.set_current_model(model_key)
        
        if temperature is not None:
            self.temperature = temperature
            
        self.llm = self.model_manager.get_current_llm(temperature=self.temperature)
        self.conversation.llm = self.llm
    
    def update_persona(self, persona_key):
        """Switch persona and clear memory"""
        self.persona_key = persona_key
        self.prompt_template = get_persona_prompt_template(persona_key)
        self.conversation.prompt = self.prompt_template
        self.memory.clear()
    
    def update_temperature(self, temperature):
        """Update temperature for current model"""
        self.temperature = temperature
        self.llm = self.model_manager.get_current_llm(temperature=temperature)
        self.conversation.llm = self.llm
    
    def update_memory_window(self, memory_window):
        """Update memory window size"""
        self.memory_window = memory_window
        # Create new memory with updated window
        old_messages = self.memory.chat_memory.messages
        self.memory = ConversationBufferWindowMemory(
            memory_key="chat_history",
            k=memory_window,
            return_messages=True
        )
        # Keep last k messages
        for msg in old_messages[-memory_window:]:
            self.memory.chat_memory.add_message(msg)
        
        self.conversation.memory = self.memory
    
    def reset_conversation(self):
        """Clear conversation history"""
        self.memory.clear()
    
    def get_stats(self):
        """Get conversation statistics"""
        messages = self.memory.chat_memory.messages
        return {
            "total_messages": len(messages),
            "memory_window": self.memory_window,
            "current_persona": self.persona_key,
            "current_model": self.model_key,
            "temperature": self.temperature
        }
    
    def get_conversation_history(self):
        """Get formatted conversation history"""
        messages = self.memory.chat_memory.messages
        history = []
        for msg in messages:
            history.append({
                "role": msg.type,
                "content": msg.content
            })
        return history


# Test conversation.py
if __name__ == "__main__":
    print("🧪 Testing ConversationManager...")
    print("=" * 50)
    
    try:
        # Test initialization
        print("1. Initializing ConversationManager...")
        conv = ConversationManager(persona_key="coder", model_key="llama")
        print("✅ ConversationManager initialized!")
        
        # Test stats
        print("\n2. Conversation Stats:")
        stats = conv.get_stats()
        for key, value in stats.items():
            print(f"   {key}: {value}")
        
        # Test model switching
        print("\n3. Testing Model Switching:")
        for model in ["llama", "mistral", "gemini"]:
            conv.update_model(model)
            print(f"   ✅ Switched to {model}")
        
        # Test persona switching  
        print("\n4. Testing Persona Switching:")
        for persona in ["assistant", "creative", "coder", "casual"]:
            conv.update_persona(persona)
            print(f"   ✅ Switched to {persona}")
        
        # Test temperature update
        print("\n5. Testing Temperature Update:")
        conv.update_temperature(0.9)
        print(f"   ✅ Temperature updated to {conv.temperature}")
        
        # Test memory window update
        print("\n6. Testing Memory Window Update:")
        conv.update_memory_window(5)
        print(f"   ✅ Memory window updated to {conv.memory_window}")
        
        print("\n🎉 ConversationManager ready for integration!")
        
    except Exception as e:
        print(f"❌ Error: {e}")
        print("\nMake sure models.py and prompt.py are working correctly first!")
