from definicion import *

def scan(token):
    if token == 'ws':
        return 
    if token == 'id':
        return ID
    if token == '+':
        return PLUS
    if token == '*':
        return TIMES
    if token == '(':
        return LPAREN
    if token == ')':
        return RPAREN
    return f'Token desconocido: {token}'
