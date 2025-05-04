import speech_recognition as sr
import time

def test_speech_recognition():
    # Initialize recognizer
    recognizer = sr.Recognizer()
    
    print("Testing speech recognition...")
    print("Please speak after the prompt. The test will record for 3 seconds.")
    
    try:
        with sr.Microphone() as source:
            print("\nAdjusting for ambient noise... Please wait...")
            # Reduced ambient noise adjustment time to 1 second
            recognizer.adjust_for_ambient_noise(source, duration=1)
            
            print("\nSpeak now! (Recording for 3 seconds)")
            print("Recording...")
            
            # Record audio with shorter timeout
            audio = recognizer.listen(source, timeout=3, phrase_time_limit=3)
            
            print("\nProcessing speech...")
            
            # Convert speech to text
            text = recognizer.recognize_google(audio)
            
            print("\nResults:")
            print("-" * 50)
            print(f"Recognized text: {text}")
            print("-" * 50)
            
            return True
            
    except sr.WaitTimeoutError:
        print("\nError: No speech detected within timeout period")
        return False
    except sr.UnknownValueError:
        print("\nError: Could not understand the audio")
        return False
    except sr.RequestError as e:
        print(f"\nError: Could not request results from Google Speech Recognition service; {e}")
        return False
    except Exception as e:
        print(f"\nError: {str(e)}")
        return False

if __name__ == "__main__":
    print("Speech Recognition Test")
    print("=" * 50)
    print("This test will:")
    print("1. Adjust for ambient noise (1 second)")
    print("2. Record your voice for 3 seconds")
    print("3. Convert your speech to text")
    print("=" * 50)
    
    input("Press Enter to start the test...")
    
    success = test_speech_recognition()
    
    if success:
        print("\nTest completed successfully!")
    else:
        print("\nTest failed. Please check the error message above.") 