from postfix import * 
# from yalReader import *
from yalReaderV2 import *
from Tree import *
from DirectAFD import *
from simulation import * 

# nombre del archivo que se abrira
filename = "slr-0.yal"
reader = YalReader(filename)
regex = reader.analize()
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

test = "prueba.txt"
with open(test) as f:
    testLines = f.readlines()

print(direct[1])
    
simulation = Simulation(direct[0],direct[1],testLines)
simulation.simulate()
