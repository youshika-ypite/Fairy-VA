from os import environ
from json import load, dump
from datetime import datetime as dt

from configure_appFounder import search

class Pathlib_y:

    userprofilePATH = str(environ["USERPROFILE"]).replace("\\", "/")
    mainLOCALpath   = userprofilePATH + "/AppData/Local/youshika-es"
    mainTEMPpath    = mainLOCALpath + "/cache"

    @staticmethod
    def get_userprofilePath()   -> str: return Pathlib_y.userprofilePATH
    @staticmethod
    def get_mainLOCALpath()     -> str: return Pathlib_y.mainLOCALpath
    @staticmethod
    def get_mainTEMPpath()      -> str: return Pathlib_y.mainTEMPpath
        

class Applicator:

    application = load(open("configs/application.json", "r", encoding="utf-8"))
    applicationcount = len(application)-1
    saveOption = False

    @staticmethod
    def reloadAppList() -> None:
        result = search(set(Applicator.application['settings']['triggers']))
        Applicator.__saveApplicationList(result[0])
        Applicator.__updateHelperCount(result[1])
        Applicator.__save()

    @staticmethod
    def getAppsCount()           ->  int: return Applicator.applicationcount
    
    @staticmethod
    def getReadyApps()           -> dict: return Applicator.application['settings']['readyApps']
    @staticmethod
    def getReadyAppsCount()      ->  int: return Applicator.application['settings']['readyAppslen']

    @staticmethod
    def getNeedDataApps()        -> dict: return Applicator.application['settings']['needDataApps']
    @staticmethod
    def getNeedDataAppsCount()   ->  int: return Applicator.application['settings']['needDataAppslen']

    @staticmethod
    def getNeedAcceptApps()      -> dict: return Applicator.application['settings']['needAcceptApps']
    @staticmethod
    def getNeedAcceptAppsCount() ->  int: return Applicator.application['settings']['needAcceptAppslen']

    @staticmethod
    def deleteReadyApps(): pass
    @staticmethod
    def deleteNeedDataApps(): pass
    @staticmethod
    def deleteNeedAcceptApps(appName: str, appPath: str):
        try: 
            del Applicator.application['settings']['needAcceptApps'][appName]
            Applicator.application['settings']['readyApps'][appName] = appPath
            Applicator.__updateApplication(appName, appPath)
            Applicator.__updateCount()
        except Exception as exc: print("App not found |configure.py 70\n", exc)
    @staticmethod
    def _checkSave():
        if Applicator.saveOption: Applicator.__save()
    # Private functions
    @staticmethod
    def __updateApplication(appName: dict, appPath: str) -> None:
        Applicator.application[appName]['relative_path'] = appPath
        Applicator.application[appName]['possible_path'] = appPath
        Applicator.application[appName]['user_application'] = True
        Applicator.application[appName]['status'] = True
        Applicator.saveOption = True
    @staticmethod
    def __saveApplicationList(applications: list) -> None:
        Applicator.applicationcount = 0
        if applications is None: applications = Applicator.application
        for app in applications:
            app = app.getinfo()
            if app['name'] not in Applicator.application:
                Applicator.application[app['name']] = app
            Applicator.applicationcount += 1
    @staticmethod
    def __updateCount():
        Applicator.application['settings']['readyAppslen']      = Applicator.application['settings']['readyApps'].__len__()
        Applicator.application['settings']['needDataAppslen']   = Applicator.application['settings']['needDataApps'].__len__()
        Applicator.application['settings']['needAcceptAppslen'] = Applicator.application['settings']['needAcceptApps'].__len__()
    @staticmethod
    def __updateHelperCount(counter: list[list]) -> None:
        Applicator.application['settings']['readyAppslen']      = counter[0].__len__()
        Applicator.application['settings']['needDataAppslen']   = counter[1].__len__()
        Applicator.application['settings']['needAcceptAppslen'] = counter[2].__len__()
        # Reload ready, none-data and confirm-type Application
        for item in counter[0]:
            data = item.getinfo()
            name, path = data['name'], data['relative_path']
            Applicator.application['settings']['readyApps'][name] = path
        for item in counter[1]:
            data = item.getinfo()
            name = data['name']
            Applicator.application['settings']['needDataApps'][name] = data
        for item in counter[2]:
            data = item.getinfo()
            name = data['name']
            Applicator.application['settings']['needAcceptApps'][name] = data
    @staticmethod
    def __save() -> None:
        # If Apps configuration never been update
        if not Applicator.application['settings']['load']:
            Applicator.application['settings']['load'] = True
        dump(
            Applicator.application,
            open("configs/application.json", "w", encoding="utf-8"),
            ensure_ascii=False,
            indent=4
        )


class Commandlibrary_y:

    library = load(open("configs/library.json", "r", encoding="utf-8"))
    
    data_set          = library["data_set"]
    CDCTRIGGERS       = library['CDCTRIGGERS']
    programs          = library['programs']
    SPECIALS          = library['SPECIALS']
    browsers          = library['browsers']
    baseLinkDict      = library['weblink']
    createCommands    = library['createCommands']
    destroyCommands   = library['destroyCommands']
    configureCommands = library['configureCommands']
    controlCommands   = library['controlCommands']
    maximizeCommands  = library['maximizeCommands']
    minimizeCommands  = library['minimizeCommands']
    openweathermap    = library['openweathermap']
    RUALPH            = library['RUALPH']
    MONTHS            = library['MONTHS']

    @staticmethod
    def get_library()           -> dict: return Commandlibrary_y.library
    @staticmethod
    def get_data_set()          -> dict: return Commandlibrary_y.data_set
    @staticmethod
    def get_CDCTRIGGERS()       -> list: return Commandlibrary_y.CDCTRIGGERS
    @staticmethod
    def get_programs()          -> dict: return Commandlibrary_y.programs
    @staticmethod
    def get_SPECIALS()          -> list: return Commandlibrary_y.SPECIALS
    @staticmethod
    def get_browsers()          -> list: return Commandlibrary_y.browsers
    @staticmethod
    def get_baseLinkDict()      -> dict: return Commandlibrary_y.baseLinkDict
    @staticmethod
    def get_createCommands()    -> list: return Commandlibrary_y.createCommands
    @staticmethod
    def get_destroyCommands()   -> list: return Commandlibrary_y.destroyCommands
    @staticmethod
    def get_configureCommands() -> list: return Commandlibrary_y.configureCommands
    @staticmethod
    def get_controlCommands()   -> list: return Commandlibrary_y.controlCommands
    @staticmethod
    def get_maximizeCommands()  -> list: return Commandlibrary_y.maximizeCommands
    @staticmethod
    def get_minimizeCommands()  -> list: return Commandlibrary_y.minimizeCommands
    @staticmethod
    def get_openweathermap()    -> dict: return Commandlibrary_y.openweathermap
    @staticmethod
    def get_RUALPH()            -> list: return Commandlibrary_y.RUALPH
    @staticmethod
    def get_MONTHS()            -> dict: return Commandlibrary_y.MONTHS

class Configuration:

    try:config = load(open("configs/config.json", 'r', encoding='utf-8'))
    except Exception as exc: print(exc)

    today = dt.now().strftime("%d-%m-%Y")

    loggingFilePath = Pathlib_y.get_mainTEMPpath() + f"/youshika_log{today}.log"

    @staticmethod
    def _CONFIG() -> dict: return Configuration.config



    @staticmethod
    def _TRIGGERS()     -> set:         return set(Configuration.config['TRIGGERS'])
    @staticmethod
    def _STOPTRIGGERS() -> list:    return Configuration.config['STOPTRIGGERS']
    


    @staticmethod
    def _SETTINGS() -> dict: return Configuration.config['settings']
    @staticmethod
    def _ACTIVE()   -> int : return Configuration.config['settings']['active']
    @staticmethod
    def _PAUSE()    -> bool: return Configuration.config['settings']['pause']

    @staticmethod
    def _import()   -> bool: return Configuration.config['settings']['import']



    @staticmethod
    def update_models(models):
        Configuration.config['settings']['models'] = models
    @staticmethod
    def update_tts(i: int = 0):
        Configuration.config['settings']['voice']['tts'] = Configuration.config['settings']['lang_models'][i]
    @staticmethod
    def update_voice(model):
        Configuration.config['settings']['active'] = Configuration.config['settings']['models'].index(model)
    @staticmethod
    def reverse_active():
        Configuration.config['settings']['voiceActive'] = not Configuration.config['settings']['voiceActive']
    @staticmethod
    def change_speed(value):
        Configuration.config['settings']['voice']['speed'] = value
    @staticmethod
    def change_protect0(value):
        Configuration.config['settings']['voice']['protect0'] = value
    @staticmethod
    def change_f0_key_up(value):
        Configuration.config['settings']['voice']['f0_key_up'] = value



    @staticmethod
    def pause():    Configuration.config['settings']['pause'] = not Configuration.config['settings']['pause']
    @staticmethod
    def stop():     Configuration.config['settings']['ATactive'] = False


    @staticmethod
    def loaderON():  Configuration.config['settings']['loader'] = True
    @staticmethod
    def loaderOFF(): Configuration.config['settings']['loader'] = False


    @staticmethod
    def loadimport():
        Configuration.config['settings']['import'] = True


    @staticmethod
    def save():
        Configuration.config['settings']['import']   = False
        Configuration.config['settings']['ATactive'] = True
        Configuration.config['settings']['pause']    = False
        Configuration.config['settings']['loader']   = False
        dump(
            Configuration.config,
            open("configs/config.json", "w", encoding="utf-8"),
            ensure_ascii=False,
            indent=4
        )