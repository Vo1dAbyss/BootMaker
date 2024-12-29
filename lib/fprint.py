import colorama
from colorama import Fore, Style

colorama.init()

def fprint(type: str, text: str, ask=False, end="\n"):
    QUESTION = Fore.MAGENTA+"? "+Fore.WHITE
    INFO = Fore.BLUE+"i "+Fore.WHITE
    WARN = Fore.YELLOW+"! "+Fore.WHITE
    ERROR = Fore.RED+"X "+Fore.WHITE
    SUCCESS = Fore.GREEN+"✓ "+Fore.WHITE

    types = {
        "Q": QUESTION,
        "I": INFO,
        "W": WARN,
        "E": ERROR,
        "S": SUCCESS,
    }

    formatted = types[type]+((Style.BRIGHT+text+Style.NORMAL) if ask==True else text)

    if ask:
        return input(formatted+" >> ")
    
    print(formatted, end=end)