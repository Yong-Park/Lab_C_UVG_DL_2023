# nombre del archivo que se abrira
filename = "sir-1.yal"

#aqui se guardaran todos los let
funciones = []
#aqui se guardaran los regex
regex = []
#para guardar las palabras y ver que se hara con ello segun la funcion que tengan
word = ""
# leer el archivo
with open('sir-1.yal', 'r') as file:
    lines = file.readlines()

print(lines)
print("==============================")
new_lines = []

active_elements = False

for line in lines:
    if active_elements:
        for x in line:
            if x != " " :
                if x != "\n":
                    print(x)
        print()
    if line.startswith("let"):
        funciones.append(line[4:-1])
    
    if line.startswith("rule"):
        active_elements = True
        
print("funciones: ",funciones)
print(new_lines)
