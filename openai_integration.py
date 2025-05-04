import os
import openai
from dotenv import load_dotenv

class OpenAIIntegration:
    def __init__(self):
        # Load environment variables from .env file
        load_dotenv()
        
        # Initialize OpenAI client
        api_key = os.getenv('OPENAI_API_KEY')
        if not api_key:
            raise ValueError("OPENAI_API_KEY not found in environment variables")
        
        openai.api_key = api_key
        
        # Default model to use
        self.model = "gpt-3.5-turbo"
    
    def get_response(self, prompt, model=None):
        """
        Get a response from OpenAI's model based on the provided prompt.
        
        Args:
            prompt (str): The input prompt to send to the model
            model (str, optional): The model to use. Defaults to self.model.
            
        Returns:
            str: The model's response
        """
        try:
            # Use specified model or default
            model_to_use = model if model else self.model
            
            # Make API call
            response = openai.ChatCompletion.create(
                model=model_to_use,
                messages=[
                    {"role": "system", "content": "You are a helpful assistant."},
                    {"role": "user", "content": prompt}
                ]
            )
            
            # Extract and return the response text
            return response.choices[0].message.content
            
        except Exception as e:
            print(f"Error getting response from OpenAI: {str(e)}")
            return None

# Example usage
if __name__ == "__main__":
    # Create instance of OpenAIIntegration
    ai = OpenAIIntegration()
    
    # Example prompt
    test_prompt = "What is the capital of France?"
    
    # Get response
    response = ai.get_response(test_prompt)
    
    if response:
        print(f"Prompt: {test_prompt}")
        print(f"Response: {response}")
    else:
        print("Failed to get response from OpenAI") 