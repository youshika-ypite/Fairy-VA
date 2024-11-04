import os
import sys
import json
import requests
import unidecode
import webbrowser
import pygetwindow

from datetime import datetime as dt

from sklearn.feature_extraction.text import CountVectorizer
from sklearn.linear_model import LogisticRegression

from configure__main import Commandlibrary_y, Pathlib_y, Configuration
from configure__main import Applicator

class launcher:

    def __init__(self) -> None:

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

    def getAllOpenPrograms(self) -> dict[str, pygetwindow.Win32Window]:
        allWindows = pygetwindow.getAllWindows()
        self.windows = {}
        for i in range(len(allWindows)):
            if allWindows[i].title != "":
                key = allWindows[i].title.encode("utf-8").decode("utf-8").lower()
                key = unidecode.unidecode(key).split(":", 1)[-1]
                if len(key.split(" - ")) > 2: key = "".join(key.split(" - ")[1:])
                self.windows[key] = allWindows[i]
        return self.windows

    def openLink(self, link): webbrowser.open_new_tab(link)

    def openOneProgram(self, path): os.startfile(rf"{path}")

    def closeOneProgram(self, program): program.close()
    def minimizeOneProgram(self, program): program.minimize()
    def maximizeOneProgram(self, program): program.maximize()

    def _SPECIAL(self, CTI):
        if CTI == 1:
            for program in self.windows.values():
                if program.title.lower() not in Commandlibrary_y.get_CDCTRIGGERS():
                    try: program.close()
                    except Exception as exc: print("youshika-es |ERROR| commandHandler.py _SPECIAL() | ", exc)
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

                    if type(browser) is list:
                        browser = browser[0]

                    vectorizer = CountVectorizer()
                    clf = LogisticRegression()
                    vectors = vectorizer.fit_transform(list(active))
                    clf.fit(vectors, list(active))

                    user_command_vector = vectorizer.transform([browser])
                    predicted_probabilities = clf.predict_proba(user_command_vector)
                                            
                    max_probability = max(predicted_probabilities[0])
                    for i in range(10):
                        if max_probability in probabilities.keys(): max_probability += 0.00000000001
                        else: break
                    probabilities[max_probability] = taskname
        
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



class BotTriggers:

    def _PASSIVE(self) -> True: return True
    def _SYSOUT(self) -> None: self._OFF(True)
    def _OFF(self, system_target: bool = False) -> None:
        Applicator._checkSave()
        Configuration.stop()
        if system_target: os.system('shutdown -s')

    def _WEATHER(self) -> list:
        weatherConfig = Commandlibrary_y.get_openweathermap()
        tempPATH = Pathlib_y.get_mainTEMPpath()
        try:
            result = requests.get(
                "http://api.openweathermap.org/data/2.5/weather",
                params={
                    'id': weatherConfig['city_id'],
                    'units': 'metric',
                    'lang': 'ru',
                    'APPID': weatherConfig['app_id']
                },
                timeout=60)
            data = result.json()
            result = ['w', data['weather'][0]['description'], data['main']['temp']]

            with open(tempPATH+"/weather.json", "w", encoding='utf-8') as file:
                json.dump(result, file, ensure_ascii=False)

            return result
        
        except Exception as exc:
            print("Weather get ERROR ", exc)
            try:
                with open(tempPATH+"/weather.json", "r", encoding='utf-8') as file: return ["we", json.load(file)]
            except:
                return ['e']
            
    def _TIME(self) -> list:
        time = dt.now().strftime("%H:%M:%S")
        hours, minutes, seconds = time.split(":")
        
        if int(list(hours)[0])   == 0: hours   = list(hours)[1]
        if int(list(minutes)[0]) == 0: minutes = list(minutes)[1]
        if int(list(seconds)[0]) == 0: seconds = list(seconds)[1]
        ######################
        #Добавить локализацию#
        ######################
        time = f"Сейчас: {hours} часов, {minutes} минут, {seconds} секунд"
        return ["t", time]
    
    def _DATE(self) -> list:
        date = dt.now().strftime("%d:%m:%Y")
        day, month, year = date.split(":")
        ######################
        #Добавить локализацию#
        ######################
        day = day+"-ое"
        month = Commandlibrary_y.get_MONTHS()[str(month)]
        
        date = f"Сегодня: {day} {month}, {year}-ого года"
        return ["d", date]


class ComandHandler:

    def __init__(self) -> None:

        self.botTriggers = BotTriggers()
        self.launcher = launcher()

        self.linkDictPath = Pathlib_y.get_mainLOCALpath() + "/links.json"
        if not os.path.exists(self.linkDictPath):
            with open(self.linkDictPath, "w", encoding="utf-8") as file:
                json.dump(Commandlibrary_y.get_baseLinkDict(), file, ensure_ascii=False)
        
        self.botCommands = {
            "passive": self.botTriggers._PASSIVE,
            "weather": self.botTriggers._WEATHER,
            "time": self.botTriggers._TIME,
            "date": self.botTriggers._DATE,
            "offbot": self.botTriggers._OFF,
            "sysout": self.botTriggers._SYSOUT
        }

        self.funcs = [
            self._openHandler,
            self._closeHandler,
            self._maximizeHandler,
            self._minimizeHandler
        ]

        self.response = None
    
        self.treshold = 0.275
        self.appTreshold = 0.6
        self.commandTreshold = 0.4

        self.__updater()

    def __updater(self):
        try:
            self.linkDict = self.__update_link()
        except Exception as exc: print("youshika-es |ERROR| CommandHandler.py __updater() | ", exc)
        self.programs = Commandlibrary_y.get_programs()

    def __update_link(self) -> dict:
        with open(self.linkDictPath, "r", encoding="utf-8") as file:
            linkDict = json.load(file)
        return linkDict

    def get_botTrigger(self, request: str) -> bool:
        self.request = request
        if self.request[0] == " ": self.request.removeprefix(" ")

        command = None

        vectorizer = CountVectorizer()
        clf = LogisticRegression()

        data_set = Commandlibrary_y.get_data_set()
        vectors = vectorizer.fit_transform(data_set.keys())
        clf.fit(vectors, list(data_set.values()))

        user_cv = vectorizer.transform([self.request])
        predicted_prob = clf.predict_proba(user_cv)

        max_prob = max(predicted_prob[0])

        if max_prob > self.treshold:
            command = clf.classes_[predicted_prob[0].argmax()].split()[0]
        else:
            for trigger in data_set.keys():
                if trigger in self.request:
                    command = data_set[f'{trigger}'].split()[0]

        if command is None: return 0
        output = self.botCommands[command]()
        if output is None: return 0
        if output[0] in ['d', 't']:
            self.response = output[1]
            return 1

        self.response = None
        ######################
        #Добавить локализацию#
        ######################
        if output[0] == "w":
            self.response = f"Сейчас {output[1]}, " \
            f"средняя температура - {output[2]} градусов."
        elif output[0] == "e":
            self.response = f"Произошла ошибка"
        elif output[0] == "we":
            self.response = \
            "Из-за непредвиденной ошибки я не могу получить активные данные, однако есть старые: "\
            f"Сейчас - {output[1][1]}, средняя температура - {output[1][2]} градусов."
        return 2

    def get_Request(self, request: str) -> bool:
        self.request = request

        commands = [
            Commandlibrary_y.get_createCommands(),
            Commandlibrary_y.get_destroyCommands(),
            Commandlibrary_y.get_maximizeCommands(),
            Commandlibrary_y.get_minimizeCommands()
        ]

        self.commandIndex = 0
        self.v_prob = []

        for command_list in commands:
            vectorizer = CountVectorizer()
            clf = LogisticRegression()

            vectors = vectorizer.fit_transform(list(command_list))
            clf.fit(vectors, list(command_list))

            user_cv = vectorizer.transform([self.request])
            predicted_prob = clf.predict_proba(user_cv)

            max_prob = max(predicted_prob[0])

            self.v_prob.append(max_prob)
        
        if max(self.v_prob) < self.commandTreshold: return 0
        
        self.commandIndex = self.v_prob.index(max(self.v_prob))
        if self.commandIndex is None: return 0
        
        for command in commands[self.commandIndex]:
            if command in self.request:
                try: self.request = self.request.replace(command+" ", "")
                except: self.request = self.request.replace(" "+command, "")

        self.windows = self.launcher.getAllOpenPrograms()
        return self.funcs[self.commandIndex]()

    def _openHandler(self) -> bool:
        function = None
        data = [self.request] if " " not in self.request else self.request.split(" ")
        for word in data:
            if word in self.linkDict.keys():
                self.launcher.openLink(self.linkDict[word])
                return 1
            if word in self.programs.keys():
                try: function = self.programs[self.request.replace(" ", "")]
                except: function = self.programs[word]
                self.launcher.funcNameDict[function](self.commandIndex)
                return 1
            
        readyApps = Applicator.getReadyApps()
        requestUC = unidecode.unidecode(self.request)
        _path = None
        prob = {}
        for app in readyApps.keys():
            if self.request.lower() in app.lower():
                _path = readyApps[app]
                self.launcher.openOneProgram(_path)
                return 1
            
            if requestUC.lower() in app.lower():
                _path = readyApps[app]
                self.launcher.openOneProgram(_path)
                return 1

            if list(app)[0].lower() in Commandlibrary_y.RUALPH: request = self.request
            else: request = requestUC

            app = app.replace("-", "")

            if len(list(app.split())) == 1: app = app + f" |{app}2"
            active = app.split(" ")[:2]
            for item in active:
                if len(item) <= 2:
                    active.remove(item)
                    active.append(active[0]+ f" |{active[0]}2")
                    break

            if type(request) is list: request = request[0]

            vectorizer = CountVectorizer()
            clf = LogisticRegression()
        
            vectors = vectorizer.fit_transform(list(active))
            clf.fit(vectors, list(active))

            user_cv = vectorizer.transform(list(request))
            predicted_prob = clf.predict_proba(user_cv)

            max_probability = max(predicted_prob[0])
            for i in range(10):
                if max_probability in prob.keys(): max_probability += 0.00000000001
                else: break
            prob[max_probability] = app

        if max(prob.keys()) >= self.appTreshold:
            self.launcher.openOneProgram(readyApps[prob[max(prob.keys())]])
            return 1
        return 0
    
    def _closeHandler(self) -> bool:
        if self.__checkSpecials(): return 1
        windowClass = self.__getWindow()
        if windowClass is None: return 0
        self.launcher.closeOneProgram(windowClass)

    def _minimizeHandler(self) -> bool:
        if self.__checkSpecials(): return 1
        windowClass = self.__getWindow()
        if windowClass is None: return 0
        self.launcher.minimizeOneProgram(windowClass)
        return 1

    def _maximizeHandler(self) -> bool:
        if self.__checkSpecials(): return 1
        windowClass = self.__getWindow()
        if windowClass is None: return 0
        self.launcher.maximizeOneProgram(windowClass)
        return 1
    
    def __checkSpecials(self) -> bool:
        for trigger in Commandlibrary_y.get_SPECIALS():
            if trigger in self.request:
                self.launcher._SPECIAL(self.commandIndex)
                return 1
        return 0

    def __getWindow(self) -> pygetwindow.Win32Window | None:
        prob = {}
        windowClass = None

        words = unidecode.unidecode(self.request)
        for taskname in self.windows.keys():
            if words in taskname: windowClass = self.windows[taskname]
            if windowClass is None:
                if len(list(taskname.split())) == 1: taskname = taskname + f" {taskname}2"
                active = taskname.split(" ", 1)

                try: active = active.remove(" ")
                except: pass

                vectorizer = CountVectorizer()
                clf = LogisticRegression()

                vectors = vectorizer.fit_transform(list(active))
                clf.fit(vectors, list(active))

                user_cv = vectorizer.transform([words])
                predicted_prob = clf.predict_proba(user_cv)

                max_prob = max(predicted_prob[0])
                for i in range(10):
                    if max_prob in prob.keys(): max_prob += 0.00000000001
                    else: break
                prob[max_prob] = taskname

        if max(prob.keys()) < self.appTreshold and windowClass == None: return None
        if windowClass == None:
            pMPK = prob[max[prob.keys()]]
            if pMPK.split(" ")[0] == pMPK.split(" ")[1]: pMPK = prob[max(prob.keys())].split()[0]
            windowClass = self.windows[pMPK]

        return windowClass