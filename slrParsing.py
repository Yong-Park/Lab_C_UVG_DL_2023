import copy

class SLRPARSING:
    def __init__(self, transitions, conjuntos, numbers, reglas):
        self.transitions = transitions
        self.conjuntos = conjuntos
        self.reglas = reglas
        
        self.state = numbers
        self.first = []
        self.action_filas = []
        self.action = []
        self.goto_filas = []
        self.goto = []
                
    def constructTable(self):
        #primero divirlos por sus secciones correspondietes
        for x in self.transitions:
            if x[1].isupper():
                if x[1] not in self.goto_filas:
                    self.goto_filas.append(x[1])
            else:
                if x[1] not in self.action_filas:
                    self.action_filas.append(x[1])
        self.action_filas.sort(reverse=True)
        print("self.state: ", self.state)
        print("self.action: ",self.action_filas)
        print("self.goto: ",self.goto_filas)
        for x in range(len(self.conjuntos)):
            print(f"{x}:{self.conjuntos[x]}")
        print("====================")
        for x in range(len(self.reglas)):
            print(f"{x}:{self.reglas[x]}")
        ignorar = self.reglas[0][1][0]
        print("====================")
        # print("ignorar: ",ignorar)
        #primero llenar el goto
        for x in self.state:    
            for y in self.goto_filas:
                for z in self.transitions:
                    if z[0] == x and z[1] == y:
                        self.goto.append([x,y,z[2]])
                        # input()
                        # print("self.goto: ", self.goto)
        #comenzar la armada de action pero los shift
        for x in self.state:
            for y in self.action_filas:
                for z in self.transitions:
                    if z[0] == x and z[1] == y:
                        if y == "$":
                            self.action.append([x,y,"acc"])
                        else:
                            self.action.append([x,y,"s"+str(z[2])])
                            
        #obtener los primeros o FIRST
        for x in self.reglas:
            largo = 0
            visitados = []
            inicial = x[0]
            visitados.append(inicial)
            while(largo != len(visitados)):
                largo = len(visitados)
                for y in visitados:
                    for z in self.reglas:
                        if y == z[0]:
                            if z[1][0] not in visitados:
                                visitados.append(z[1][0])
            #agarrar los terminales
            agregar = []
            for y in visitados:
                if y in self.action_filas:
                    agregar.append(y)
            if [inicial,agregar] not in self.first:
                self.first.append([inicial,agregar])
                
        print("self.first: ",self.first)
        print("====================")
                            
        #armar la action pero con el de follow o replace
        for x in range(len(self.conjuntos)): #ubicacion, seria el primer parametro para el [x, ... ,...]
            for y in self.conjuntos[x]:
                if y[1][len(y[1])-1] == ".":
                    indice = y[1].index(".")
                    if y[1][indice-1] != ignorar:
                        trans_copy = copy.deepcopy(y)
                        trans_copy[1].remove(".")
                        for z in range(len(self.reglas)): #donde poner, seria el ultimo del parametro para el [x, ..., z]
                            if self.reglas[z] == trans_copy:
                                print(trans_copy)
                                print(self.conjuntos[x])
                                print()
                    
        print("self.goto: ", self.goto)
        print("self.action: ",self.action)