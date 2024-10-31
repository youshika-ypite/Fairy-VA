import time
import speech_recognition as sr

from configure__main import Configuration

from assistante_soundModule import Sound
from commandHandler import ComandHandler

recognizer = sr.Recognizer()
microphone = sr.Microphone()

class Assistant:

    def __init__(self) -> None:
        self.text = ""
        self.whileStatus = True

        self.com_handler = ComandHandler()
        self.soundModule = Sound()

        self.restart = False

        self.import_llama_and_voice()

    def import_llama_and_voice(self) -> None: # Импорт модулей
        if Configuration._CONFIG()['settings']['voiceActive']:
            try:
                print("Voice module load..")
                if not Configuration._import():
                    from assistante_voiceModule import Voice
                    from assistante_llama3_1 import Llama
                    self.voiceModule = Voice()
                    self.llamaModule = Llama()
                    Configuration.loadimport()
                else:
                    self.voiceModule.voice.load()
                print("Voice module loaded successfully.")
            except Exception as exc:
                print("assistant || ", exc)

    def commandHandler(self, text: str) -> bool: # Поиск команд
        botTrigger = self.com_handler.get_botTrigger(text)
        if not botTrigger:
            request = self.com_handler.get_Request(text)
            if not request:
                print("assistant || None commands")
                return None
            else: return True
        else: return False

    def recognize_command(self, text: str):
        RVCtimer, LLMtimer = 0, 0
        speaks = True
        # Если запрос пустой, возвращаемся
        if text in ["",  " ", None]: return
        # Поиск и замена слова триггера, если нету, возвращаемся
        target_word = list(Configuration._TRIGGERS().intersection(text.split()))
        if not target_word: return
        try: text = text.replace(target_word[0]+" ", "")
        except: text = text.replace(" "+target_word[0], "")
        # Поиск комманды
        result = self.commandHandler(text)
        # Если включена генерация голоса
        if Configuration._CONFIG()['settings']['voiceActive']:
            # Если есть команда из botTrigger, берем оттуда ответ
            if result is False: response = self.com_handler.response
            # Если результат команды не требует ответа
            elif result is True:
                speaks = False
                self.voiceModule.speakReady()
            # Иначе обращаемся к модели
            else:
                print(f"Generate response.. --> 0.0")
                start = time.time()
                response = self.llamaModule.getResponse(text)
                if response is None:
                    speaks = False
                    self.soundModule._notify()
                LLMtimer = round(time.time() - start, 2)
                print(f"Response generated. --> {LLMtimer}")

            if speaks:
                print(f"Generate voice.. --> 0.0")
                start = time.time()
                self.voiceModule.generate(response)
                RVCtimer = round(time.time() - start, 2)
                timer = round(LLMtimer+RVCtimer, 2)
                print(f"Voice generated. --> {RVCtimer}")
                print("Speaking..")
                self.voiceModule.speak()
                print("All time spend -> ", timer)

    def callback(self, c_recognizer: sr.Recognizer, audio: sr.AudioData):
        try: # Распознование речи
            text = c_recognizer.recognize_google(audio, language="ru_RU").lower()
            # Распознование команд
            self.recognize_command(text)
        except sr.UnknownValueError as exc: # Речь не найдена
            print("assistant || UnknownValue -> ", exc)
        except sr.RequestError as exc: # Ошибка запроса
            print("assistant || RequestError -> ", exc)

    def start_while(self): # Запуск потока
        print("youshika || Start loop -", time.strftime('%X'))
        self.soundModule._start_listen()
        recognizer.listen_in_background(microphone, self.callback)

        while self.whileStatus:
            # Если не приложение активно
            if not Configuration._CONFIG()['settings']['ATactive']:
                self.stop_while()
                continue
            # Перезапуск
            if self.restart:
                self.restart_while()
                continue
            # Пауза распознования
            while Configuration._PAUSE():
                time.sleep(0.5)
            # Загрузка голосового модуля и Llama
            if Configuration._CONFIG()['settings']['loader']:
                self.import_llama_and_voice()
                Configuration.loaderOFF()
            time.sleep(1)
        self.soundModule._stop_listen()
        print("youshika || Stop loop -", time.strftime('%X'))
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
        if Configuration._CONFIG()['settings']['voiceActive']:
            print("Saving llama chat history..")
            try:
                self.llamaModule._SAVE()
                print("LLama chat history saved success")
            except Exception as exc:
                errorCount += 1
                errors.append(exc)

        print("Save assistant configuration")

        try:
            Configuration.save()
            print("Assistant configuration saved success")
        except Exception as exc:
            errorCount += 1
            errors.append(exc)

        if errorCount == 0: print("Program was closed without errors")
        else: print(f"Program was closed with {errorCount} errors\n||", errors)