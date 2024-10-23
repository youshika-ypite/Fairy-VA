import time
import speech_recognition as sr

from configure__main import Configuration

from assistante_soundModule import Sound
from commandHandler import ComandHandler

class Assistant:

    def __init__(self) -> None:

        self.listen = False
        self.blocker = False

        self.response = "Готово!"

        self.duration = 2

        self.oldtime = None

        self._import()
        self._init()
        
        self.speechR = sr.Recognizer()

    def _import(self) -> None:
        if Configuration._CONFIG()['settings']['voiceActive']:
            print("Voice module init..")
            try:
                if not Configuration._import():
                    from assistante_voiceModule import Voice
                    from assistante_llama3_1 import Llama
                    self.voiceModule = Voice()
                    self.llamaModule = Llama()
                    Configuration.loadimport()
                else:
                    self.voiceModule.voice.load()
                print("Voice module init successfully.")
            except Exception as exc: print(exc)
    
    def _init(self) -> None:
        self.com_handler = ComandHandler()
        self.soundModule = Sound()
        
    def __start__(self) -> None:
        print("--- Miko! Start! ---")
        print("Start loop -", time.strftime('%X'))
        print("@youshika--ecosys. ")

    def __close__(self) -> None:
        errorCounter, errors = 0, []
        if Configuration._CONFIG()['settings']['voiceActive']:
            print("Saving llama chat history..")
            try:
                self.llamaModule._SAVE()
                print("Llama chat history saved success")
            except Exception as exc:
                errorCounter += 1
                errors.append(exc)

        print("Save assistant configuration")
        try:
            Configuration.save()
            print("Assistant configuration saved success")
        except Exception as exc:
            errorCounter += 1
            errors.append(exc)
        
        print("--- Miko! Close! ---")
        print("Stop. loop -", time.strftime('%X'))
        if errorCounter == 0: print("Program was closed without errors")
        else: print(f"Program was closed with {errorCounter} errors\n", errors)
        print("@youshika--ecosys. ")

    def __play_trigger__(self, type: int) -> None: # subsequent
        {
             1 :self.soundModule._start_listen,
             0 :self.soundModule._stop_listen,
            -1 :self.soundModule._notify
        }.get(type, lambda : None)()

    def _llama_get_(self, prompt) -> str | None: # subsequent
        return self.llamaModule.getResponse(
            prompt
            ).replace("*", "")
    
    def _voice_speak(self, response) -> None: # subsequent
        self.voiceModule.generate(response)
        print("Speaking..")
        self.voiceModule.speak()

    def _start_listen(self) -> None: # subsequent
        self.__play_trigger__(1)
        self.duration += 2
        self.listen = True
        self.oldtime = time.time()

    def _stop_listen(self) -> None: # subsequent
        self.__play_trigger__(0)
        self.duration -= 2
        self.listen = False
        self.oldtime = None

    def __checkCommand(self, data) -> bool | None:

        botTrigger = self.com_handler.get_botTrigger(data)
        if not botTrigger:
            request = self.com_handler.get_Request(data)
            if not request:
                print("None commands")
                return None
            else: return True
        else:
            return False

    def _recognize(self, data: str) -> None: # recognize command

        result = self.__checkCommand(data)
        
        if Configuration._CONFIG()['settings']['voiceActive']:
            if result is False:
                response = self.com_handler.response
            elif result is True:
                response = self.response
            else:
                response = self._llama_get_(data)
            self._voice_speak(response)

        self._stop_listen()

    def __recognizer(self, data=None) -> None: # check target-word
        if data is None: return
        self.data = data

        target = Configuration._TRIGGERS().intersection(self.data.split())
        if not target: return

        self._start_listen()

    def _listen(self, source):
        while Configuration._CONFIG()['settings']['ATactive']:
            if not self.blocker and not Configuration._PAUSE():
                if Configuration._CONFIG()['settings']['loader']:
                    self._import()
                    Configuration.loaderOFF()
                try:
                    if self.oldtime is not None:
                        if time.time() - self.oldtime > 15:
                            self._stop_listen()
                    audio = self.speechR.record(source, duration=self.duration)
                except Exception as exc: print(__name__, f"timer ERROR\n{exc}")
                try:
                    result = self.speechR.recognize_google(
                        audio,
                        language='ru_RU'
                        ).lower()
                    print(result)
                    if not self.listen:
                        self.__recognizer(result)
                    else:
                        if any(x in result for x in Configuration._STOPTRIGGERS()):
                            self._stop_listen()
                        else: self._recognize(result)
                except Exception as exc: print("main while: ", exc)

    def _listener(self):
        self.__start__()
        with sr.Microphone() as source: self._listen(source)
        self.__close__()