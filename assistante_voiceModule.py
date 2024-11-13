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

    def generate(self, text: str, pattern: bool = False, filename: str = None) -> bool:
        self.text = text

        config = App.model()

        result = self.voice.tts(
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
        return result

    def generateReadyAnswer(self):
        texts = Localization.get_ReadyAnsw_lang()
        index = App.modelIndex()
        modelName = App.modelsList()[index]

        _path = Pathlib_y.get_voicePatternspath()
        files = os.listdir(_path)

        i = 0
        ready = False
        
        for file in files:
            if modelName in file: ready = True
        if ready: return
        print("Voice || Generate voice patterns..")

        while i <= 3:
            r = self.generate(texts[i], pattern=True, filename=modelName+texts[i]+".wav")
            if r: i += 1
            else: print(f"Voice || Pattern generate ({texts[i]}) was failed, retrying..")
        
        print("Voice || Success")

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
            print("Voice || Patterns not found")
            self.generateReadyAnswer()
            self.speakReady()