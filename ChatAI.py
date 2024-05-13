
from openai import OpenAI
import os
from dotenv import load_dotenv


load_dotenv()
OPENAI_API_KEY = os.getenv('OPENAI_API_KEY')
OPENAI_MODEL = os.getenv('OPENAI_MODEL')
class ai_agent:
    def __init__(self, api_key=OPENAI_API_KEY, model=OPENAI_MODEL):
        self.api_key = api_key
        self.model = model
        self.client = OpenAI(api_key=self.api_key)
        self.history = []
        self.response = ""
        self.system_message = {'role': 'system', 'content': ''}

    def generate_response(self, message=None, history_count=10, stream=False):
        if message:
            self.history_append(message, 'user')
        self.response = ""
        history_to_use = [self.system_message]
        if len(self.history) > history_count:
            history_to_use.extend(self.history[-history_count:])
        else:
            history_to_use.extend(self.history)
        response = self.client.chat.completions.create(
                model=self.model,
                messages=history_to_use,
                stream=stream)
        if stream:
            for response_chunk in response:
                text_chunk = response_chunk.choices[0].delta.content
                if text_chunk:
                    self.response += text_chunk
                    yield text_chunk
        else:
            response_content = response.choices[0].message.content
            return response_content

    def set_system_message(self, text):
        self.system_message = {'role': 'system', 'content': text}

    def history_append(self, content, role='user'):
        self.history.append({'role': role, 'content': content})

    def history_clear(self):
        self.history = []


def main():
    chat_ai = ai_agent()
    chat_ai.set_system_message("Help the user. Only answer in one sentence.")

    while True:
        # Example usage
        user_query = input("input: ")
        print("AI: ", end='', flush=True)
        for response_chunk in chat_ai.generate_response(user_query, stream=True):
            print(response_chunk, end='', flush=True)
        print()
        chat_ai.history_append(chat_ai.response)
        print(f"chat history:\n{chat_ai.history}\n")

if __name__ == '__main__':
    main()
