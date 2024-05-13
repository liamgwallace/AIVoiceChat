# OpenAI Voice Interface

## Description
This project is an interactive voice assistant that uses OpenAI's GPT models and ElevenLabs' voice synthesis to respond to user input. It features a graphical user interface (GUI) to display the assistant's and user's speech as text. The project integrates speech-to-text to understand user commands and text-to-speech to generate audible responses in different personas, primarily using the GLaDOS voice from the Portal series.

## Table of Contents
1. [Installation](#installation)
2. [Usage](#usage)
3. [Technologies Used](#technologies-used)
4. [Project Structure](#project-structure)
5. [License](#license)

## Installation

Follow these steps to set up your development environment and run the project:

1. **Clone the repository:**
   ```bash
   git clone https://github.com/liamgwallace/AIVoiceChat
   cd AIVoiceChat
   ```

2. **Install the required Python packages:**
   Ensure you have Python installed, then run:
   ```bash
   pip install -r requirements.txt
   ```

   Your `requirements.txt` should include:
   ```plaintext
   openai
   tkinter
   pillow
   python-dotenv
   ```

3. **Environment Variables:**
   Create a `.env` file in the root of your project directory with the necessary API keys and model configurations. You can use `example.env` as a template:
   ```plaintext
   ELEVENLABS_API_KEY=your_elevenlabs_api_key_here
   ELEVENLABS_MODEL=eleven_turbo_v2
   OPENAI_API_KEY=your_openai_api_key_here
   OPENAI_MODEL=gpt-3.5-turbo-1106
   ```

4. **Hardware Requirements:**
   To use all features, ensure you have a microphone and speakers (or headphones) connected to your computer.

## Usage

To run the OpenAI Voice Interface, follow these steps:

1. **Start the application:**
   Navigate to the project directory and run:
   ```bash
   python openai_voice_interface.py
   ```

2. **Using the Assistant:**
   - Speak the wake word **"Computer"** to activate the assistant.
   - The assistant will transcribe your speech and respond both textually and audibly.
   - Use keywords like "stop", "cancel", or "goodbye" to stop the assistant from listening.

3. **Interacting with the GUI:**
   - The GUI displays the user's speech and the assistant's responses in real time.
   - You can see the listening status through an animated microphone icon.

## Technologies Used

- **Python**: The main programming language used.
- **OpenAI API**: For generating responses using GPT models.
- **ElevenLabs API**: For converting text responses into speech.
- **Tkinter**: For creating the graphical user interface.
- **Pillow**: For image processing in the GUI.
- **python-dotenv**: For managing environment variables.

## Project Structure

```plaintext
ChatAI.py                   - Defines the AI agent using OpenAI's API.
GUI.py                      - Implements the graphical user interface.
ai_personas.py              - Contains different AI personas.
elevenlabs_voices.py        - Maps personas to specific ElevenLabs voice models.
example.env                 - An example .env file with API keys and model configurations.
microphone_icon.png         - The microphone icon displayed in the GUI.
openai_voice_interface.py   - The main script that ties together all components.
```

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.
