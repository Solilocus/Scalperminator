

class SettingWebsite():
    """GUI settings for one website."""
    
    def __init__(self: str, Url: str, Element: str, ElementValue: str, ElementType: str):
        self.Url = Url
        self.Element = Element
        self.ElementValue = ElementValue
        self.ElementType = ElementType