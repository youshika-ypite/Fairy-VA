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
Applicator.checkApplicationLoad()
print("youshika-es |INFO| found ", Applicator.getAppsCount(), " application.")
print("youshika-es |INFO|", Applicator.getReadyAppsCount(), " ready to use.")
print("youshika-es |INFO| your local path is ", localpath)
print("youshika-es |INFO| your temp path is ", _temppath)

assistante = Assistant()

def load_application():
    app = Application()
    window = app.get_window()
    assistante.setApplicationUpdater(window.__update)
    app.set_exec()

def main():
    applicate = Thread(target=load_application, daemon=True)
    
    applicate.start()
    assistante.start_while()

if __name__ == "__main__":
    main()