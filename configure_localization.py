from json import load, dump

RU_TG = "RU_TG"
EN_TG = "ENG_TG"

class Localization:

    mainLang = RU_TG
    configuration = load(open("configs/localization.json", "r", encoding="utf-8"))

    @staticmethod
    def get_AppLang() -> dict:
        
        if Localization.getLANG() == RU_TG: return Localization.__get_AppL_RU()
        else: return Localization.__get_AppL_EN()

    @staticmethod
    def getLANG() -> str: return Localization.configuration['settings']['LANG']

    @staticmethod
    def __get_AppL_RU() -> dict: return Localization.configuration[RU_TG]['App']
    @staticmethod
    def __get_AppL_EN() -> dict: return Localization.configuration[EN_TG]['App']