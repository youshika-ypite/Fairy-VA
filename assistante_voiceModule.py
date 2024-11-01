import os
import random
import winsound

from RVC__main import generateTTS
from configure__main import Pathlib_y, Configuration
from configure_localization import Localization

class Voice():
    def __init__(self) -> None:

        self.voice = generateTTS()
        self.voice.load()
        self.path = Pathlib_y.get_mainLOCALpath()+"/result.wav"
        self.generateReadyAnswer()

    def generate(self, text: str, pattern: bool = False, filename: str =None):
        self.text = text

        self.voice.tts(
            text,
            
            Configuration._CONFIG()['settings']['voice']['speed'],
            Configuration._CONFIG()['settings']['voice']['tts'],

            Configuration._CONFIG()['settings']['voice']['f0_key_up'],
            Configuration._CONFIG()['settings']['voice']['f0_method'],
            Configuration._CONFIG()['settings']['voice']['index_rate'],
            Configuration._CONFIG()['settings']['voice']['protect0'],

            pattern=pattern,
            filename=filename
        )

    def generateReadyAnswer(self):
        texts = Localization.get_ReadyAnsw_lang()
        index = Configuration._CONFIG()['settings']['active']
        modelName = Configuration._CONFIG()['settings']['models'][index]

        _path = Pathlib_y.get_voicePatternspath()
        files = os.listdir(_path)

        ready = False
        
        for file in files:
            if modelName in file: ready = True
        if ready: return
        print("Generate voice patterns..")
        for text in texts:
            self.generate(text, pattern=True, filename=modelName+text+".wav")
        print("Success")

    def speak(self): winsound.PlaySound(self.path, winsound.SND_FILENAME)

    def speakReady(self):
        index = Configuration._CONFIG()['settings']['active']
        modelName = Configuration._CONFIG()['settings']['models'][index]

        _path = Pathlib_y.get_voicePatternspath()
        files = os.listdir(_path)
        
        activeFiles = [file for file in files if modelName in file]
        if activeFiles:
            file = random.choice(activeFiles)
            winsound.PlaySound(_path+"/"+file, winsound.SND_FILENAME)
        else:
            print("Patterns not found")
            self.generateReadyAnswer()
            self.speakReady()