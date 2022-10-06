from Language import Language
from colorama import Back, Fore, Style
header = Back.YELLOW + Fore.BLACK + Style.BRIGHT + '[PYTHON IMPROVED]' + Back.RESET + Fore.RESET + Style.RESET_ALL + ' '
parser = Language(graph=False)

def print_output(value):
    print(Fore.RED + Style.DIM + '\t> ' + Fore.LIGHTBLUE_EX + str(value) + 
Fore.RESET + Style.RESET_ALL)

expression = input(header)
while expression.lower().strip() not in ['exit', 'quit']:
    result = parser.parse(expression)
    if result is not None:
        print_output(result)
    expression = input(header)