"""
서버 이름을 한글로 받았을 경우에는 영어로 변환하고
서버 이름을 영어로 받았을 때에는 한글로 변환하는 메소드입니다.
"""


def to_eng(servername):
    if servername == "카인":
        char_server = "cain"
    elif servername == "디레지에":
        char_server = "diregie"
    elif servername == "프레이":
        char_server = "prey"
    elif servername == "카시야스":
        char_server = "casillas"
    elif servername == "힐더":
        char_server = "hilder"
    elif servername == "안톤":
        char_server = "anton"
    elif servername == "바칼":
        char_server = "bakal"
    return char_server


def to_kor(servername):
    if servername == "cain":
        char_server = "카인"
    elif servername is "diregie":
        char_server = "디레지에"
    elif servername is "prey":
        char_server = "프레이"
    elif servername is "casillas":
        char_server = "카시야스"
    elif servername is "hilder":
        char_server = "힐더"
    elif servername is "anton":
        char_server = "안톤"
    elif servername is "bakal":
        char_server = "바칼"
    return char_server
