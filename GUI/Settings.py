from GUI.SettingWebsite import SettingWebsite
from typing import List

class Settings():
    """Contains the settigns of the GUI. Used to save them in a file."""

    def __init__(self, RefreshTime: str, SettingWebsites: List[SettingWebsite]):
         self.RefreshTime = RefreshTime
         self.SettingWebsites = SettingWebsites