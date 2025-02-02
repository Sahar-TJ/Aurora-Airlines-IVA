# Aurora Airlines
# This code implements a GILIICAPRA (Greeting, Identify, Listen, Intent, Confirm, Act, and Provide Closure) exchange for Aurora Airlines intelligent virtual assistant.
#
# The system is designed to handle a variety of intents, including booking flights, checking flight status, providing general information about the airline, answering questions about the frequent flyer program, and providing information about baggage policies.
#
# Some suggested phrases that you can try include:
#
# Booking a flight:
# - "Can you reserve me a Flight?"    
# - "I'd like to book a flight to Sydney next week."
# - "Do you have any flights available to Paris in July?"
#
# Checking flight status:
# - "Can you tell me the status of flight AO123?"
# - "Is my flight to Melbourne on time?"
#
# General information:
# - "What is your policy on pets?"
# - "Do you offer in-flight meals?"
# - "Can you tell me about the airline?"
#
# Frequent flyer program:
# - "How do I join your frequent flyer program?"
# - "How many points do I need to redeem a flight?"
#
# Baggage information:
# - "What is the weight limit for checked baggage?"
# - "Can I bring a musical instrument on board as carry-on?"
# - "How many luggage items can I carry?"
#
# The system uses automatic speech recognition (ASR) to transcribe the user's speech, sentiment analysis to gauge the user's emotion, and a rule-based approach to identify the user's intent. The system responds to the user's query using text-to-speech (TTS) synthesis.
#
# The code also includes functionality to log the conversation between the user and the system to a file in the 'logs' directory.



import pyttsx3
import sounddevice as sd
import soundfile as sf
import torch
from transformers import pipeline, AutoModelForSequenceClassification, AutoTokenizer
import random
import os

def text_to_speech(text, rate=150, volume=1):
    """
    Convert text to speech using the pyttsx3 library.
    Args:
    - text (str): The text to convert to speech.
    - rate (int): The speed of speech (words per minute). Default is 150.
    - volume (float): The volume of speech (0.0 to 1.0). Default is 1.0.
    """
    # Initialize the TTS engine
    engine = pyttsx3.init()
    print(text)
    bot_to_file(text)
    # Set properties
    engine.setProperty('rate', rate)
    engine.setProperty('volume', volume)
    
    # Convert text to speech
    engine.say(text)
    
    # Wait for the speech to finish
    engine.runAndWait()

def record_audio(filename, duration=3, audio_file=None):
    # Set the sample rate and number of channels
    sample_rate = 16000
    channels = 1

    if audio_file:
        # Read audio file from disk
        try:
            audio_data, _ = sf.read(audio_file)
        except Exception as e:
            print(f"Error reading audio file: {e}")
            return

        # Save audio data to a WAV file
        sf.write(filename, audio_data, sample_rate)
        print("Audio file saved.")
    else:
        # Record audio from the sound device
        print("Recording audio...")
        audio_data = sd.rec(int(duration * sample_rate), samplerate=sample_rate, channels=channels, dtype='int16')
        sd.wait()  # Wait until recording is finished

        # Save audio data to a WAV file
        sf.write(filename, audio_data, sample_rate)
        print("Recording finished.")

def transcribe_audio(filename):
    # Initialize the ASR pipeline
    asr_pipeline = pipeline(
        "automatic-speech-recognition",
        model="openai/whisper-base",
        device=0 if torch.cuda.is_available() else -1  # Use GPU if available
    )

    # Load the audio file
    audio, sample_rate = sf.read(filename)

    # Perform speech recognition using Whisper base model
    try:
        transcript = asr_pipeline(audio)['text']
        print("Transcript:", transcript)
        user_to_file(transcript)
        return transcript
    except Exception as e:
        print(f"Error transcribing audio: {e}")
        return None

    
def user_to_file(transcript):
    # Create a log directory if it doesn't exist
    if not os.path.exists('logs'):
        os.makedirs('logs')

    # Write the transcript to a file in the log directory
    with open('logs/transcript_log.txt', 'a') as f:
        f.write('User: ' + transcript + '\n')
        f.write('* ' * 25 + '\n')

        
def bot_to_file(transcript):
    # Create a log directory if it doesn't exist
    if not os.path.exists('logs'):
        os.makedirs('logs')

    # Write the transcript to a file in the log directory
    with open('logs/transcript_log.txt', 'a') as f:
        f.write("Aurora Airlines: "+ transcript + '\n')
        f.write('-' * 50 + '\n')
        


def is_affirmative(text):
    affirmative_keywords = ["yes", "yeah", "yep", "sure", "correct", "true", "right", "affirmative", "okay", "ok", "right","absolutely"]
    text = text.lower()
    
    for keyword in affirmative_keywords:
        if keyword in text:
            return True
    
    return False  # Return False if no affirmative keyword is found

def is_negative(text):
    negative_keywords = ["no", "nope", "incorrect", "wrong", "not really", "nah", "negative"]
    text = text.lower()
    
    for keyword in negative_keywords:
        if keyword in text:
            return True
    
    #return False
    
def analyze_sentiment(query):
    # Perform sentiment analysis
    result = sentiment_pipeline(query)
    
    # Extract sentiment label and score
    sentiment_label = result[0]['label']
    sentiment_score = result[0]['score']
    # Calculate compound sentiment score
    sentiment_score_c = (sentiment_score - 0.5) * 2  # Convert [0, 1] range to [-1, 1]

    # Print sentiment results
    print("Sentiment Label:", sentiment_label)
    print("Sentiment Score:", sentiment_score)
    print("Compound Sentiment Score:", sentiment_score_c)
    
    return sentiment_label, sentiment_score, sentiment_score_c

def handle_irrelevant_query():
    print("confused")
    text_to_speech("Sorry to hear that. Let me connect you to an agent for further assistance.")
    play_music()

    
    
def identify_intent(prompt, query, intent_keywords):
    # Extracting intent from keywords
    for intent, keywords in intent_keywords.items():
        if any(keyword in query.lower() for keyword in keywords):
            return intent

    # If intent not found in keywords, using prompt-based classification
    model = pipeline("text-classification", model="distilbert-base-uncased", tokenizer="distilbert-base-uncased")
    classification_input = prompt + "\n\nUser: " + query
    print(classification_input)
    classification_result = model(classification_input)
    print(classification_result)
    intent_label = classification_result[0]['label']

    if intent_label == 'LABEL_0':
        return None
    else:
        return intent_label.lower()


    
'''def identify_intent(response):
    response_text = response.lower()
    identified_intent = None
    max_matched_keywords = 0

    for intent, keywords in intent_keywords.items():
        matched_keywords = sum(1 for keyword in keywords if keyword in response_text)
        if matched_keywords > max_matched_keywords:
            max_matched_keywords = matched_keywords
            identified_intent = intent

    if identified_intent is None or max_matched_keywords < 1:
        return None

    return identified_intent'''

def respond_to_intent(intent):
    response = random.choice(responses[intent])
    print("Response:")
    text_to_speech(response)

# Load pre-trained BERT model and tokenizer for sentiment analysis
sentiment_pipeline = pipeline("sentiment-analysis")

# Load responses and intent identification keywords
responses = {
    "booking": [
        "Sure thing! To book a flight, you'll need to provide information such as your travel dates, destination, and number of passengers. You can do this on our website or by speaking with one of our customer service representatives.",
        "Of course! I'd be happy to help you book a flight. Can you please provide me with your travel dates and destination?",
        "Absolutely! To get started with booking a flight, we'll need some basic information from you such as your departure city, arrival city, and travel dates. You can provide this information online or over the phone with one of our agents."
    ],
    "flight_status": [
        "To check the status of a flight, you can visit our website and enter the flight number and date. You can also sign up for flight status notifications to receive updates via text or email.",
        "If you'd like to know the status of a flight, I can help you with that. Please provide me with the flight number and date, and I'll do my best to provide you with the most up-to-date information.",
        "Checking the status of a flight is easy! Just head to our website and enter the flight number and date. You can also call our customer service hotline for real-time updates."
    ],
    "general_information": [
        "If you have general questions about our airline or policies, you can find a wealth of information on our website. There, you'll find details about our routes, baggage policies, pet policies, and more.",
        "For general inquiries about our airline, I'd recommend checking out our website. There, you'll find a comprehensive FAQ section as well as contact information for our customer service team.",
        "If you're looking for information about our airline's policies or services, our website is a great resource. There, you'll find details about everything from in-flight amenities to special accommodations for passengers with disabilities."
    ],
    "frequent_flyer": [
        "If you're a frequent flyer with our airline, you may be eligible for special perks and benefits. To learn more about our frequent flyer program, including how to enroll and earn miles, visit our website or speak with one of our customer service representatives.",
        "As a frequent flyer with our airline, you may be able to take advantage of perks such as priority boarding, free checked bags, and access to our exclusive lounges. To learn more about our program and how to earn miles, visit our website or give us a call.",
        "Our frequent flyer program is designed to reward our loyal customers with perks and benefits that make travel more enjoyable. To learn more about the program and how to enroll, I'd recommend visiting our website or speaking with one of our customer service agents."
    ],
    "baggage_information": [
        "If you have questions about our baggage policies, including carry-on and checked baggage allowances, you can find that information on our website. There, you'll also find details about fees for excess or oversized baggage.",
        "Our baggage policies vary depending on factors such as your destination and fare class. To learn more about what you're allowed to bring on board and what fees may apply, I'd recommend checking out our website or speaking with one of our customer service representatives.",
        "For information about our baggage policies, including carry-on and checked baggage allowances, fees, and restrictions, visit our website. There, you'll find everything you need to know to ensure a smooth and hassle-free travel experience."
    ]
}

intent_keywords = {
    "booking": ["book", "reserve", "flight", "flights", "to", "from"],
    "flight_status": ["status", "flight", "delay", "cancel", "late", "delayed", "arrive", "arrival", "time", "depart", "departure"],
    "general_information": ["information", "policy", "route", "airline", "offer", "offers", "pets", "meal", "food", "allowances"],
    "frequent_flyer": ["frequent flyer", "miles", "rewards", "points", "perks", "benefits"],
    "baggage_information": ["baggage", "luggage", "carry on", "checked", "allowance", "bag", "weight"]
}

# Define the prompt
prompt = """
Welcome to Aurora Airlines customer service! How can we assist you today?

1. Booking a Flight: Example queries - "I need to book a flight for next week", "Can you help me reserve a seat on a flight to Paris?"
2. Flight Status: Example queries - "What's the status of my flight to New York?", "Is my flight delayed?", "Will my flight be cancelled", "When is the arrival or departure of the flight"
3. General Information: Example queries - "What are your pet policies?", "Do you offer in flight meals?", "Tell me about your airline's policy"
4. Frequent Flyer Program: Example queries - "How can I enroll in your frequent flyer program?", "What are the benefits of being a frequent flyer?", "How much reward can I score?"
5. Baggage Information: Example queries - "What's the baggage allowance for my flight?", "Are there any restrictions on carry-on luggage?"

Please provide your query, and we'll do our best to assist you!
"""


def play_music():
    # Load the audio file
    data, samplerate = sf.read("out_music.wav")
    
    # Play the audio
    sd.play(data, samplerate)
    
    # Wait until the audio is done playing
    sd.wait()


def get_audio_input():
    while True:
        # Speak the prompt to the user
        text_to_speech("Do you want to record audio from the device or provide an audio file? Type 'record' to record audio or 'file' to provide an audio file.")
        
        # Get user input
        choice = input("Record / File: ").lower()
        
        if choice == 'record':
            return 'record'
        elif choice == 'file':
            return 'file'
        else:
            # Speak the error message to the user
            text_to_speech("Invalid choice. Please type 'record' or 'file'.")

if __name__ == "__main__":
    # Greet user and ask for their query
    text_to_speech("Hello! Welcome to Aurora Airline's Intelligent Virtual Assistant. How can we assist you today?")
    
    # Prompt user for audio input method
    audio_input_method = get_audio_input()

    if audio_input_method == 'record':
        record_audio("user_query.wav", duration=3)
    else:
        text_to_speech("Please provide the path to the audio file. Please use a .WAV file ")
        audio_file_path = input("File: ")
        record_audio("user_query.wav", audio_file=audio_file_path, duration=3)

    transcript = transcribe_audio("user_query.wav")

    # Perform sentiment analysis on the user's query
    sentiment_label, sentiment_score, sentiment_score_c = analyze_sentiment(transcript)

    # Perform further processing based on sentiment
    if sentiment_score_c < -0.7:
        print("operator")
        #text_to_speech("I'm sorry to hear that you're upset. Let me transfer you to our customer support team.")
        play_music()
        exit()
    else:
        # Identify intent of user query
        intent = identify_intent(prompt, transcript, intent_keywords)

        # Check if intent is identified
        if intent is not None:
            # Ask the user if the identified intent matches their query
            text_to_speech(f"Did you mean to inquire about {intent}? Please respond with yes or no.")

            # Record the user's response
            record_audio("user_response.wav", duration=3)
            user_response_transcript = transcribe_audio("user_response.wav")

            # Check if the response is affirmative
            if is_affirmative(user_response_transcript):
                # Proceed with providing the response for the identified intent
                print("Intent: ",intent)
                respond_to_intent(intent)
                text_to_speech("Please Wait while we connect you to an agent! Thank you for choosing Aurora Airlines!")
                play_music()
            elif is_negative(user_response_transcript):
                # Handle the query as irrelevant
                handle_irrelevant_query()
            else:
                # Ask for clarification if the response is unclear
                text_to_speech("I'm sorry, I didn't understand your response. Can you please confirm with yes or no?")
        else:
            handle_irrelevant_query()
