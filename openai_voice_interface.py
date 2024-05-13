from ChatAI import ChatAI
from GUI import AssistantGUI
import ai_personas
import elevenlabs_voices

import elevenlabs
from RealtimeSTT import AudioToTextRecorder

import threading
import queue
import time
import string

elevenlabs_api_key = '4f6508be147a0eb2794a356342ba0d8c'

class WakeWordHandler:
    def __init__(self):
        self.triggered = False

    def wake_word_detected(self):
        self.triggered = True

    def reset(self):
        self.triggered = False

    def is_triggered(self):
        return self.triggered

def check_stopword(text, keywords = ['stop', 'cancel', 'council', 'halt', 'pause', 'ok', 'thanks', 'thankyou','thank you', 'bye', 'goodbye', 'good bye']):
    translator = str.maketrans('', '', string.punctuation)
    normalized_text = text.translate(translator).lower()
    for keyword in keywords:
        if keyword == normalized_text:
            return True
    return False
def my_wakeword_timeout(gui):
    print("DEBUG: Wakeword timeout")
    gui.queue.put("HIDE_ALL")

def my_start_callback(gui):
    print("DEBUG: Recording started!")
    gui.queue.put("CLEAR_USER")
    gui.queue.put("LISTEN")

def my_stop_callback(gui):
    print("DEBUG: Recording stopped!")
    gui.queue.put("STOP_LISTEN")


def my_wakeword_detected_callback(handler):
    print("my_wakeword_detected_callback")
    handler.wake_word_detected()

def my_realtime_transcription_update(text, gui):

    gui.queue.put(f"USER_MSG:{text}")

def my_on_sentence(text, gui):
    gui.queue.put(f"AI_STREAM:{text}")
    print(text, end="", flush=True)
    #gui.text_stream(text)
def my_on_character(text, gui):
    gui.queue.put(f"AI_STREAM:{text}")
    print(text, end="", flush=True)
    #gui.text_stream(text)

def listen_user_input(wake_word_handler, recorder, elevenlabs, chat_agent, gui):
    def print_and_pass(generator):
        for response in generator:
            gui.queue.put(f"AI_STREAM:{response}")
            print(response, end="", flush=True)
            yield response
    while True:
        wake_word_handler.reset()
        user_text = recorder.text().strip()
        if not user_text:
            continue
        print(f'>>> {user_text}\n<<< ', end="", flush=True)
        gui.queue.put(f"USER_MSG:{user_text}")
        if check_stopword(user_text):
            time.sleep(2)
            gui.queue.put("HIDE_ALL")
            break
        if wake_word_handler.is_triggered():
            chat_agent.history_clear()
        gui.queue.put("START_AI_STREAM")
        agent_response1 = chat_agent.generate_response(user_text, stream=True)
        agent_response2 = print_and_pass(agent_response1)

        elevenlabs.stream(
            elevenlabs.generate(
                text=agent_response2,
                voice=elevenlabs_voices.glados,
                model="eleven_turbo_v2",
                stream=True,
            )
        )


        chat_agent.history_append(chat_agent.response)

def main():
    chat_agent = ChatAI()
    chat_agent.set_system_message(ai_personas.glados)

    wake_word_handler = WakeWordHandler()

    gui = AssistantGUI()

    recorder = AudioToTextRecorder(
        model="tiny.en",
        language="en",
        wake_words="Computer",
        spinner=False,
        post_speech_silence_duration=1.5,
        wake_word_activation_delay=5,
        on_recording_start=lambda: print("on_recording_start"),
        on_recording_stop=lambda: print("on_recording_stop"),
        on_transcription_start=lambda: print("on_transcription_start"),
        enable_realtime_transcription=True,
        #on_realtime_transcription_update=lambda text: my_realtime_transcription_update(text, gui),
        on_realtime_transcription_stabilized=lambda text: my_realtime_transcription_update(text, gui),
        #on_recorded_chunk=lambda data: print("on_recorded_chunk"),
        on_vad_detect_start=lambda: my_start_callback(gui),
        on_vad_detect_stop=lambda: my_stop_callback(gui),
        on_wakeword_detected=lambda: my_wakeword_detected_callback(wake_word_handler),
        on_wakeword_timeout=lambda: my_wakeword_timeout(gui),
    )

    # Create the voice stream and background thread for listening to user input
    elevenlabs.set_api_key(elevenlabs_api_key)

    input_thread = threading.Thread(target=listen_user_input, args=(wake_word_handler, recorder, elevenlabs, chat_agent, gui))
    input_thread.start()

    # Run the UI in the main thread
    gui.run_gui()

if __name__ == '__main__':
    main()
