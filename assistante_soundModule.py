import winsound
class Sound:
    def _start_listen(self): winsound.PlaySound("C:/Windows/Media/Speech On.wav",    winsound.SND_ASYNC)
    def _stop_listen(self):  winsound.PlaySound("C:/Windows/Media/Speech Sleep.wav", winsound.SND_ASYNC)
    def _notify(self):       winsound.PlaySound("C:/Windows/Media/Speech Off.wav",   winsound.SND_ASYNC)