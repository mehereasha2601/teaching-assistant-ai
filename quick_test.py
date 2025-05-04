import speech_recognition as sr

def quick_test():
    print("Quick Microphone Test")
    print("=" * 50)
    
    try:
        # Just try to access the microphone
        with sr.Microphone() as source:
            print("✓ Microphone accessed successfully")
            
            # Create recognizer
            r = sr.Recognizer()
            
            print("\nSpeak a short phrase when you see 'Recording...'")
            print("Recording...")
            
            # Try to record a very short phrase
            audio = r.listen(source, timeout=2, phrase_time_limit=2)
            
            print("Processing...")
            text = r.recognize_google(audio)
            
            print("\nYou said:", text)
            return True
            
    except Exception as e:
        print(f"\nError: {str(e)}")
        return False

if __name__ == "__main__":
    print("This is a quick test to check if your microphone is working.")
    print("It will only record for 2 seconds maximum.")
    input("\nPress Enter to start...")
    
    if quick_test():
        print("\nTest completed!")
    else:
        print("\nTest failed. Please check if your microphone is properly connected and has necessary permissions.") 