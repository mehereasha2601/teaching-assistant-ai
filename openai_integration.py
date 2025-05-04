import os
import openai
import streamlit as st

class OpenAIIntegration:
    def __init__(self):
        # Try to get API key from Streamlit secrets first
        try:
            api_key = st.secrets["OPENAI_API_KEY"]
            print("Found API key in Streamlit secrets")
        except Exception as e:
            print(f"Error accessing Streamlit secrets: {str(e)}")
            # Fallback to environment variables
            api_key = os.getenv('OPENAI_API_KEY')
            if api_key:
                print("Found API key in environment variables")
            else:
                print("API key not found in environment variables")
                st.error("OPENAI_API_KEY not found in Streamlit secrets or environment variables")
                raise ValueError("OPENAI_API_KEY not found in Streamlit secrets or environment variables")
        
        openai.api_key = api_key
        print("Successfully set OpenAI API key")
        
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
            error_msg = f"Error getting response from OpenAI: {str(e)}"
            print(error_msg)
            st.error(error_msg)
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