import os
import winapps
from difflib import SequenceMatcher

def start_menu_searcher() -> list[dict[str, str]]:
    paths = [
        os.path.join(os.environ['USERPROFILE'],
        'AppData', 'Roaming', 'Microsoft', 'Windows', 'Start Menu', 'Programs')]
    t = [
        'python', 'steam', 'desktop', 'powershell', 'tools',
        'unins', 'удал', 'инсталл', 'nsight', 'nvidia', 'profiler',
        'bash', 'cmd', 'gui', 'java', '@', 'help', 'application verifier']
    _pathslinked = {}
    _nameslinked = {}
    for path in paths:
        for root, dirs, files in os.walk(path):
            for file in files:
                if not any([True for i in t if i in str(files).lower()]):
                    _pathslinked[str(files[0])] = os.path.join(root, file)
                    _nameslinked[str(files[0])[:files[0].index(".")]] = str(files[0])

    return [_pathslinked, _nameslinked]

class InstallApplication:

    def __init__(self, name: str, path, uninstall_string=None, append=False) -> None:
        
        if append:
            self.name = name
            self.expectLaunchFile = path
            self.launchFile = path
            return

        self.name = name
        self.install_location = str(path).replace('"', '')
        self.uninstall_string = str(uninstall_string).replace('"', '')

        res = self.install_location if self.install_location not in [
            '', None] else self.uninstall_string

        self.expectLaunchFile = None
        self.launchFile = None
        self.existerror = False

        self.default = res[:res.index(".")+4] if "." in res else res
        self.defaultLOW = self.default.lower()
        if "unins" in self.defaultLOW: self.default = self.default[:self.defaultLOW.index("unins")-1]
        if self.default[1] != ":": return

        if not os.path.exists(self.default): self.default = None
        else:
            if ".exe" in self.default:
                self.expectLaunchFile = self.default
                self.existerror = os.path.isfile(self.expectLaunchFile)
                if not self.existerror: self.launchFile = self.expectLaunchFile
            else:
                self.files = []
                for item in os.listdir(self.default):
                    il = item.lower()
                    if all(
                        [
                            "vc_redist" not in il,
                            "unins" not in il,
                            ".exe" in il
                        ]
                        ):
                        self.files.append(item)
                        self.expectLaunchFile = self.default+"\\"+item
                        nl = self.name.lower()
                        if any(
                            [
                                nl in il,
                                nl.replace(" ", "") in il,
                                nl.replace(" ", "") in il.replace(" ", "")
                            ]
                        ): break
                sequences = {}
                if len(self.files) == 0: return

                # result = get_close_matches(self.name, self.files)

                for file in self.files:
                    sequences[SequenceMatcher(None, file, self.default+"\\"+self.name).ratio()] = file
                max_sequence = max(sequences)
                if max_sequence > 0.2:
                    # Safety
                    if self.default+"\\"+sequences[max_sequence] != self.expectLaunchFile:
                        self.expectLaunchFile = self.default+"\\"+sequences[max_sequence]
                    else:
                        self.launchFile = self.expectLaunchFile
                        
    def getinfo(self) -> dict:
        return {
            "name": self.name,
            "possible_path": self.expectLaunchFile,
            "relative_path": self.launchFile,
            "user_application": False,
            "status": True if self.launchFile is not None else False
        }
    
def search(triggers) -> list[list[InstallApplication]]:
    installed = [x for x in winapps.search_installed()]

    startM = start_menu_searcher()
    startMpaths = startM[0]
    startMnames = startM[1]

    sorteds = [
        InstallApplication(
            x.name, x.install_location, x.uninstall_string
        ) for x in installed if not set(x.name.lower().split()).intersection(triggers)
    ]

    appNames = [app.name.split(maxsplit=1)[0].lower() for app in [item for item in sorteds]]

    for name in startMnames.keys():
        if name.split(maxsplit=1)[0].lower() not in appNames:
            sorteds.append(InstallApplication(
                name=startMnames[name],
                path=startMpaths[startMnames[name]],
                append=True
            ))

    readyApp, needData, needAccept = [], [], []

    for i in [item for item in sorteds]:
        if i.expectLaunchFile is None: needData.append(i)
        else:
            if i.launchFile is None: needAccept.append(i)
            else: readyApp.append(i)

    return [sorteds, [readyApp, needData, needAccept]]