import ollama

from json import dump
from datetime import datetime as dt

from configure__main import Pathlib_y, Configuration

class Llama:
    def __init__(self) -> None:
        self.history_path = Pathlib_y.get_mainTEMPpath()+"/llama-chat-history.json"
        # Стандартный промпт для ассистента
        self.prompt = open("prompt.txt", 'r', encoding="utf-8").readlines()[0]
        self.generate = ollama.chat
        self.role = 'system'

        self.status = True

        self.modelName = Configuration.OllamaModelName()
        if self.modelName == "":
            print("Ollama model was not found")
            self.status = False
        else: print("Ollama model: ", self.modelName)

        self.chat_history = {}
        self.context_memory = []
        # Задание стандартного промпта
        self.getResponse()

    def _get_default_prompt_and_role(self) -> any:
        return self.prompt, self.role
    
    def _generate_response(self, prompt, role) -> str:
        self.context_memory.append({'role': role, 'content': prompt})
        response = self.generate(
            model=self.modelName,
            messages=[self.context_memory[0]]+self.context_memory[-8:],
            options={'temperature': 0.0}
            )
    
        self.context_memory[-1]['role'] = 'system'

        return response['message']['content']
    
    def _update_chat_history(self, prompt, response) -> None:
        self.chat_history[prompt] = response

    def getResponse(self, prompt = None) -> str | None:
        if not self.status:
            print("Ollama model was not found, please restart")
            return None
        role = 'user'
        if prompt is None: # Если промпт не задан, то стандартное значение
            prompt, role = self._get_default_prompt_and_role()
        # Получение ответа от Ollama
        response = self._generate_response(prompt, role)
        # Сохранение запроса и ответа в активной истории
        current_time = dt.now().strftime("%H:%M:%S--%d-%m-%Y")
        updated_prompt = f"{prompt} |INFO| {current_time}"
        self._update_chat_history(updated_prompt, response)
        # Возврат ответа
        return response
    
    def _SAVE(self) -> None: # Сохранение истории о сообщениях
        with open(self.history_path, "w", encoding="utf-8") as file:
            dump(self.chat_history, file, ensure_ascii=False)