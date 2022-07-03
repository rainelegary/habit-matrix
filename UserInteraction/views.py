from enum import Enum



class ViewEnum(Enum):
    HOME = "home"
    CALENDAR = "calendar"
    HABITS = "habits"
    RECURRENCES = "recurrences"
    CHECKLISTS = "checklists"



class Views:
    VIEW_STRINGS = [view.value for view in ViewEnum]
    VIEW_STRING_TO_ID = {view.value: view for view in ViewEnum}



class ChangeViewException(Exception):
    def __init__(self, view):
        self.view = view



class ExitException(Exception):
    """exception for exiting the program"""