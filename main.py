# nombre del archivo que se abrira
filename = "sir-1.yal"

#aqui se guardaran todos los let
funciones = []
filter_funciones = []
ascii_funciones = []
#aqui se guardaran los regex
regex = []
filter_regex = []
#para guardar las palabras y ver que se hara con ello segun la funcion que tengan
word = ""
# leer el archivo
with open('sir-1.yal', 'r') as file:
    lines = file.readlines()

print(lines)
print("==============================")
new_lines = []

active_elements = False

#obtener los elementos
for line in lines:
    #obtener los tokens
    if active_elements:
        temporary_word = ""
        for x in line:
            if x != " " :
                if x != "\n":
                    if x != "'":
                        temporary_word += x
                    if x =="|":
                        regex.append(temporary_word)
                        temporary_word = ""
                else:
                    regex.append(temporary_word)
    #obtener todas sus funciones
    if line.startswith("let"):
        funciones.append(line[4:-1])
    #activar lo de tokens
    if line.startswith("rule"):
        active_elements = True
        
#realizar limpieza de los datos de regex
for x in range(len(regex)):
    temporary_word = ""
    for l in regex[x]:
        temporary_word += l
        if "{" in temporary_word:
            temporary_word = temporary_word[:-1]
            break 
        if "(*" in temporary_word:
            temporary_word = temporary_word[:-2]
            break 
    regex[x] = temporary_word

for x in regex:
    if len(x) != 0:
        filter_regex.append(x)

#limpieza de los datos de funciones

print(funciones)
for f in funciones:
    deletable_array = []
    temporal_array = []
    nombre, definicion = f.split("=")
    nombre = nombre.strip()
    definicion = definicion.strip()
    definicion = definicion.replace('\\t', '\t').replace('\\n', '\n').replace('\\s','\s')
    #agregar el nombre de la funcion
    temporal_array.append(nombre)
    word= ""
    #realizar revision para a definicion
    if definicion[0] == "[":
        definicion = definicion[1:-1]
        for x in definicion:
            word+=x
            if word[0] == '"' or word[0] == "'":
                if word.count("'") == 2:
                    word = word[1:-1]
                    # print("word: ", word)
                    # print(ord(word))
                    deletable_array.append(ord(word))
                    word = ""
                if word.count('"') == 2:
                    deletable_array.append(word[1:-1])
            else:
                # print("word: ", word)
                deletable_array.append(word)
                word = ""
            # print("deletable array: ", deletable_array)
        
        # print(definicion)
        
    else:
        # print("word: ", definicion)
        tokens = []
        token_actual = ""
        
        for caracter in definicion:
            if caracter in ("(", ")", "*", "?", "+", "|"):
                if token_actual:
                    tokens.append(token_actual)
                    token_actual = ""
                tokens.append(caracter)
            else:
                token_actual += caracter

        if token_actual:
            tokens.append(token_actual)
        # print("tokens: ", tokens)
        
        deletable_array.extend(tokens)
        
        
    temporal_array.append(deletable_array)
    
    #agregar temporal array a funciones
    filter_funciones.append(temporal_array)
    # print(nombre)
    # print(definicion)
    print()

print("funciones: ",filter_funciones)
print("regex: ", filter_regex)

