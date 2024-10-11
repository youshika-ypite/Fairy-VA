import winsound

from RVC__main import generateTTS
from configure__main import Pathlib_y, Configuration

class Voice():
    def __init__(self) -> None:

        self.voice = generateTTS()
        self.voice.load()
        self.path = Pathlib_y.get_mainLOCALpath()+"/result.wav"

    def generate(self, text: str):
        self.f0_key_up = Configuration._CONFIG()['settings']['voice']['f0_key_up']
        self.f0_method = Configuration._CONFIG()['settings']['voice']['f0_method']
        self.index_rate = Configuration._CONFIG()['settings']['voice']['index_rate']
        self.protect0 = Configuration._CONFIG()['settings']['voice']['protect0']
        self.tts_voice = Configuration._CONFIG()['settings']['voice']['tts']
        self.speed = Configuration._CONFIG()['settings']['voice']['speed']

        self.text = text

        self.voice.tts(
            text,
            
            Configuration._CONFIG()['settings']['voice']['speed'],
            Configuration._CONFIG()['settings']['voice']['tts'],

            Configuration._CONFIG()['settings']['voice']['f0_key_up'],
            Configuration._CONFIG()['settings']['voice']['f0_method'],
            Configuration._CONFIG()['settings']['voice']['index_rate'],
            Configuration._CONFIG()['settings']['voice']['protect0']
        )

    def speak(self): winsound.PlaySound(self.path, winsound.SND_FILENAME)