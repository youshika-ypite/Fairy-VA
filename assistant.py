import time
import winsound
import speech_recognition as sr

from configure__main import App

from commandHandler import ComandHandler

recognizer = sr.Recognizer()
microphone = sr.Microphone()

class Sound:
    def _start_listen(self):
        winsound.PlaySound("C:/Windows/Media/Speech On.wav", winsound.SND_ASYNC)
    def _stop_listen(self): 
        winsound.PlaySound("C:/Windows/Media/Speech Sleep.wav", winsound.SND_ASYNC)
    def _notify(self):
        winsound.PlaySound("C:/Windows/Media/Speech Off.wav", winsound.SND_ASYNC)

class Assistant:

    def __init__(self) -> None:
        self.text = ""
        self.whileStatus = True

        self.com_handler = ComandHandler()
        self.soundModule = Sound()

        self.restart = False

        self.import_llama_and_voice()

    def import_llama_and_voice(self) -> None: # Импорт модулей
        if App.voiceModule():
            try:
                print("youshika || Voice module load..")
                App.setPause()
                if not App.voiceLoad():
                    from assistante_voiceModule import Voice
                    from assistante_llama3_1 import Llama
                    self.voiceModule = Voice()
                    self.llamaModule = Llama()
                else:
                    self.voiceModule.voice.load()
                App.setPause()
                print("youshika || Voice module loaded successfully.")
            except Exception as exc:
                print("youshika ||  ", exc)
                self.soundModule._notify()

    def response_clear(self, response) -> str:
        items = ["*"]
        for i in items:
            if i in response:
                response = response.replace(i, "")
        
        return response

    def commandHandler(self, text: str) -> bool | None: # Поиск команд
        """
        >>> Возвращает True если команда не требует ответа
        >>> Возвращает False если команда заимствует ответ
        >>> Возвращает None если команда не найдена\
 (Передача в ollama если включен голосовой модуль)
        """
        botTrigger = self.com_handler.get_botTrigger(text)
        if not botTrigger:
            request = self.com_handler.diff_command_search(text)
            if type(request) is str:
                print(request)
                return None
            elif request: return True
            return None
        else: return False

    def recognize_command(self, text: str):
        RVCtimer, LLMtimer = 0, 0
        speaks = True
        # Поиск и замена слова триггера, если нету, возвращаемся
        target_word = list(App.TRIGGERS().intersection(text.split()))
        if not target_word: return
        text = text.replace(target_word[0], "")
        # Если запрос пустой, возвращаемся
        if text in ["",  " ", None]: return
        # Поиск комманды
        result = self.commandHandler(text)
        # Если включена генерация голоса
        if App.voiceModule():
            # Если есть команда из botTrigger, берем оттуда ответ
            if result is False: response = self.com_handler.response
            # Если результат команды не требует ответа
            elif result is True:
                speaks = False
                self.voiceModule.speakReady()
            # Иначе обращаемся к модели
            else:
                print("LLM || Generate response.. --> 0.0")
                print("LLM || Request:", text)
                start = time.time()
                response = self.llamaModule.getResponse(text)
                if response is None:
                    speaks = False
                    self.soundModule._notify()
                LLMtimer = round(time.time() - start, 2)
                print(f"LLM || Response generated. --> {LLMtimer}")

            if speaks:
                print(f"RVC || Generate voice.. --> 0.0")
                start = time.time()
                response = self.response_clear(response)
                self.voiceModule.generate(response)
                RVCtimer = round(time.time() - start, 2)
                timer = round(LLMtimer+RVCtimer, 2)
                print(f"RVC || Voice generated. --> {RVCtimer}")
                print("RVC || Speaking..")
                self.voiceModule.speak()
                print("assistant || All time spend -> ", timer)
        print("assistant || listening..")

    def callback(self, c_recognizer: sr.Recognizer, audio: sr.AudioData):
        try: # Распознование речи
            text = c_recognizer.recognize_google(audio, language="ru_RU").lower()
            # Распознование команд
            print("assistant || Found text:", text)
            self.recognize_command(text)
        except sr.UnknownValueError as exc: # Речь не найдена
            print("assistant || UnknownValue -> None speech")
        except sr.RequestError as exc: # Ошибка запроса
            self.soundModule._notify()
            print("assistant || RequestError -> ", exc)

    def start_while(self): # Запуск потока
        print("assistant || Start loop -", time.strftime('%X'))
        self.soundModule._start_listen()
        recognizer.listen_in_background(microphone, self.callback)

        while self.whileStatus:
            # Если не приложение активно
            if not App.ACTIVE():
                self.stop_while()
                continue
            # Перезапуск
            if self.restart:
                self.restart_while()
                continue
            # Пауза распознования
            while App.PAUSE():
                if not App.ACTIVE():
                    self.stop_while()
                time.sleep(1)
            # Загрузка голосового модуля и Llama
            if App.LOAD():
                self.import_llama_and_voice()
                App.reLOAD()
            time.sleep(1)
        self.soundModule._stop_listen()
        print("assistant || Stop loop -", time.strftime('%X'))
        self.whileStatus = None

    def restart_while(self):
        self.whileStatus = False
        while self.whileStatus in [True, False]:
            time.sleep(0.2)
        self.whileStatus = True
        self.restart = False
        self.start_while()

    def stop_while(self): # Остановка потока и сохранение данных
        self.whileStatus = False
        errorCount, errors = 0, []
        if App.voiceModule():
            print("youshika || Saving llama chat history..")
            try:
                self.llamaModule._SAVE()
                print("youshika || LLama chat history saved success")
            except Exception as exc:
                errorCount += 1
                errors.append(exc)

        print("youshika || Save assistant configuration")

        try:
            App.save()
            print("youshika || Assistant configuration saved success")
        except Exception as exc:
            errorCount += 1
            errors.append(exc)

        if errorCount == 0: print("youshika || Program was closed without errors")
        else: print(f"youshika || Program was closed with {errorCount} errors\n||", errors)