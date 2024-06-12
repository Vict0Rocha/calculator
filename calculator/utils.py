import re

# Essa expressão regular encontra um número de 0 a 9 ou um . "ponto"
NUM_OR_DOT_REGEX = re.compile(r'^[0-9.]$')


def is_num_or_dot(string: str):
    return bool(NUM_OR_DOT_REGEX.search(string))

# Verificando se o valor recebido é um número valido


def is_valid_number(string: str):
    valid = False
    try:
        float(string)
        valid = True
    except ValueError:
        valid = False
    return valid

# Checando se uma string está vazia


def is_empty(string: str):
    return len(string) == 0


def convert_to_number(string: str):
    number = float(string)

    if number.is_integer():
        number = int(number)

    return number
