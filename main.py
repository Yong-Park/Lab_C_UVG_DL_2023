from postfix import * 
# from yalReader import *
from yalReaderV2 import *
from Tree import *
from DirectAFD import *
from simulation import * 

# nombre del archivo que se abrira
# este sera para la lectura del yal respectivo y obtener los tokens al leer su archivo correspondiente
filename = 'slr-1.yal'
reader = YalReader(filename)
regex,token_functions = reader.analize()
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

#realizar su postfix respecntivo
post = Postfix()
postfix = post.transform_postfix(regex)
# print("\npostfix: ", postfix)
#dibujar su arbol
tree = Tree()
tree.build_tree_from_postfix(postfix)
# tree.print_tree()

result = tree.left_most()

afd = DirectAfd(result)
direct= afd.Dstate()
# print(direct[1])
# afd.DirectGraph(direct[0],direct[1])

test = "yalp_test.txt"
with open(test) as f:
    testLines = f.readlines()

# print("token_functions: ", token_functions)
    
simulation = Simulation(direct[0],direct[1],testLines)
test_token = simulation.simulate() # en este tengo guardado el valor a probar, usar el de la izquierda
# print("test_token: ",test_token)

#==============================================================

from scanner import *

with open("result_test.txt", "w") as archivo:
    for s in test_token:
        scanner = scan(s[0])
        archivo.write(f"{s}:{scanner}\n")

# este sera para la lectura del archivo yalp
filename = "yalp_analyzer.yal"
reader = YalReader(filename)
regex,token_functions = reader.analize()

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
# print("simulacion: ", simulacion)
# print("")

# print("______________")
# print("regex: ", regex)
# convertirlo en su postfix respectivo
post = Postfix()
postfix = post.transform_postfix(regex)
# print("\npostfix: ", postfix)
#dibujar su arbol
tree = Tree()
tree.build_tree_from_postfix(postfix)
# tree.print_tree()

result = tree.left_most()

afd = DirectAfd(result)
direct= afd.Dstate()
# print(direct[1])
# afd.DirectGraph(direct[0],direct[1])

test = "slr-1.yalp"
file = "slr-1.yal"
with open(test) as f:
    testLines = f.readlines()

# print("token_functions: ", token_functions)
    
simulation = Simulation(direct[0],direct[1],testLines)
simulacion = simulation.simulate()

# from scanner import *

with open("result.txt", "w") as archivo:
    for s in simulacion:
        scanner = scan(s[0])
        archivo.write(f"{s}:{scanner}\n")

#comenzar a armar el yalp
from yalp_Reader import *
yalp = YalpReader(simulacion, file)
yalp.startConstruct()
yalp.subsetConstruction()
yalp.create_graph()

# print("yalp.productions_copy: ",yalp.productions_copy)
# print("conjuntos: ", yalp.conjuntos)
# print("transiciones: ", yalp.transiciones)

#comenzar a construir el slrparsing
from slrParsing import *
slr_parsing_table = SLRPARSING(yalp.transiciones, yalp.conjuntos, yalp.conjuntos_number, yalp.productions_copy)
slr_parsing_table.constructTable()
slr_parsing_table.draw_table()
slr_parsing_table.simulate()