import re

# Essa expressão regular encontra um número de 0 a 9 ou um . "ponto"
NUM_OR_DOT_REGEX = re.compile(r'^[0-9.]$')


def is_num_or_dot(string: str):
    return bool(NUM_OR_DOT_REGEX.search(string))

# Checando se uma string está vazia


def is_empty(string: str):
    return len(string) == 0
