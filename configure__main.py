import os
import webbrowser
from json import load, dump

from configure_appFounder import search

class Pathlib_y:

    userprofilePATH   = str(os.environ["USERPROFILE"]).replace("\\", "/")
    mainLOCALpath     = userprofilePATH + "/AppData/Local/youshika-es"
    mainTEMPpath      = mainLOCALpath + "/cache"
    voicePatternspath = mainLOCALpath + "/voicePatterns"

    @staticmethod
    def get_userprofilePath()   -> str: return Pathlib_y.userprofilePATH
    @staticmethod
    def get_mainLOCALpath()     -> str: return Pathlib_y.mainLOCALpath
    @staticmethod
    def get_mainTEMPpath()      -> str: return Pathlib_y.mainTEMPpath
    @staticmethod
    def get_voicePatternspath() -> str: return Pathlib_y.voicePatternspath
        

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
    def getApps()                -> dict: return Applicator.application
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
    def appendApp(name: str, path: str):
        Applicator.application[name] = {
            'name': name,
            'relative_path': path,
            'possible_path': path,
            'user_application': True,
            'status': True
        }
        Applicator.application['settings']['readyApps'][name] = path
        Applicator.applicationcount += 1
        Applicator.saveOption = True
        Applicator.__updateCount()

    @staticmethod
    def deleteApp(name: str):
        try: del Applicator.application[name]
        except KeyError as exc_ke: print("Not found", exc_ke)
        for ctg in ['readyApps', 'needDataApps', 'needAcceptApps']:
            try:
                del Applicator.application['settings'][ctg][name]
                print("Found")
            except Exception as exc_ke: print(f"can't find {name} in {ctg}\n", exc_ke)
        Applicator.applicationcount -= 1
        Applicator.saveOption = True
        Applicator.__updateCount()

    @staticmethod
    def deleteReadyApps(appName: str, appPath: str = None): Applicator.deleteApp(appName)
    @staticmethod
    def deleteNeedDataApps(appName: str, appPath: str, deleteAction: bool = False):
        try: 
            del Applicator.application['settings']['needDataApps'][appName]
            if not deleteAction: Applicator.application['settings']['readyApps'][appName] = appPath
            Applicator.__deleteUpdater(appName, appPath, 0 if not deleteAction else 1)
        except Exception as exc: print(f"App not found |configure.py | {appName}\n", exc)
    @staticmethod
    def deleteNeedAcceptApps(appName: str, appPath: str, deleteAction: bool = False):
        try: 
            del Applicator.application['settings']['needAcceptApps'][appName]
            if not deleteAction: Applicator.application['settings']['readyApps'][appName] = appPath
            Applicator.__deleteUpdater(appName, appPath, 0 if not deleteAction else 1)
        except Exception as exc: print(f"App not found |configure.py | {appName}\n", exc)
    @staticmethod
    def _checkSave():
        if Applicator.saveOption: Applicator.__save()
    # Private functions
    @staticmethod
    def __deleteUpdater(name: str = None, path: str = None, flg: bool = 0):
        """Only DRA | DNDA | DNAA"""
        if not flg:
            Applicator.__updateApplication(name, path)
        else:
            Applicator.deleteApp(name)
            Applicator.saveOption = True

        Applicator.__updateCount()
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
    @staticmethod
    def __load() -> None:
        Applicator.application = load(open("configs/application.json", "r", encoding="utf-8"))
        Applicator.applicationcount = len(Applicator.application)-1



class Commandlibrary_y:

    library = load(open("configs/library.json", "r", encoding="utf-8"))

    @staticmethod
    def get_library() -> dict: return Commandlibrary_y.library
    @staticmethod
    def get_data_set() -> dict: return Commandlibrary_y.library["data_set"]
    @staticmethod
    def get_CDCTRIGGERS() -> list: return Commandlibrary_y.library['CDCTRIGGERS']
    @staticmethod
    def get_programs() -> dict: return Commandlibrary_y.library['programs']
    @staticmethod
    def get_SPECIALS() -> list: return Commandlibrary_y.library['SPECIALS']
    @staticmethod
    def get_browsers() -> list: return Commandlibrary_y.library['browsers']
    @staticmethod
    def get_baseLinkDict() -> dict: return Commandlibrary_y.library['weblink']
    @staticmethod
    def get_createCommands() -> list: return Commandlibrary_y.library['createCommands']
    @staticmethod
    def get_destroyCommands() -> list: return Commandlibrary_y.library['destroyCommands']
    @staticmethod
    def get_maximizeCommands() -> list: return Commandlibrary_y.library['maximizeCommands']
    @staticmethod
    def get_minimizeCommands() -> list: return Commandlibrary_y.library['minimizeCommands']
    @staticmethod
    def get_openweathermap() -> dict: return Commandlibrary_y.library['openweathermap']
    @staticmethod
    def get_RUALPH() -> list: return Commandlibrary_y.library['RUALPH']
    @staticmethod
    def get_MONTHS() -> dict: return Commandlibrary_y.library['MONTHS']
        

class App:

    config = load(open("configs/settings.json", "r", encoding="utf-8"))
    links = ["https://github.com/youshika-ypite", "https://boosty.to/ypite"]

    @staticmethod
    def search():
        """Поиск и **замена** моделей в папке `weights`"""
        model_root = "weights"
        models = [d for d in os.listdir(model_root) if os.path.isdir(os.path.join(model_root, d))]
        if len(models) == 0: raise ValueError("tts-out || No model found in `weights` folder")
        models.sort()
        App.updateModels(models)

    @staticmethod
    def save(): # Сохранение данных (сброс значений)
        App.config["appStatus"] = True
        App.config["pauseStatus"] = False
        App.config["voiceLoad"] = False
        dump(
            App.config,
            open("configs/settings.json", "w", encoding="utf-8"),
            ensure_ascii=False,
            indent=4)

    @staticmethod
    def load(): # Загрузка данных
        App.config = load(open("configs/settings.json", 'r', encoding='utf-8'))


    @staticmethod # Возвращает триггеры (Имена) ассистента
    def TRIGGERS() -> list: return set(App.config["TRIGGERS"])

    @staticmethod # Возвращает статус всего приложения
    def ACTIVE() -> bool: return App.config["appStatus"]
    @staticmethod # Возвращает статус паузы распознования
    def PAUSE() -> bool: return App.config["pauseStatus"]
    @staticmethod # Возвращает статус режима "Генерации"
    def voiceModule() -> bool: return App.config["voiceModule"]
    @staticmethod # Возвращает статус "Загрузки моделей"
    def voiceLoad() -> bool: return App.config["voiceLoad"]

    @staticmethod # Возвращает настройки для генерации
    def voice() -> dict: return App.config["voice"]

    @staticmethod # Возвращает настройки для tts
    def model() -> dict: return App.voice()["model"]
    @staticmethod # Возвращает список найденных RVC моделей
    def modelsList() -> list: return App.voice()["modelsList"]
    @staticmethod # Возвращает индекс активной модели из списка
    def modelIndex() -> int : return App.voice()["modelIndex"]
    @staticmethod # Возвращает список основных моделей голосов
    def based_Mods() -> list: return App.voice()["based_Mods"]

    @staticmethod # Возвращает словарь временных статусов
    def temp() -> dict: return App.config["temp"]

    @staticmethod # Возвращает статус этапа загрузки по ум. - false
    def LOAD() -> bool: return App.temp()["toLOAD"]
    @staticmethod
    def reLOAD() -> bool:
        """Переключает статус этапа загрузки на противоположный,
        возвращает итоговый статус"""
        App.config["temp"]["toLOAD"] = not App.LOAD()
        return App.LOAD()
    @staticmethod
    def setVoiceLoad():
        App.config["voiceLoad"] = True

    @staticmethod
    def reverseVoiceModule():
        """Переключает статус активного режима 'генерации'"""
        App.config["voiceModule"] = not App.voiceModule()

    @staticmethod
    def updateVoiceModule(model_name: str):
        """На вход получает имя модели.
        Находит ее индекс в списке моделей и заменяет его"""
        App.config["voice"]["modelIndex"] = App.modelsList().index(model_name)

    @staticmethod
    def updateBasedModels(model_index: int):
        """На вход получает индекс модели
        Заменяет активную базовую модель по индексу в списке"""
        App.config["voice"]["model"]["tts"] = App.based_Mods()[model_index]

    @staticmethod # Изменяет значение паузы на противоположное
    def setPause() -> None: App.config["pauseStatus"] = not App.PAUSE()

    @staticmethod # Останавливает программу
    def stopApp() -> None: App.config["appStatus"] = not App.ACTIVE()

    @staticmethod # Изменение параметра скорости - speed (tts)
    def change_speed(value): App.config["voice"]["model"]["speed"] = value
    @staticmethod # Изменение параметра защиты - protect0 (tts)
    def change_protect0(value): App.config["voice"]["model"]["protect0"] = value
    @staticmethod # Изменение параметра темпа - f0_key_up (tts)
    def change_f0_key_up(value): App.config["voice"]["model"]["f0_key_up"] = value

    @staticmethod # Обновление списка моделей
    def updateModels(models: list) -> None:
        App.config["voice"]["modelsList"] = models


    @staticmethod
    def open(linkID: int):
        """
        * 0 - GitHub
        * 1 - Support
        """
        webbrowser.open(App.links[linkID])

class LlamaConfig:

    config = load(open("configs/llama.json", "r", encoding="utf-8"))

    @staticmethod
    def save(): # Сохранение данных
        dump(LlamaConfig.config,
             open("configs/llama.json", "w", encoding="utf-8"),
             ensure_ascii=False,
             indent=4)

    @staticmethod
    def currentConfig() -> dict:
        return LlamaConfig.config
    @staticmethod
    def currentModel() -> str:
        return LlamaConfig.config['modelName']
    @staticmethod
    def currentOptions() -> dict:
        return LlamaConfig.config['options']
    @staticmethod
    def currentPrompt() -> str:
        return LlamaConfig.config['standart_prompt']
    @staticmethod
    def currentContextIndex() -> int:
        return LlamaConfig.config['context_memory']*-1
    @staticmethod
    def currentContext() -> list:
        return LlamaConfig.config['context']
    
    @staticmethod
    def updateCurrentContext(msg):
        context = LlamaConfig.currentContext()
        context.append(msg)
        LlamaConfig.setContext(context)
        
    @staticmethod
    def setCurrentContextIndex(index: int):
        LlamaConfig.config['context_memory'] = index
        LlamaConfig.save()

    @staticmethod
    def setCurrentTemperatureCount(count: float):
        LlamaConfig.config['options']['temperature'] = count
        LlamaConfig.save()

    @staticmethod
    def setCurrentPrompt(text: str, apply: bool = False):
        LlamaConfig.config['standart_prompt'] = text
        if apply: LlamaConfig.save()

    @staticmethod
    def setModelName(name: str):
        LlamaConfig.config['modelName'] = name

    @staticmethod
    def setContext(context: list[dict]):
        LlamaConfig.config['context'] = context
        

    @staticmethod
    def clearContext(prompt = False) -> bool:
        if prompt:
            old_context = LlamaConfig.config["context"][1:]
            new_context = [LlamaConfig.config["standart_prompt"]] + old_context
            LlamaConfig.config["context"] = new_context
            LlamaConfig.save()
        else:
            LlamaConfig.config["context"] = [LlamaConfig.config["context"][0]]


class Localization:

    configuration = load(open("configs/localization.json", "r", encoding="utf-8"))

    @staticmethod
    def get_AppLang() -> dict:

        lang = Localization.getLANG()
        return Localization.__get_AppLang(lang)
    
    @staticmethod
    def get_ToolLang() -> dict:

        lang = Localization.getLANG()
        return Localization.__get_ToolLang(lang)
    
    @staticmethod
    def get_NotificateLang() -> dict:

        lang = Localization.getLANG()
        return Localization.__get_NotificateLang(lang)
    
    @staticmethod
    def get_SecondsWinLang() -> dict:

        lang = Localization.getLANG()
        return Localization.__get_SecondsWindLang(lang)
    
    @staticmethod
    def get_MenuLang() -> dict:

        lang = Localization.getLANG()
        return Localization.__get_MenuLang(lang)
    
    @staticmethod
    def get_ReadyAnsw_lang() -> list:

        lang = Localization.getLANG()
        return Localization.__get_ReadyAnswLang(lang)
    
    @staticmethod
    def get_ChangerLang() -> dict:

        lang = Localization.getLANG()
        return Localization.__getChangerLang(lang)

    @staticmethod
    def getLANG() -> str:
        return Localization.configuration['settings']['LANG']
    
    @staticmethod
    def changeLang(lang: str):

        lang += "_TG"
        if lang in ["RU_TG", "EN_TG"]:
            Localization.configuration['settings']['LANG'] = lang
            Localization.__save()

    @staticmethod
    def __get_AppLang(lang) -> dict:
        return Localization.configuration[lang]['App']
    
    @staticmethod
    def __get_ToolLang(lang) -> dict:
        return Localization.configuration[lang]['ToolTips']
    
    @staticmethod
    def __get_NotificateLang(lang) -> dict:
        return Localization.configuration[lang]['NotificateTexts']
    
    @staticmethod
    def __get_SecondsWindLang(lang) -> dict:
        return Localization.configuration[lang]['SecondsWin']
    
    @staticmethod
    def __get_MenuLang(lang) -> dict:
        return Localization.configuration[lang]['Menu']
    
    @staticmethod
    def __get_ReadyAnswLang(lang) -> list:
        return Localization.configuration[lang]['ReadyAnswers']
    
    @staticmethod
    def __getChangerLang(lang) -> dict:
        return Localization.configuration[lang]['Changer']

    

    @staticmethod
    def __save():
        dump(
            Localization.configuration,
            open("configs/localization.json", "w", encoding="utf-8"),
            ensure_ascii=False,
            indent=4
            )