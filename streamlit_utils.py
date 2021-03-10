import re


def is_dni_correct(dni_string):
    if len(dni_string) != 9:
        print("a")
        return False
    if not dni_string[:8].isnumeric():
        print("aa")
        return False
    if not dni_string[-1].isalpha():
        print("aaa")
        return False

    return True


def is_telf_correct(telf):
    if len(telf) != 9:
        return False
    if not telf.isnumeric():
        return False

    return True


def is_mail_correct(mail):
    regex = "[^@]+@[^@]+\.[^@]+"
    if re.search(regex, mail):
        return True
    else:
        return False
