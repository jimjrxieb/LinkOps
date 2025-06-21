#!/usr/bin/env python3
"""
Test OpenAI integration
"""
import openai
from config.settings import settings

def test_openai_integration():
    """Test OpenAI API key loading and basic functionality"""
    print("🔧 Testing OpenAI Integration...")
    
    # Test 1: Check if API key is loaded
    print(f"✅ OpenAI API Key loaded: {settings.OPENAI_API_KEY[:10]}...")
    
    # Test 2: Set OpenAI API key
    openai.api_key = settings.OPENAI_API_KEY
    print("✅ OpenAI API key set successfully")
    
    # Test 3: Test the generate_rune_with_openai function
    from core.utils.llm import generate_rune_with_openai, contains_code
    
    test_text = "Create a Kubernetes deployment for a Python Flask application"
    print(f"📝 Testing with: {test_text}")
    
    # Test code detection
    has_code = contains_code(test_text)
    print(f"🔍 Contains code patterns: {has_code}")
    
    if not has_code:
        print("🤖 Generating rune with OpenAI...")
        try:
            generated = generate_rune_with_openai(test_text)
            print("✅ OpenAI generation successful!")
            print("📄 Generated rune:")
            print("-" * 50)
            print(generated)
            print("-" * 50)
        except Exception as e:
            print(f"❌ OpenAI generation failed: {e}")
    else:
        print("ℹ️  Text contains code patterns, skipping OpenAI generation")
    
    print("🎉 OpenAI integration test completed!")

if __name__ == "__main__":
    test_openai_integration() 