import speech_recognition as sr

def instant_test():
    print("Instant Microphone Test")
    print("=" * 50)
    
    try:
        # Create recognizer
        r = sr.Recognizer()
        
        # Set very short timeout
        r.dynamic_energy_threshold = True
        r.energy_threshold = 1000  # Lower threshold for faster response
        
        with sr.Microphone() as source:
            print("Recording... (Speak now!)")
            
            # Record with minimal timeout
            audio = r.listen(source, timeout=1, phrase_time_limit=1)
            
            print("Processing...")
            text = r.recognize_google(audio)
            
            print("\nYou said:", text)
            return True
            
    except sr.WaitTimeoutError:
        print("\nNo speech detected - try speaking louder")
        return False
    except sr.UnknownValueError:
        print("\nCould not understand audio - try speaking clearly")
        return False
    except Exception as e:
        print(f"\nError: {str(e)}")
        return False

if __name__ == "__main__":
    print("Speak immediately when you see 'Recording...'")
    print("Test will run for 1 second only")
    input("\nPress Enter to start...")
    
    if instant_test():
        print("\nTest completed!")
    else:
        print("\nTest failed - try again") 