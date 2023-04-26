from definicion import *

def scan(token):
    if token == 'ws':
         return 
    if token == 'id':
         try:
            return ID
         except NameError:
            return f'Token desconocido: {token}'
    if token == '+':
         try:
            return PLUS
         except NameError:
            return f'Token desconocido: {token}'
    if token == '*':
         try:
            return TIMES
         except NameError:
            return f'Token desconocido: {token}'
    if token == '(':
         try:
            return LPAREN
         except NameError:
            return f'Token desconocido: {token}'
    if token == ')':
         try:
            return RPAREN
         except NameError:
            return f'Token desconocido: {token}'
    return f'Token desconocido: {token}'
