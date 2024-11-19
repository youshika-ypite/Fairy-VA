import ollama

from json import dump
from datetime import datetime as dt

from configure__main import Pathlib_y, LlamaConfig

SYSTEM = 'system'
USER = 'user'
ASSISTANT = 'assistant'

class Llama:
    def __init__(self) -> None:
        self.history_path = Pathlib_y.get_mainTEMPpath()+"/llama-chat-history.json"
        # Стандартный промпт для ассистента
        self.prompt = LlamaConfig.currentPrompt()
        self.generate = ollama.chat
        self.role = SYSTEM

        self.status = True
        self.modelName = LlamaConfig.currentModel()
        if self.modelName == "":
            print("Ollama model was not found")
            return None
        else: print("Ollama model: ", self.modelName)
        self.chat_history = {}
        # Задание стандартного промпта
        if LlamaConfig.currentContext()[0] == {}:
            LlamaConfig.setContext([])
            self.getResponse()

    def _get_default_prompt_and_role(self) -> any:
        return self.prompt, self.role
    
    def _generate_response(self, prompt, role) -> str:
        _copt = LlamaConfig.currentOptions()
        
        if role == SYSTEM: _prmpt = []
        else: _prmpt = [LlamaConfig.currentContext()[0]]

        context = LlamaConfig.currentContext()
        index = LlamaConfig.currentContextIndex() * -1

        _cntx = _prmpt + context[index:]
        _msgs = _cntx + [{'role': role, 'content': prompt}]

        response = self.generate(
            model = self.modelName,
            messages = _msgs,
            options = _copt
            )
        
        response_message = response['message']['content']

        LlamaConfig.updateCurrentContext({'role': SYSTEM, 'content': prompt})
        LlamaConfig.updateCurrentContext({'role': ASSISTANT, 'content': response_message})
        LlamaConfig.newResponse(response_message)
        LlamaConfig.setNewContent(True)

        return response_message
    
    def _update_chat_history(self, prompt, response) -> None:
        self.chat_history[prompt] = response

    def getResponse(self, prompt = None) -> str | None:
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
    
    def update(self) -> bool:
        return LlamaConfig.isNewContent()
    
    def _SAVE(self) -> None: # Сохранение истории о сообщениях
        dump(
            self.chat_history,
            open(self.history_path, "w+", encoding="utf-8"),
            ensure_ascii=False,
            indent=4
            )
        LlamaConfig.save()