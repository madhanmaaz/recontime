import colorama

try:
    RED = colorama.Fore.RED
    GREEN = colorama.Fore.GREEN
    CYAN = colorama.Fore.CYAN
    YELLOW = colorama.Fore.YELLOW
    RESET = colorama.Style.RESET_ALL
except:
    RED = ""
    GREEN = ""
    CYAN = ""
    YELLOW = ""
    RESET = ""
