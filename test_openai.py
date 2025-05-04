from openai_integration import OpenAIIntegration

def test_openai_integration():
    print("Testing OpenAI Integration...")
    
    # Create instance of OpenAIIntegration
    ai = OpenAIIntegration()
    
    # Test prompts
    test_prompts = [
        "What is the capital of France?",
        "Explain quantum computing in one sentence.",
        "What is 2+2?"
    ]
    
    # Test each prompt
    for prompt in test_prompts:
        print("\n" + "="*50)
        print(f"Testing prompt: {prompt}")
        response = ai.get_response(prompt)
        
        if response:
            print(f"Response received successfully!")
            print(f"Response: {response}")
        else:
            print("Failed to get response from OpenAI")
            print("Please check your API key and internet connection.")

if __name__ == "__main__":
    test_openai_integration() 