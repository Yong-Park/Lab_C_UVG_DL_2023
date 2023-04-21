from definicion import *

def scan(token):
    if token == 'ws':
        return NONE
    if token == 'id':
        if t.value = 0: return ID else: return NONE
    if token == '+':
        return PLUS
    if token == '*':
        return TIMES
    if token == '(':
        return LPAREN
    if token == ')':
        return RPAREN
    if token == '*)':
        return STARTCOMMENT
    return f'Token desconocido: {token}'
