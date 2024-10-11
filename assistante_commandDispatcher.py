import os, sys, json
import requests
import unidecode
import webbrowser
import pygetwindow

from datetime import datetime as dt

from sklearn.feature_extraction.text import CountVectorizer
from sklearn.linear_model import LogisticRegression

from configure__main import Commandlibrary_y, Pathlib_y

def vectorizing(probabilities = {}, data = None, signal = None, taskname=None, DCC = False):
    probabilities = probabilities
    if type(signal) is list:
        signal = signal[0]

    vectorizer = CountVectorizer()
    clf = LogisticRegression()
    vectors = vectorizer.fit_transform(list(data))
    clf.fit(vectors, list(data))

    user_command_vector = vectorizer.transform([signal])
    predicted_probabilities = clf.predict_proba(user_command_vector)
                            
    max_probability = max(predicted_probabilities[0])
    if DCC:
        for i in range(10):
            if max_probability in probabilities.keys(): max_probability += 0.00000000001
            else: break
    probabilities[max_probability] = taskname

    return probabilities

class botInput:

    def __init__(self) -> None:
        
        super(botInput, self).__init__()

    def _PASSIVE(self, *args) -> True: return True
    
    def _WEATHER(self, *args) -> list:
        weatherConfig = Commandlibrary_y.get_openweathermap()
        tempPATH = Pathlib_y.get_mainTEMPpath()
        try:
            res = requests.get(
                "http://api.openweathermap.org/data/2.5/weather",
                params={
                    'id': weatherConfig['city_id'],
                    'units': 'metric',
                    'lang': 'ru',
                    'APPID': weatherConfig['app_id']
                },
                timeout=60)
            data = res.json()

            conditions = data['weather'][0]['description']
            temp = data['main']['temp']

            result = ['w', conditions, temp]

            with open(tempPATH+"/weather.json", "w", encoding='utf-8') as file:
                json.dump(result, file, ensure_ascii=False)

            return result
        
        except Exception as exc:
            print("Weather get ERROR ", exc)
            try:
                with open(tempPATH+"/weather.json", "r", encoding='utf-8') as file:
                    result = json.load(file)
                return ['we', result]
            except:
                return ['e']
            
    def _TIME(self, *args) -> list:
        time = dt.now().strftime("%H:%M:%S")
        hours, minutes, seconds = time.split(":")
        
        if int(list(hours)[0])   == 0: hours   = list(hours)[1]
        if int(list(minutes)[0]) == 0: minutes = list(minutes)[1]
        if int(list(seconds)[0]) == 0: seconds = list(seconds)[1]
        
        time = f"Сейчас: {hours} часов, {minutes} минут, {seconds} секунд"
        return ["t", time]
    
    def _DATE(self, *args) -> list:
        date = dt.now().strftime("%d:%m:%Y")
        day, month, year = date.split(":")
        
        day = day+"-ое"
        month = Commandlibrary_y.get_MONTHS()[int(month)]
        
        date = f"Сегодня: {day} {month}, {year}-ого года"
        return ["d", date]

    def _OFF(self, system_target = False) -> None:
        if system_target: os.system('shutdown -s')
        else: sys.exit()

    def _SYSOUT(self) -> None: self._OFF(True)


class launcher:

    def __init__(self) -> None:
        
        super(launcher, self).__init__()

        self.funcNameDict = {
            "_BROWSER":     self._BROWSER,
            "_YANDEX":      self._YANDEX,
            "_GOOGLE":      self._GOOGLE,
            "_BING":        self._BING,
            "_SETTINGS":    self._SETTINGS,
            "_CMD":         self._CMD,
            "_POWERSHELL":  self._POWERSHELL,
            "_EXPLORER":    self._EXPLORER
        }

    def getAllOpenPrograms(self):
        allWindows = pygetwindow.getAllWindows()
        self.windows = {}
        for i in range(len(allWindows)):
            if allWindows[i].title != "":
                key = allWindows[i].title.encode("utf-8").decode("utf-8").lower()
                key = unidecode.unidecode(key).split(":", 1)[-1]
                if len(key.split(" - ")) > 2: key = "".join(key.split(" - ")[1:])
                self.windows[key] = allWindows[i]

    def openLink(self, link): webbrowser.open_new_tab(link)

    def openOneProgram(self, path): os.startfile(rf"{path}")
    def configureSystemParam(self): pass
    def controlAssistantParam(self): pass

    def closeOneProgram(self, program): program.close()
    def minimizeOneProgram(self, program): program.minimize()
    def maximizeOneProgram(self, program): program.maximize()

    def _SPECIAL(self, CTI):
        if CTI == 1:
            for program in self.windows.values():
                if program.title.lower() not in Commandlibrary_y.get_CDCTRIGGERS():
                    try: program.close()
                    except Exception as exc: print(exc)
        elif CTI == 4:
            for program in self.windows.values(): program.maximize()
        elif CTI == 5:
            for program in self.windows.values(): program.minimize()

    def _BROWSER(self, CTI):
        actions = [webbrowser.open_new_tab, self.control_BROWSER, None, None, self.control_BROWSER, self.control_BROWSER]
        if CTI not in [2, 3]: actions[CTI]("bing.com") if not CTI else actions[CTI](CTI)

    def _YANDEX(self, CTI):
        actions = [webbrowser.open_new_tab, self.control_BROWSER, None, None, self.control_BROWSER, self.control_BROWSER]
        if CTI not in [2, 3]: actions[CTI]("yandex.ru") if not CTI else actions[CTI](CTI)

    def _GOOGLE(self, CTI):
        actions = [webbrowser.open_new_tab, self.control_BROWSER, None, None, self.control_BROWSER, self.control_BROWSER]
        if CTI not in [2, 3]: actions[CTI]("google.com") if not CTI else actions[CTI](CTI)

    def _BING(self, CTI):
        actions = [webbrowser.open_new_tab, self.control_BROWSER, None, None, self.control_BROWSER, self.control_BROWSER]
        if CTI not in [2, 3]: actions[CTI]("bing.com") if not CTI else actions[CTI](CTI)

    def _SETTINGS(self, CTI):
        actions = [os.startfile, self.control_SETTINGS, None, None, self.control_SETTINGS, self.control_SETTINGS]
        if CTI not in [2, 3]: actions[CTI]("ms-settings:windows") if not CTI else actions[CTI](CTI)

    def _CMD(self, CTI):
        actions = [os.startfile, self.control_CMD, None, None, self.control_CMD, self.control_CMD]
        if CTI not in [2, 3]: actions[CTI]("cmd") if not CTI else actions[CTI](CTI)

    def _POWERSHELL(self, CTI):
        actions = [os.startfile, self.control_POWERSHELL, None, None, self.control_POWERSHELL, self.control_POWERSHELL]
        if CTI not in [2, 3]: actions[CTI]("powershell") if not CTI else actions[CTI](CTI)

    def _EXPLORER(self, CTI):
        actions = [os.startfile, self.control_EXPLORER, None, None, self.control_EXPLORER, self.control_EXPLORER]
        if CTI not in [2, 3]: actions[CTI]("explorer") if not CTI else actions[CTI](CTI)

    def control_BROWSER(self, elseType=None):
        browsers_name = Commandlibrary_y.get_browsers()
        self.find = 0
        probabilities, tabClass = {}, None
        for taskname in self.windows.keys():
            for browser in browsers_name:
                browser = unidecode.unidecode(browser)
                if browser in taskname:
                    self.windows[taskname].close()
                    return 1
                browser = [browser, browser+"2"]
                if not self.find:
                    if len(list(taskname.split(" "))) == 1: taskname = taskname + f" {taskname}2"
                    active = taskname.split(" ", 1)

                    try: active = active.remove(" ")
                    except: pass

                    probabilities = vectorizing(probabilities, active, browser, taskname)
        
        if max(probabilities.keys()) < 0.7 and tabClass == None: return 0
        window = self.windows[probabilities[max(probabilities.keys())]]
        {
            1: window.close,
            4: window.maximize,
            5: window.minimize
        }.get(elseType, lambda: None)()

        return 1

    def control_SETTINGS(self, elseType=None): pass

    def control_CMD(self, elseType=None):
        try:
            {
                1:self.windows[[key for key in self.windows.keys() if 'komandnaia stroka' in key or 'cmd' in key][0]].close,
                4:self.windows[[key for key in self.windows.keys() if 'komandnaia stroka' in key or 'cmd' in key][0]].maximize,
                5:self.windows[[key for key in self.windows.keys() if 'komandnaia stroka' in key or 'cmd' in key][0]].minimize
            }.get(elseType, lambda: None)()
            return 1
        except: return 0

    def control_POWERSHELL(self, elseType=None):
        try:
            {
                1:self.windows[[key for key in self.windows.keys() if 'windows powershell' in key][0]].close,
                4:self.windows[[key for key in self.windows.keys() if 'windows powershell' in key][0]].maximize,
                5:self.windows[[key for key in self.windows.keys() if 'windows powershell' in key][0]].minimize
            }.get(elseType, lambda: None)()
            return 1
        except: return 0

    def control_EXPLORER(self, elseType): pass

class startMenu:
    def __init__(self) -> None:
        super(startMenu, self).__init__()

        self.winStartMenuPath = Pathlib_y.get_userprofilePath() +"/AppData/Roaming/Microsoft/Windows/Start Menu/Programs"

    def update_dir(self):
        self.startMenuFolders = {} #
        self.startMenuLnk = {} # .lnk
        self.startMenuIni = {} # .ini

        self.StartMenuPrograms = os.listdir(rf"{self.winStartMenuPath}")

        CDCTRIGGERS = Commandlibrary_y.get_CDCTRIGGERS()

        for item in self.StartMenuPrograms:
            if any(map(lambda x: x in item.lower(), CDCTRIGGERS)):
                self.StartMenuPrograms.remove(item)

        for item in self.StartMenuPrograms:
            item = item.lower()
            if item[-4:] == ".lnk":
                if not any(map(lambda x: x in item, CDCTRIGGERS)):
                    self.startMenuLnk[item.replace(".lnk", "")] = str(self.winStartMenuPath+"/"+item)
            elif item[-4:] == ".ini": self.startMenuIni[item.replace(".ini", "")] = str(self.winStartMenuPath+"/"+item)
            else: self.startMenuFolders[item] = str(self.winStartMenuPath+"/"+item)

        for dir in self.startMenuFolders.values():
            programs = os.listdir(rf"{dir}")
            for item in programs:
                item = item.lower()
                if item[-4:] == ".lnk":
                    item = item.replace(".lnk", "")
                    if item not in self.startMenuLnk:
                        if not any(map(lambda x: x in item, CDCTRIGGERS)):
                            self.startMenuLnk[item] = str(dir+"/"+item+".lnk")

class linkMenu:
    def __init__(self) -> None:
        super(linkMenu, self).__init__()

        self.linkDictPath = Pathlib_y.get_mainLOCALpath() + "/links.json"
        if not os.path.exists(self.linkDictPath):
            with open(self.linkDictPath, "w", encoding="utf-8") as file:
                json.dump(Commandlibrary_y.get_baseLinkDict(), file, ensure_ascii=False)

    def update_link(self):
        with open(self.linkDictPath, "r", encoding="utf-8") as file: self.linkDict = json.load(file)

class commandDispatcher(startMenu, linkMenu, launcher, botInput):

    def __init__(self):

        super(commandDispatcher, self).__init__()

        self.inputCommands = {
            "passive": self._PASSIVE,
            "weather": self._WEATHER,
            "time": self._TIME,
            "date": self._DATE,
            "offbot": self._OFF,
            "sysout": self._SYSOUT
        }

        self.openType = [0,1,4,5]

    def updater(self):
        print("-----------------")
        try:
            print("youshika-es |INFO| dir updating..")
            self.update_dir()
            print("youshika-es |INFO| dir updating successfully.")
            print("youshika-es |INFO| webLink updating..")
            self.update_link()
            print("youshika-es |INFO| webLink updating successfully.")
        except Exception as exc: raise OSError("youshika-es |ERROR| Please check link configuration before restart program\n", exc)
        print("-----------------")
    
    def checkOpenType_NoneFunction(self) -> bool:
        commandtyping = [
            self.openOneProgram,
            self.closeOneProgram,
            None, # Not use
            None, # Not use
            self.maximizeOneProgram,
            self.minimizeOneProgram
        ]

        probabilities = {}
        tabClass = None

        words = unidecode.unidecode(self.signal)
        for taskname in self.windows.keys():
            if words in taskname: tabClass = self.windows[taskname]
            if tabClass is None:
                if len(list(taskname.split(" "))) == 1: taskname = taskname + f" {taskname}2"
                active = taskname.split(" ", 1)

                try: active = active.remove(" ")
                except: pass

                probabilities = vectorizing(probabilities, active, words, taskname, DCC=True)

        if max(probabilities.keys()) < 0.6 and tabClass == None:
            return 0
        if tabClass == None:
            pMPK = probabilities[max(probabilities.keys())]
            if pMPK.split(" ")[0] == pMPK.split(" ")[1]: pMPK = probabilities[max(probabilities.keys())].split(" ")[0]
            tabClass = self.windows[pMPK]

        if self.commandTypeIndex in [1, 4, 5]: commandtyping[self.commandTypeIndex](tabClass)
        if self.commandTypeIndex != 0: commandtyping[self.commandTypeIndex]()
        return 1
    
    def checkOpenType(self) -> bool:
        if self.commandTypeIndex in self.openType:
            # Check open program or link
            if self.commandTypeIndex == 0:
                self.updater()
                function = None
                data = [self.signal] if " " not in self.signal else self.signal.split(" ")
                for word in data:
                    # Check link
                    if word in self.linkDict.keys():
                        try:
                            self.openLink(self.linkDict[word])
                            return 1
                        except: pass
                    # Check program
                    programs = Commandlibrary_y.get_programs()
                    if word in programs.keys():
                        try: function = programs[self.signal.replace(" ", "")]
                        except: function = programs[word]
                # Check start menu
                # --- # --- #
                """probabilities = {} # Programm check
                for program in self.startMenuLnk.keys():
                    if unidecode.unidecode(self.signal) in program or self.signal in program:
                        path = self.startMenuLnk[program]

                    if list(program)[0].lower() in config.RU_ALPH: r = self.signal
                    else: r = unidecode.unidecode(self.signal)

                    if path is None:
                        if len(list(program.split(" "))) == 1: program = program + f" |{program}2"
                        active = program.split(" ", 1)

                        try: active = active.remove(" ")
                        except: pass

                        probabilities = vectorizing(probabilities, active, r, program, DCC=True)

                if max(probabilities.keys()) >= 0.595 or path is not None:
                    if path is None:
                        name = probabilities[max(probabilities.keys())].split(" |", 1)[0]
                        path = self.startMenuLnk[name]
                    try:
                        print(f"Opening -- {path}")
                        self.openOneProgram(path=path)
                        return 1
                    except Exception as exc:
                        print(exc)
                        return 0
                del probabilities"""
                # --- # --- #
                # function return
                if function is not None:
                    self.funcNameDict[function](self.commandTypeIndex)
                    return 1
            else:
                for trigger in Commandlibrary_y.get_SPECIALS():
                    if trigger in self.signal:
                        self._SPECIAL(self.commandTypeIndex)
                        return 1
                    
            result = self.checkOpenType_NoneFunction()
            if result: return 1

        return 0
    
    def defaultChecker(self) -> bool:
        result = self.checkOpenType()
        if result: return 1
        return 0

    def checkCommandAvailable(self, signal = None) -> bool:
        self.signal = signal

        result = 0

        self.commandTypeIndex = None
        self.vectors_probabilities = []
        self.commands = [
            Commandlibrary_y.get_createCommands(),
            Commandlibrary_y.get_destroyCommands(),
            Commandlibrary_y.get_configureCommands(), # not use
            Commandlibrary_y.get_controlCommands(), # not use
            Commandlibrary_y.get_maximizeCommands(),
            Commandlibrary_y.get_minimizeCommands(),
        ]

        for command_list in self.commands:
            vectorizer = CountVectorizer()
            clf = LogisticRegression()
            vectors = vectorizer.fit_transform(list(command_list))
            clf.fit(vectors, list(command_list))
            user_command_vector = vectorizer.transform([self.signal])
            predicted_probabilities = clf.predict_proba(user_command_vector)
            max_probability = max(predicted_probabilities[0])

            self.vectors_probabilities.append(max_probability)

        if max(self.vectors_probabilities) < 0.4: return 0

        self.commandTypeIndex = self.vectors_probabilities.index(max(self.vectors_probabilities))
        if self.commandTypeIndex is None: return 0

        for command in self.commands[self.commandTypeIndex]:
            if command in self.signal:
                try: self.signal = self.signal.replace(command+" ", "")
                except: self.signal = self.signal.replace(" "+command, "")

        self.getAllOpenPrograms()

        if self.commandTypeIndex in self.openType:
            result = self.defaultChecker()
        
        if result: return 1
        return 0
    
    def checkInput(self, signal):
        self.signal = signal if signal[0] != " " else signal[1:]
        command = None

        treshold = 0.275

        vectorizer = CountVectorizer()
        clf = LogisticRegression()

        data_set = Commandlibrary_y.get_data_set()

        vectors = vectorizer.fit_transform(list(data_set.keys()))
        clf.fit(vectors, list(data_set.values()))

        user_command_vector = vectorizer.transform([self.signal])
        predicted_probabilities = clf.predict_proba(user_command_vector)

        max_probabilities = max(predicted_probabilities[0])
        if max_probabilities > treshold:
            command = clf.classes_[predicted_probabilities[0].argmax()].split()[0]
        else:
            for trigger in data_set.keys():
                if trigger in self.signal:
                    command = data_set[f'{trigger}'].split()[0]
        
        if command is None:
            print("None input-commands ->")
            return 0
        else:
            output = self.inputCommands[command]()

            if output is True: return 1

            self.response = None

            if output[0] == 'w':

                self.response = f"LLM Скажи 'Сейчас {output[1]}, " \
                    f"средняя температура - {output[2]} градусов'"
            
            elif output[0] == 'e':

                self.response = 'LLM Скажи "Произошла ошибка.."'
            
            elif output[0] == 'we':

                self.response = \
                    "LLM Скажи 'Из-за ошибки я не могу получить активные данные, однако есть старые:" \
                    f"Сейчас - {output[1][1]}, " \
                    f"средняя температура - {output[1][2]} градусов'"
                
            elif output[0] in ['t', 'd']:

                self.response = output[1]
                
            return 2