#!/usr/bin/env python3
"""
Test script to verify Gemini API is working
"""

import os
import google.generativeai as genai
from dotenv import load_dotenv

def test_gemini_api():
    # Load API key from .env file
    load_dotenv()
    api_key = os.getenv("GEMINI_API_KEY")
    
    if not api_key:
        print("❌ ERROR: GEMINI_API_KEY not found in environment variables")
        return False
    
    print(f"✓ API key found: {api_key[:4]}...{api_key[-4:]}")
    
    try:
        # Configure the API
        genai.configure(api_key=api_key)
        
        # Create a model instance
        model = genai.GenerativeModel('gemini-1.5-pro')
        
        # Test with a simple prompt
        prompt = "Hello, please respond with a short greeting."
        response = model.generate_content(prompt)
        
        print(f"\n✓ API Response: {response.text}\n")
        print("✓ Gemini API is working correctly!")
        return True
    except Exception as e:
        print(f"\n❌ ERROR: {str(e)}")
        return False

if __name__ == "__main__":
    print("\n🔍 Testing Gemini API Connection...\n")
    test_gemini_api() 