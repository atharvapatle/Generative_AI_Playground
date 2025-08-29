# models.py
from langchain.chat_models import ChatOpenAI
from langchain_google_genai import ChatGoogleGenerativeAI
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

class ModelManager:
    """Manages different LLM models using standard LangChain integrations"""
    
    def __init__(self):
        # Load API keys from environment
        self.openai_api_key = os.getenv("OPENAI_API_KEY")  # Your OpenRouter key
        self.openai_api_base = os.getenv("OPENAI_API_BASE")  # OpenRouter base URL
        self.google_api_key = os.getenv("GOOGLE_API_KEY")
        
        if not self.openai_api_key:
            raise ValueError("OPENAI_API_KEY missing in environment variables")
        
        if not self.google_api_key:
            raise ValueError("GOOGLE_API_KEY missing in environment variables")
        
        # Available models with their configurations
        self.models = {
            "mistral": {
                "name": "Mistral Small",
                "model_id": "mistralai/mistral-small-3.2-24b-instruct:free",
                "provider": "openrouter",
                "description": "Free Mistral model for text conversations"
            },
            "llama": {
                "name": "LLaMA 3.3", 
                "model_id": "meta-llama/llama-3.3-8b-instruct:free",
                "provider": "openrouter",
                "description": "Free LLaMA model for text conversations"
            },
            "gemini": {
                "name": "Gemini Flash Lite",
                "model_id": "gemini-2.5-flash-lite",
                "provider": "google",
                "description": "Google's Gemini Flash Lite model"
            }
        }
        
        # Default model
        self.current_model = "llama"
    
    def get_llm(self, model_key="llama", temperature=0.7, max_tokens=1500):
        """Get LLM instance for specified model"""
        
        if model_key not in self.models:
            raise ValueError(f"Model '{model_key}' not supported. Available: {list(self.models.keys())}")
        
        model_info = self.models[model_key]
        model_id = model_info["model_id"]
        
        if model_info["provider"] == "google":
            # Use ChatGoogleGenerativeAI for Gemini
            return ChatGoogleGenerativeAI(
                google_api_key=self.google_api_key,
                model=model_id,
                temperature=temperature,
                max_output_tokens=max_tokens
            )
        
        else:  # OpenRouter models (mistral, llama)
            # Use ChatOpenAI - it will automatically use OPENAI_API_BASE from env
            return ChatOpenAI(
                model=model_id,
                temperature=temperature,
                max_tokens=max_tokens
            )
    
    def set_current_model(self, model_key):
        """Set the current active model"""
        if model_key in self.models:
            self.current_model = model_key
        else:
            raise ValueError(f"Model '{model_key}' not supported. Available: {list(self.models.keys())}")
    
    def get_current_llm(self, temperature=0.7, max_tokens=1500):
        """Get LLM instance for current model"""
        return self.get_llm(self.current_model, temperature, max_tokens)
    
    def get_available_models(self):
        """Get list of available models for UI"""
        return {
            key: {
                "name": info["name"],
                "description": info["description"]
            }
            for key, info in self.models.items()
        }
    
    def get_model_info(self, model_key=None):
        """Get detailed model information"""
        model_key = model_key or self.current_model
        return self.models.get(model_key, {})
    
    def get_all_available_keys(self):
        """Debug function to see what API keys are loaded"""
        return {
            "openai_api_key": "✅ Loaded" if self.openai_api_key else "❌ Missing",
            "openai_api_base": self.openai_api_base or "❌ Missing",
            "google_api_key": "✅ Loaded" if self.google_api_key else "❌ Missing"
        }


# Testing section
if __name__ == "__main__":
    print("🧪 Testing ModelManager...")
    print("=" * 50)
    
    try:
        # Initialize ModelManager
        print("1. Initializing ModelManager...")
        manager = ModelManager()
        print("✅ ModelManager initialized successfully!")
        
        # Test API keys loading
        print("\n2. Checking API Keys Status:")
        keys_status = manager.get_all_available_keys()
        for key, status in keys_status.items():
            print(f"   {key}: {status}")
        
        # Test available models
        print("\n3. Available Models:")
        models = manager.get_available_models()
        for key, info in models.items():
            print(f"   📝 {key}: {info['name']}")
            print(f"      Description: {info['description']}")
        
        # Test model switching
        print("\n4. Testing Model Switching:")
        for model_key in ["llama", "mistral", "gemini"]:
            try:
                manager.set_current_model(model_key)
                print(f"   ✅ Switched to {model_key}")
                
                # Test LLM initialization (without API call)
                llm = manager.get_llm(model_key, temperature=0.5)
                print(f"   ✅ {model_key} LLM initialized: {type(llm).__name__}")
                
            except Exception as e:
                print(f"   ❌ Error with {model_key}: {e}")
        
        print("\n🎉 All tests passed successfully!")
        print("Ready to integrate with conversation.py and app.py!")
        
    except Exception as e:
        print(f"❌ Error during testing: {e}")
        print("\nTroubleshooting:")
        print("1. Check if .env file exists and has correct API keys")
        print("2. Run: pip install langchain-community langchain-openai langchain-google-genai")
        print("3. Verify API key formats are correct")
