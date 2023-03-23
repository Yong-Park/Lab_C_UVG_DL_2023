# nombre del archivo que se abrira
filename = "slr-2.yal"

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
with open(filename, 'r') as file:
    lines = file.readlines()

# print(lines)
# print("==============================")
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

# print(funciones)
for f in funciones:
    deletable_array = []
    temporal_array = []
    nombre, definicion = f.split("=")
    nombre = nombre.strip()
    definicion = definicion.strip()
    # print("definicion: ", definicion)
    # definicion = definicion.replace('\\t', '\t').replace('\\n', '\n')
    # print("definicion modificada: ", definicion)
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
                    # print(len(word))
                    #estos son los que tienen \
                    if len(word) == 2:
                        deletable_array.append(word)
                    #esto son los que no tienen \
                    else:
                        deletable_array.append(ord(word))
                    word = ""
                    # print("deletable_array: ", deletable_array)
                if word.count('"') == 2:
                    # si tiene \ o no tiene dependiendo de este se trabajara conforme a ello
                    # print("word: ", word)
                    word = word[1:-1]
                    # deletable_array.append(word[1:-1])
                    temporary_word = ""
                    #si tiene \ en word
                    if chr(92) in word:
                        for y in word:
                            temporary_word+=y
                            if temporary_word.count(chr(92)) == 2:
                                deletable_array.append(temporary_word[:-1])
                                temporary_word = temporary_word[2:]
                        if len(temporary_word) != 0:
                            deletable_array.append(temporary_word)
                    else:
                        word = list(word)
                        deletable_array.extend(word)
                        
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
            # print("caracter: ",caracter)
            # print("token_actual: ",token_actual)
            
            if "]" in token_actual:
                palabra = ""
                array = []
                array.append("(")
                
                token_actual[1:-1]
                for tok in token_actual:
                    palabra += tok
                    if palabra.count("'") == 2:
                        palabra = palabra[1:-1]
                        array.append(palabra)
                        array.append("|")
                        palabra = ""
                array[len(array)-1] = ")"
                tokens.extend(array)
                token_actual = ""
            
            if token_actual.count("'") == 2:
                if "[" not in token_actual:
                    token_actual = token_actual[1:-1]
                    tokens.append(token_actual)
                    token_actual = ""
            
            if caracter in ("(", ")", "*", "?", "+", "|","."):
                if "'" not in token_actual:
                    if token_actual:
                        tokens.append(token_actual)
                        token_actual = ""
                    tokens.append(caracter)
                else:
                    token_actual += caracter
            else:
                token_actual += caracter
            # print("tokens: ", tokens)
            # print("==================")
        if token_actual:
            tokens.append(token_actual)
        # print("tokens: ", tokens)
        
        deletable_array.extend(tokens)
        
        
    temporal_array.append(deletable_array)
    
    #agregar temporal array a funciones
    filter_funciones.append(temporal_array)
    # print("filter_funciones antes: ",filter_funciones)
    
    # print(nombre)
    # print(definicion)
# print("filter_funciones: ", filter_funciones)


containPoint = []
#agregar concatenacion a las funciones
for x in range(len(filter_funciones)):
    isFunc = True
    
    #revisar si tiene int
    for c in ["+","*","(",")","?","|"]:
        if c in filter_funciones[x][1]:
            isFunc = False
        
    # print("filter_funciones: ", filter_funciones[x][1])
    # print(isFunc)
    
    if isFunc == False:
        #revisar si tiene .
        result = []
        
        #comenzar a concatenar
        temporal_array = []
        for y in filter_funciones[x][1]:
            temporal_array.append(y)
            temporal_array.append("•")
        #eliminar las concatenaciones inecesarios del funciones
        for z in range(len(temporal_array)):
            if temporal_array[z] == "(":
                if temporal_array[z+1] == "•":
                    temporal_array[z+1] = ''
            if temporal_array[z] == ")":
                if temporal_array[z-1] == "•":
                    temporal_array[z-1] = ''
            if temporal_array[z] == "*":
                if temporal_array[z-1] == "•":
                    temporal_array[z-1] = ''
            if temporal_array[z] == "|":
                if temporal_array[z-1] == "•":
                    temporal_array[z-1] = ''
                if temporal_array[z+1] == "•":
                    temporal_array[z+1] = ''
            if temporal_array[z] == "+":
                if temporal_array[z-1] == "•":
                    temporal_array[z-1] = ''
            if temporal_array[z] == "?":
                if temporal_array[z-1] == "•":
                    temporal_array[z-1] = ''
        temporal_array = [element for element in temporal_array if element != '']
                    
        filter_funciones[x][1] = temporal_array[:-1]
        
    else:
        #revisar si tiene -
        ascii_array=[]
        newString_Array = []
        if '-' in filter_funciones[x][1]:
            for z in range(len(filter_funciones[x][1])):
                if filter_funciones[x][1][z] == '-':
                    for i in range(filter_funciones[x][1][z-1],filter_funciones[x][1][z+1]+1):
                        ascii_array.append(i)
            #convertir el ascii en string otra vez
            for i in ascii_array:
                newString_Array.append(chr(i))
            #reemplazarlo en su respectiva posicion
            filter_funciones[x][1] = newString_Array
        else:
            for z in range(len(filter_funciones[x][1])):
                if type(filter_funciones[x][1][z]) == int:
                    filter_funciones[x][1][z] = chr(filter_funciones[x][1][z])
                    
        #añadir los | en cada uno
        newString_Array = []
        for y in filter_funciones[x][1]:
            newString_Array.append(y)
            newString_Array.append('|')
            
        newString_Array = newString_Array[:-1]
        filter_funciones[x][1] = newString_Array
        
        # print("filter_funciones: ",filter_funciones[x][1])

#agregar () al final y inicial 
# print(filter_funciones)
for func in filter_funciones:
    func[1].insert(0,"(")
    func[1].insert(len(func[1]),")")

print("===================================")
print("funciones:")
for x in filter_funciones:
    print(x)
    
print("\nregex: ", filter_regex)

#comenzar a reemplazar la regex
