from json import load, dump

class Localization:

    configuration = load(open("configs/localization.json", "r", encoding="utf-8"))



    @staticmethod
    def get_AppLang() -> dict:

        lang = Localization.getLANG()+"_LOCAL"
        return Localization.__get_AppLang(lang)
    
    @staticmethod
    def get_ToolLang() -> dict:

        lang = Localization.getLANG()+"_LOCAL"
        return Localization.__get_ToolLang(lang)
    
    @staticmethod
    def get_NotificateLang() -> dict:

        lang = Localization.getLANG()+"_LOCAL"
        return Localization.__get_NotificateLang(lang)
    
    @staticmethod
    def get_SecondsWinLang() -> dict:

        lang = Localization.getLANG()+"_LOCAL"
        return Localization.__get_SecondsWindLang(lang)
    
    @staticmethod
    def get_MenuLang() -> dict:

        lang = Localization.getLANG()+"_LOCAL"
        return Localization.__get_MenuLang(lang)



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
    def __save():
        dump(
            Localization.configuration,
            open("configs/localization.json", "w", encoding="utf-8"),
            ensure_ascii=False,
            indent=4
            )