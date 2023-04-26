from postfix import * 
# from yalReader import *
from yalReaderV2 import *
from Tree import *
from DirectAFD import *
from simulation import * 


# nombre del archivo que se abrira
filename = "sr-yal.yal"
reader = YalReader(filename)
regex,token_functions = reader.analize()
print("______________")
print("regex: ", regex)
# convertirlo en su postfix respectivo
post = Postfix()
postfix = post.transform_postfix(regex)
# print("\npostfix: ", postfix)
#dibujar su arbol
tree = Tree()
tree.build_tree_from_postfix(postfix)
tree.print_tree()

result = tree.left_most()

afd = DirectAfd(result)
direct= afd.Dstate()
# print(direct[1])
afd.DirectGraph(direct[0],direct[1])

test = "slr-1.yal"
with open(test) as f:
    testLines = f.readlines()

print("token_functions: ", token_functions)
    
simulation = Simulation(direct[0],direct[1],testLines)
simulacion = simulation.simulate()

# Abrir el archivo scanner.py para escribir en él
with open("scanner.py", "w") as archivo:
    archivo.truncate(0)
    archivo.write("from definicion import *\n\n")       #llamada de la funcion
    archivo.write("def scan(token):\n")
    for tf in token_functions:
        token, code = tf[0], tf[1]
        # print("code: ", code)
        # print("toke: ", token)
        if code == '':
            archivo.write(f"    if token == '{token}':\n")
            archivo.write("         return ""\n")
        # elif code.startswith("if"):
        #     archivo.write(f"    if token == '{token}':\n")
        #     archivo.write(f"        {code}\n")
        else:
            archivo.write(f"    if token == '{token}':\n")
            archivo.write("         try:\n")
            archivo.write(f"            {code}\n")
            archivo.write("         except NameError:\n")
            archivo.write("            return f'Token desconocido: {token}'\n")
    archivo.write("    return f'Token desconocido: {token}'\n")
archivo.close()
print("simulacion: ", simulacion)
print("")

from scanner import *

with open("result.txt", "w") as archivo:
    for s in simulacion:
        scanner = scan(s[0])
        archivo.write(f"{s}:{scanner}\n")
