from definicion import *

def scan(token):
    if token == 'ws':
         try:
            return WHITESPACE
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
    if token == '(*':
         try:
            return LEFTCOMMENT
         except NameError:
            return f'Token desconocido: {token}'
    if token == '*)':
         try:
            return RIGHTCOMMENT
         except NameError:
            return f'Token desconocido: {token}'
    if token == 'let':
         try:
            return LET
         except NameError:
            return f'Token desconocido: {token}'
    if token == '=':
         try:
            return EQ
         except NameError:
            return f'Token desconocido: {token}'
    if token == '|':
         try:
            return OR
         except NameError:
            return f'Token desconocido: {token}'
    if token == '+':
         try:
            return POSITIVE
         except NameError:
            return f'Token desconocido: {token}'
    if token == '*':
         try:
            return KLEENE
         except NameError:
            return f'Token desconocido: {token}'
    if token == '?':
         try:
            return NULLABLE
         except NameError:
            return f'Token desconocido: {token}'
    if token == 'rule':
         try:
            return RULE
         except NameError:
            return f'Token desconocido: {token}'
    if token == 'tokens':
         try:
            return TOKENS
         except NameError:
            return f'Token desconocido: {token}'
    if token == 'word':
         try:
            return WORD
         except NameError:
            return f'Token desconocido: {token}'
    if token == 'digits':
         try:
            return DIGITS
         except NameError:
            return f'Token desconocido: {token}'
    return f'Token desconocido: {token}'
