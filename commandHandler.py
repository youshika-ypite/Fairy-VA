import os
import json
import requests
import unidecode
import webbrowser
import pygetwindow

from datetime import datetime as dt

from sklearn.feature_extraction.text import CountVectorizer
from sklearn.linear_model import LogisticRegression

from configure__main import Commandlibrary_y, Pathlib_y, App
from configure__main import Applicator

def similarity(list1, list2, round_count = 3) -> float | int:
    """Сравнение матрицами
    >>> Если совпадений нет возвращает 0 иначе (0.0 ; 1.0)
    """
    matrix = [[0 for _ in range(len(list2) + 1)] for _ in range(len(list1) + 1)]

    for i in range(len(list1) + 1):
        matrix[i][0] = i
    for j in range(len(list2) + 1):
        matrix[0][j] = j

    for i in range(1, len(list1) + 1):
        for j in range(1, len(list2) + 1):
            if list1[i - 1] == list2[j - 1]:
                matrix[i][j] = matrix[i - 1][j - 1]
            else:
                matrix[i][j] = min(matrix[i - 1][j] + 1, matrix[i][j - 1] + 1)

    float_result = 1.0 - (matrix[len(list1)][len(list2)] / float(max(len(list1), len(list2))))

    if float_result < 0: result = 0
    else: result = round(float_result, round_count)

    return result


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

    def openOneProgram(self, path) -> None | bool:
        if os.path.isfile(path):
            os.startfile(path)
            return None
        else: return 1

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
        max_diff = 0
        tabClass = None
        for taskname in self.windows.keys():
            request_list = [_ for _ in taskname.lower()]
            seq_kf = {}

            for key in browsers_name:
                if key in taskname:
                    tabClass = taskname 
                    break
                max_diff = similarity(request_list, [_ for _ in key.lower()])
                seq_kf[max_diff] = key

            if seq_kf is not {}:
                max_diff = max(seq_kf.keys())

        if max_diff < 0.7 and tabClass == None: return 0
        if tabClass == None: tabClass = seq_kf[max_diff]

        window = self.windows[tabClass]
        {1: window.close, 4: window.maximize, 5: window.minimize}.get(elseType, lambda: None)()
        return 1

    def control_SETTINGS(self, elseType=None): pass

    def control_CMD(self, elseType=None):
        try:
            obj = self.windows[[key for key in self.windows.keys() if 'komandnaia stroka' in key or 'cmd' in key][0]]
            {1:obj.close, 4:obj.maximize, 5:obj.minimize}.get(elseType, lambda: None)()
            return 1
        except: return 0

    def control_POWERSHELL(self, elseType=None):
        try:
            obj = self.windows[[key for key in self.windows.keys() if 'windows powershell' in key][0]]
            {1:obj.close, 4:obj.maximize, 5:obj.minimize}.get(elseType, lambda: None)()
            return 1
        except: return 0

    def control_EXPLORER(self, elseType): pass



class BotTriggers:

    def _PASSIVE(self) -> True: return True
    def _SYSOUT(self) -> None: self._OFF(True)
    def _OFF(self, system_target: bool = False) -> None:
        Applicator._checkSave()
        App.stopApp()
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

        self.data_set = {
            "open_set": {
                "type": "OPEN",
                "index": 0,
                "full": ['открой', 'запусти', "инициализируй", "включи"],
                "startwith": ['откр', 'запус', "инициализ", "включ"]
            },
            "close_set": {
                "type": "CLOSE",
                "index": 1,
                "full": ["закрой", "выключи", "отключи", "заверши"],
                "startwith": ["закр", "выключ", "отключ", "завер"]
            },
            "max_set": {
                "type": "MAX",
                "index": 2,
                "full": ["выведи", "разверни", "покажи", "раскрой"],
                "startwith": ["вывед", "разверн", "покаж", "раскр"]
            },
            "min_set": {
                "type": "MIN",
                "index": 3,
                "full": ["уведи", "сверни", "скрой", "убери"],
                "startwith": ["увед", "сверн", "скр", "убер"]
            },
            "SPECIALS_set": {
                "type": "SPECIALS",
                "index": 4,
                "full": ["все окна", "всё", "все", "окна"],
                "startwith": [None]
            }
        }

        self.response = None
    
        self.treshold = 0.275
        self.appTreshold = 0.6
        self.commandTreshold = 0.4
        
    def diff_command_search(self, request: str) -> str | bool | str:
        """
        >>> Возвращает "Command not found" если команда не найдена
        >>> Возвращает "App path error - doesn't exists. Path: {_path}" если путь к приложению не существует
        >>> Возвращает bool=1 если команда выполнена
        >>> Возвращает bool=0 если команда не выполнена
        """
        self.request = request
        request_list = [_ for _ in self.request.lower()]
        target = None
        max_kf = []

        for key in self.data_set.keys():
            sequence = []
            for item in self.data_set[key]['full']:
                item_list = [_ for _ in item]
                sequence.append(similarity(request_list, item_list))

            max_kf.append(max(sequence))

        key_i, sw_i  = 0, 0
        keys = [_ for _ in self.data_set.keys()]
        while target is None:
            if key_i == 5: break
            key = keys[key_i]
            if self.data_set[key]['startwith'][0] is None: break
            if self.data_set[key]['startwith'][sw_i] in self.request:
                target = [key, self.data_set[key]['startwith'][sw_i]]
            if sw_i == 3:
                key_i += 1
                sw_i = 0
            else:
                sw_i += 1

        if target is not None:
            min_index = self.request.index(target[1])
            seq = self.request[min_index:]
            for char in seq:
                if char == " " or char == seq[-1]:
                    max_index = self.request.index(char, min_index)
                    self.request = self.request.replace(self.request[min_index:max_index], "")
                    break

            index = self.data_set[target[0]]['index']
        else:
            _max = max(max_kf)
            if _max < 0.175: return "Command not found"
            max_index = max_kf.index(_max)
            index = [_ for _ in self.data_set.values()][max_index]['index']

        self.windows = self.launcher.getAllOpenPrograms()
        
        while self.request[0] == " ":
            self.request = self.request[1:]
        while self.request[-1] == " ": 
            stop = len(self.request)-1
            self.request = self.request[:stop]

        self.index = index
        
        return self.funcs[index]()

    def get_botTrigger(self, request: str) -> bool:
        """
        >>> Возвращает 0 если команда не найдена
        >>> Возвращает 1 если команда найдена (Обход Llama)
        """
        self.request = request
        if self.request[0] == " ":
            self.request = self.request.removeprefix(" ")

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

        if output[0] in ['d', 't']: self.response = output[1]
        else:
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
        return 1

    def _openHandler(self) -> bool:
        self.programs = Commandlibrary_y.get_programs()
        self.linkDict = Commandlibrary_y.get_baseLinkDict()
        
        function = None
        data = [self.request] if " " not in self.request else self.request.split(" ")
        for word in data:
            if word in self.linkDict.keys():
                self.launcher.openLink(self.linkDict[word])
                return 1
            if word in self.programs.keys():
                try: function = self.programs[self.request.replace(" ", "")]
                except: function = self.programs[word]
                self.launcher.funcNameDict[function](self.index)
                return 1

        readyApps = Applicator.getReadyApps()
        _path = None
        active_seq = []

        ITI_search = self.__InToIn_search(readyApps)
        if ITI_search is not None: _path = ITI_search
        if _path is None:
            first_seq = self.__diff_app_search_WUD(readyApps)
            secnd_seq = self.__diff_app_search_UD(readyApps)

            if first_seq is not None: active_seq.append(first_seq)
            if secnd_seq is not None: active_seq.append(secnd_seq)

            if not active_seq: return None

            if len(active_seq) == 1:
                _path = active_seq[0][max(active_seq[0].keys())]
            else:
                if max(active_seq[0].keys()) > max(active_seq[0].keys()):
                    _path = active_seq[0][max(active_seq[0].keys())]
                else:
                    _path = active_seq[1][max(active_seq[1].keys())]

        if _path is not None:
            result = self.launcher.openOneProgram(_path)
            if result is not None: return f"App path error - doesn't exists. Path: {_path}"
            return 1
        return 0
    
    def _closeHandler(self) -> bool:
        if self.__checkSpecials(): return 1
        windowClass = self.__getWindow()
        if windowClass is None: return 0
        self.launcher.closeOneProgram(windowClass)
        return 1

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
                self.launcher._SPECIAL(self.index)
                return 1
        return 0

    def __getWindow(self) -> pygetwindow.Win32Window | None:
        windowClass = None

        words = unidecode.unidecode(self.request)

        request_list = [_ for _ in words.lower()]
        seq_kf = {}

        for key in self.windows.keys():
            if key in words:
                windowClass = key
            max_diff = similarity(request_list, [_ for _ in key.lower()])
            seq_kf[max_diff] = key

        if seq_kf is not {}:
            max_diff = max(seq_kf.keys())

        if max_diff < 0.55 and windowClass == None: return None
        if windowClass == None: windowClass = seq_kf[max_diff]

        window = self.windows[windowClass]

        return window
    
    def __diff_app_search_WUD(self, readyApps: dict) -> dict | None:
        """Поиск без использования `unidecode`"""
        request_list = [_ for _ in self.request.lower()]

        seq_kf = {}

        for key in readyApps.keys():
            max_diff = similarity(request_list, [_ for _ in key.lower()])
            seq_kf[max_diff] = key

        max_diff = max(seq_kf.keys())
        if max_diff < self.appTreshold: return None

        return seq_kf
    
    def __diff_app_search_UD(self, readyApps: dict) -> dict | None:
        """Поиск с использованием `unidecode`"""
        request = unidecode.unidecode(self.request)
        request_list = [_ for _ in request.lower()]

        seq_kf = {}

        for key in readyApps.keys():
            max_diff = similarity(request_list, [_ for _ in key.lower()])
            seq_kf[max_diff] = key

        max_diff = max(seq_kf.keys())
        if max_diff < self.appTreshold: return None

        return seq_kf
    
    def __InToIn_search(self, readyApps: dict) -> str | None:
        """Дословный поиск (включает unidecode проверку)
        >>> Возвращает путь к приложению или `None`"""
        base_req = self.request.lower()
        UDCD_req = unidecode.unidecode(self.request).lower()
        #print(base_req, UDCD_req)

        for app in readyApps.keys():
            if base_req in app.lower() or UDCD_req in app.lower():
                return readyApps[app]
            if len(base_req.split()) > 1:
                for word in base_req.split():
                    if word in app.lower(): return readyApps[app]
            if len(UDCD_req.split()) > 1:
                for word in UDCD_req.split():
                    if word in app.lower(): return readyApps[app]

        return None