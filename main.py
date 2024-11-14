from platform import system
if system().lower() != 'windows':
    raise OSError("not Windows/-_-")
import os
from threading import Thread
from configure__main import Pathlib_y, Applicator
from applicate_new import Application
from assistant import Assistant

localpath = Pathlib_y.get_mainLOCALpath()
_temppath = Pathlib_y.get_mainTEMPpath()
voicepath = Pathlib_y.get_voicePatternspath()
if not os.path.exists(localpath): os.mkdir(localpath)
if not os.path.exists(_temppath): os.mkdir(_temppath)
if not os.path.exists(voicepath): os.mkdir(voicepath)
if not Applicator.application['settings']['load']: Applicator.reloadAppList()
#print("youshika-es |INFO| found ", Applicator.applicationcount, " application.")
print("youshika-es |INFO| your local path is ", localpath)
print("youshika-es |INFO| your temp path is ", _temppath)
assistante = Assistant()
applicate = Thread(target=Application, daemon=True)

def main():
    applicate.start()
    assistante.start_while()

if __name__ == "__main__":
    main()