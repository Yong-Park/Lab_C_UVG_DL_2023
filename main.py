from postfix import * 
from yalReader import *
from Tree import *

# nombre del archivo que se abrira
filename = "slr-2.yal"
#leer el archivo yal
reader = YalReader(filename)
regex = reader.analize()
print("regex: ", regex)
#convertirlo en su postfix respectivo
post = Postfix()
postfix = post.transform_postfix(regex)
print("\npostfix: ", postfix)
#dibujar su arbol
tree = Tree()
tree.build_tree_from_postfix(postfix)
tree.print_tree()