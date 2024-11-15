import os
import webbrowser
from json import load, dump

from configure_appFounder import search, InstallApplication

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
    # Статус изменения конфигурации приложений False - если изменений не было
    saveOption = False

    @staticmethod # Загружает последний сохраненный файл конфигурации (потеря данных в процессе сессии)
    def __load() -> None:
        Applicator.application = load(open("configs/application.json", "r", encoding="utf-8"))

    @staticmethod # Проверка первой загрузки приложений (при запуске) 
    def checkApplicationLoad():
        if not Applicator.application['settings']['load']:
            Applicator.reloadAppList()

    @staticmethod
    def reloadAppList() -> None:
        """Заново ищет приложения в системе, заменяя уже созданные\n
        Не изменяет сохраненные пользователем приложения (с меткой `user_application=True`)"""
        result = search(set(Applicator.application['settings']['triggers']))
        # Фильтрация пользовательских приложений
        newTempDict = {}
        tempApplicDict = Applicator.getApps().copy()
        tempApplicDict["settings"]["readyApps"] = {}
        tempApplicDict["settings"]["needDataApps"] = {}
        tempApplicDict["settings"]["needAcceptApps"] = {}

        for i, item in enumerate(tempApplicDict.values()):
            if i == 0: # Сохранение настроек
                newTempDict["settings"] = item
                continue
            if item["user_application"]:
                newTempDict[item["name"]] = item
        # Сохранение списка новых приложений
        for app in result:
            app = app.getinfo()
            if app["name"] not in newTempDict:
                newTempDict[app["name"]] = app
        # Общее сохранение
        Applicator.application = newTempDict
        Applicator.__applicationCounter()
        Applicator.saveOption = True

    @staticmethod # Переносит приложения в подходящии словари
    def __applicationCounter() -> None:
        PP, RP = "possible_path", "relative_path"
        ST = "settings"
        RA, NDA, NAA = "readyApps", "needDataApps", "needAcceptApps"
        tempDict = Applicator.getApps().copy()
        tempDict.pop(ST)
        for app in tempDict:
            APD = Applicator.application[app]
            # Если предпологаемый путь отсутствует
            if APD[PP] is None and APD[RP] is None:
                # Требуются данные
                Applicator.application[ST][NDA][app] = APD
            # Если есть предпологаемый путь, но он не точный
            elif APD[PP] is not None and APD[RP] is None:
                # Требуется подтверждение
                Applicator.application[ST][NAA][app] = APD
            # Если есть все вышеп. приложение готово к использованию
            elif APD[PP] is not None and APD[RP] is not None:
                # Ничего не требуется
                Applicator.application[ST][RA][app] = APD[RP]

    @staticmethod # Возвращает общий список приложений
    def getApps() -> dict: return Applicator.application
    @staticmethod # Возвращает список готовых(найденных) приложений
    def getReadyApps() -> dict: return Applicator.application['settings']['readyApps']
    @staticmethod # Возвращает список приложений с отсутствующим путем (не найденных)
    def getNeedDataApps() -> dict: return Applicator.application['settings']['needDataApps']
    @staticmethod # Возвращает список прилоежний с найденным но не точным путем
    def getNeedAcceptApps() -> dict: return Applicator.application['settings']['needAcceptApps']
    @staticmethod # Возвращает количество найденных приложений -1 (словарь с параметрами)
    def getAppsCount() -> int: return len(Applicator.application)-1
    @staticmethod # Возвращает количество готовых к использованию приложений
    def getReadyAppsCount() -> int: return len(Applicator.application['settings']['readyApps'])

    @staticmethod # Добавление нового приложения
    def appendApp(name: str, path: str, user = True):
        Applicator.application[name] = {
            'name': name,
            'relative_path': path,
            'possible_path': path,
            'user_application': True if user else False,
            'status': True
        }
        Applicator.application['settings']['readyApps'][name] = path
        Applicator.saveOption = True

    @staticmethod
    def deleteApp(name: str, appKey = False, readyKey = False, dataKey = False, acceptKey = False, path = None):
        """
        Удаляет приложение из всех словарей если не указано иначе:
        * appKey - удаление данных о приложении. Если True другие параметры воспринимаются как True
        * readyKey - удаление статуса готовности. Переводит приложение в needAcceptApps.
        * dataKey - удаляет статус проверки, переводит в готовность (если указан path).
        Не удаляет данные приложения если appKey - False, иначе полное удаление.
        * acceptKey - удаляет статус неподтвержденного, переводит в готовность.
        Не удаляет данные приложения если appKey - False, иначе полное удаление.
        \n### Пример использования\n
        >>> Applicator.deleteApp('Name', appKey = True) # Удаление приложения из памяти
        >>> Applicator.deleteApp('Name', dataKey = True, Path = 'path') # Когда указан путь к приложению без пути
        >>> Applicator.deleteApp('Name', acceptKey = True # Подтверждение найденного пути у приложения
        """

        if name in Applicator.application and appKey:
            Applicator.application.pop(name, None)
            readyKey, dataKey, acceptKey = True, True, True
            #print("Delete from Applicator")

        keys = ['readyApps', 'needDataApps', 'needAcceptApps']
        
        if name in Applicator.application['settings'][keys[0]] and readyKey:
            if not appKey:
                Applicator.application['settings'][keys[2]][name] = Applicator.application[name]
                #print("Append to NeedAcceptApps")
            Applicator.application['settings'][keys[0]].pop(name)
            #print("Delete from ", keys[0])
        
        if name in Applicator.application['settings'][keys[1]] and dataKey:
            if path is not None and not appKey:
                Applicator.application['settings']['readyApps'][name] = path
                #print("Append to readyApps")
            Applicator.application['settings'][keys[1]].pop(name)
            #print("Delete from ", keys[1])
        
        if name in Applicator.application['settings'][keys[2]] and acceptKey:
            if not appKey:
                if path is None:
                    path = Applicator.application['settings'][keys[2]][name]["possible_path"]
                Applicator.application[name]["relative_path"] = path
                Applicator.application[name]["user_application"] = True
                Applicator.application[name]["status"] = True
                Applicator.application['settings']['readyApps'][name] = path
                #print("Append to readyApps")
            Applicator.application['settings'][keys[2]].pop(name)
            #print("Delete from ", keys[2])

        Applicator.saveOption = True

    @staticmethod
    def updateApp(appName: str, path: str) -> None:
        Applicator.application[appName] = {
            "name": appName,
            "possible_path": path,
            "relative_path": path,
            "user_application": True,
            "status": True
        }
        Applicator.application['settings']['readyApp'][appName] = path
        if appName in Applicator.application['settings']['needDataApps']:
            Applicator.application['settings']['needDataApps'].pop(appName)
        if appName in Applicator.application['settings']['needAcceptApps']:
            Applicator.application['settings']['needAcceptApps'].pop(appName)

        Applicator.saveOption = True

    @staticmethod # Сохранение файла конфигурации (в конце сессии)
    def __save() -> None:
        # Если конфигурация никогда не загружалась
        if not Applicator.application['settings']['load']:
            Applicator.application['settings']['load'] = True
        dump(
            Applicator.application,
            open("configs/application.json", "w", encoding="utf-8"),
            ensure_ascii=False,
            indent=4
        )

    @staticmethod
    def _checkSave(): # Если в процессе были изменены файлы, то сохраняем конфигурацию
        if Applicator.saveOption:
            Applicator.__save()
            Applicator.saveOption = False



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
            prompt = {"role": "system", "content": LlamaConfig.config["standart_prompt"]}
            new_context = [prompt] + old_context
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