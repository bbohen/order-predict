dic = {
    "header": '\033[95m',
    "okblue": '\033[94m',
    "okgreen": '\033[92m',
    "warning": '\033[93m',
    "fail": '\033[91m',
    "endc": '\033[0m',
    "bold": '\033[1m',
    "underline": '\033[4m'
}

def line(color, text_to_print):
    dic_color = dic[color]
    return dic_color + text_to_print + dic["endc"]
