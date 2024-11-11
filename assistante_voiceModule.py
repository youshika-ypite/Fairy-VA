import os
import random
import winsound

from RVC__main import generateTTS
from configure__main import Pathlib_y, App, Localization

class Voice():
    def __init__(self) -> None:

        self.voice = generateTTS()
        self.path = Pathlib_y.get_mainLOCALpath()+"/result.wav"
        self.generateReadyAnswer()

    def generate(self, text: str, pattern: bool = False, filename: str =None):
        self.text = text

        config = App.model()

        self.voice.tts(
            text,
            
            config['speed'],
            config['tts'],

            config['f0_key_up'],
            config['f0_method'],
            config['index_rate'],
            config['protect0'],

            pattern=pattern,
            filename=filename
        )

    def generateReadyAnswer(self):
        texts = Localization.get_ReadyAnsw_lang()
        index = App.modelIndex()
        modelName = App.modelsList()[index]

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
        index = App.modelIndex()
        modelName = App.modelsList()[index]

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