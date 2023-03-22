# # nombre del archivo que se abrira
# filename = "sir-1.yal"

# #aqui se guardaran todos los let
# funciones = []
# #aqui se guardaran los regex
# regex = []
# #para guardar las palabras y ver que se hara con ello segun la funcion que tengan
# word = ""
# # leer el archivo
# with open(filename, "r") as file:
#     content = file.read()

# #obtener todos los valores que se utilizaran
# for x in content:
#     word += x
#     #en caso que es comentario
#     if "(* " in word:
#         if "*)" in word:
#             start = word.find("(*")
#             end = word.find("*)", start) + 2
#             if start != -1 and end != -1:
#                 word = word[:start] + word[end:]
#     #en caso que lea let
#     if "let" in word:
#         if "\n" in word:
#             word = word[4:-1]
#             funciones.append([word])
#             word = ""
#     #cuando lea el rule para los tokens
#     if "rule" in word:
#         temporal_word = ""
#         if "=" in word:
#             if x not in "":
#                 temporal_word += x
#     #en caso que son solo saltos
#     if "\n" in word and ("(*" not in word or "let" not in word or "rule" not in word):
#         word= ""
#         print("word: ", word)
# print(funciones)



with open('sir-1.yal', 'r') as file:
    lines = file.readlines()

print(lines)
print("==============================")
new_lines = []

for line in lines:
    if line.startswith("let") or line.startswith("rule") or line.startswith("tokens"):
        new_lines.append(line)

print(new_lines)


# Crear la lista de funciones
# functions = []
# for line in lines:
#     if line.startswith('let'):
#         parts = line.split('=')
#         function_name = parts[0].strip()
#         function_value = parts[1].strip()
#         functions.append([function_name, function_value])

# # Crear la lista de regex
# regex_line = next(line for line in lines if line.startswith('rule tokens'))
# regex_parts = regex_line.split('=')
# regex = regex_parts[1].strip().split('|')

# # Imprimir los resultados
# print('Funciones:', functions)
# print('Regex:', regex)



