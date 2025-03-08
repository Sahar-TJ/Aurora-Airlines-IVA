# Aurora-Airlines-IVA

Welcome to the Aurora Airlines IVA (Intelligent Virtual Assistant) System repository! This project is an AI-driven virtual assistant designed for an airline, allowing customers to interact with the system via voice or keypad inputs to perform various tasks such as flight booking, flight status checks, and more.  

## Overview
The Aurora Airlines IVA System is a Python-based application that enhances traditional IVR (Interactive Voice Response) systems with AI-powered capabilities. It provides a user-friendly interface for customers to access essential services without the need for human intervention. The system is built to handle common airline-related queries and transactions efficiently.

## IVA System Highlights:

-  **Flight Information:** Customers can inquire about flight schedules, statuses, and other relevant details.
-  **Reservations:** The IVR system allows users to book, modify, or cancel reservations through voice prompts.
-  **Customer Support**: Provides assistance with common inquiries and connects customers to live agents when necessary.
-  **Multilingual Support:** Handle customer queries in multiple languages.
-  **Scalable Architecture:** Easily adaptable to handle high call volumes.
-  **Interactive Menu:** The system uses a voice and keypad-based interactive menu to guide users through the options.

## Features:

-  **Automatic Speech Recognition (ASR):** Converts user speech into text using OpenAI's Whisper model.
-  **Sentiment Analysis:** Determines user emotions to route interactions effectively.
-  **Intent Recognition:** Identifies customer intent using keyword matching and machine learning-based text classification.
-  **Text-to-Speech (TTS) Synthesis:** Converts responses into speech using pyttsx3.
-  **Conversation Logging:** Saves interactions in a log file for future reference.
-  **Music Playback:** Plays hold music when necessary.

## Technologies Used:

-  **Python:** The core programming language used for developing the IVR logic.
-  **pyttsx3:** For text-to-speech conversion.
-  **Transformers Library:** For sentiment analysis and intent classification.
-  **SoundDevice & SoundFile:** For audio recording and playback.
-  **Whisper ASR Model:** For automatic speech recognition (transcription of user queries).

## How It Works:

It follows the **GILIICAPRA** exchange model (Greeting, Identify, Listen, Intent, Confirm, Act, Provide Closure) to handle various customer queries efficiently.

-  **Greeting:** The system greets the user and prompts them to state their query.
-  **Audio Input:** The user can either record their query directly or provide an audio file.
-  **Transcription:** The system transcribes the user's speech using the Whisper ASR model.
-  **Sentiment Analysis:** The system analyzes the sentiment of the user's query to determine if escalation is needed.
-  **Intent Identification:** The system identifies the user's intent using keyword matching and a rule-based approach.
-  **Response:** Based on the identified intent, the system provides a predefined response or escalates the query to a human agent.
-  **Logging:** All interactions are logged for future reference.

## Installation:

### Clone the Repository:

``git clone https://github.com/Sahar-TJ/Aurora-Airlines-IVR.git``

``cd Aurora-Airlines-IVR``

### Install Dependencies:
Ensure Python 3.x is installed. Then, install the required libraries:

``pip install -r requirements.txt``

### Run the Application:
Execute the main script to start the IVR system:

``python AuroraIVR.ipynb``


## Future Enhancements

-  Integration with a telephony service like Twilio for real-world deployment.
-  Adding a database (e.g., SQLite or PostgreSQL) for more robust data management.
-  Enhancing the user interface with a web or mobile app.


