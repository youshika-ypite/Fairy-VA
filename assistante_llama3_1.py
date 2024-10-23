import ollama

from json import dump
from datetime import datetime as dt

from configure__main import Pathlib_y

class Llama:
    def __init__(self) -> None:
        self.history_path = Pathlib_y.get_mainTEMPpath()+"/llama-chat-history.json"

        self.prompt = open("prompt.txt", 'r', encoding="utf-8").readlines()[0]
        self.generate = ollama.chat
        self.role = 'system'

        self.chat_history = {}

        self.getResponse()

    def _get_default_prompt_and_role(self) -> any:
        return self.prompt, self.role
    
    def _generate_response(self, prompt, role) -> str:
        messages = [
            {'role': role, 'content': prompt}
        ]
        return self.generate(
            model='llama3.1',
            messages=messages,
            options={
                'temperature': 0.0
            })['message']['content']
    
    def _update_chat_history(self, prompt, response) -> None:
        self.chat_history[prompt] = response

    def getResponse(self, prompt = None) -> str:
        role = 'user'
        if prompt is None:
            prompt, role = self._get_default_prompt_and_role()

        response = self._generate_response(prompt, role)
        current_time = dt.now().strftime("%H:%M:%S--%d-%m-%Y")
        updated_prompt = f"{prompt} |INFO| {current_time}"
        self._update_chat_history(updated_prompt, response)

        return response
    
    def _SAVE(self) -> None:
        with open(self.history_path, "w", encoding="utf-8") as file:
            dump(self.chat_history, file, ensure_ascii=False)