from yalReaderV2 import *
import copy

class YalpReader:
    def __init__(self, simulation, file):
        self.number = 0
        self.simulation = simulation
        self.tokenCopy = []
        self.tokens = []
        self.productions = [] #en este se guardara la producion principal para que se pueda utlizar en el closure
        self.conjuntos = [] #en este se guardaran todos los posible conjuntos que se pueden llegar a armar
        self.conjuntos_number = [] # en este se guardaran el numero que pertenecen cada conjunto
        self.ciclo = [] #tendra lo de conjuntos pero sirve para utilizarlo en el ciclo para encontrar nuevos y sus transiciones respectivas
        self.transiciones = [] #en este tendra la transicion correspondiente de cada conjunto
        # nombre del archivo que se abrira
        reader = YalReader(file)
        _,token_functions = reader.analize()

        for sublist in token_functions:
            if 'return' in sublist[1]:
                sublist[1] = sublist[1].replace('return ', '')
        self.tokenFunctions = token_functions
        # print("token_functions: ", token_functions)
        
    #en produciones los que son minusculos son los no terminales y mayusculas los terminales
    def startConstruct(self):
        divided = False
        comment = False
        token = False
        temporal = []
        expresion = True
        functionName = ""
        # print("simulation: ", self.simulation)
        for x in self.simulation:
            if x[0] == "/*":
                comment = True
            
            if not comment:
                if x[0] == "%%":
                    divided = True
                #lectura de las producciones
                if divided:
                    if expresion:
                        if x[0] == "minusword":
                            functionName = x[1][0].upper()
                            expresion = False
                    else:
                        if x[0] == "minusword":
                            temporal.append(x[1][0].upper())
                        if x[0] == "mayusword":
                            temporal.append(x[1])
                        if x[0] == "|":
                            self.productions.append([functionName,temporal])
                            temporal = []
                        if x[0] == ";":
                            if temporal:
                                self.productions.append([functionName,temporal])
                                temporal = []
                            expresion=True
                        
                    # print("producciones")
                    # print(x)
                
                #lectura de los tokens
                else:
                    if x[0] == "%token":
                        token = True
                    if x[0] == "IGNORE":
                        token = False
                        
                    if token:
                        if x[0] == "mayusword":
                            self.tokens.append(x[1])
                            self.tokenCopy.append(x[1])
                    else:
                        if x[0] == "mayusword":
                            self.tokens.remove(x[1])
                            self.tokenCopy.remove(x[1])

                    # print("tokens")
                    # print(x)
                        
            if x[0] == "*/":
                comment = False
                
        #cambiar los tokens con su respectiva figura
        for x in range(len(self.tokens)):
            for y in self.tokenFunctions:
                if self.tokens[x] == y[1]:
                    self.tokens[x] = y[0]
                    break
        #cambiar los productions sus tokens o estados finales por su respectiva figura
        for x in self.productions:
            for y in range(len(x[1])):
                for z in self.tokenCopy:
                    if x[1][y] == z:
                        indice = self.tokenCopy.index(z)
                        x[1][y] = self.tokens[indice]
        
        # print("self.tokenCopy: ", self.tokenCopy)
        # print("tokens: ", self.tokens)
        # print("self.productions: ",self.productions)
        
    def subsetConstruction(self):
        #crear el inicial
        value = self.productions[0][0]
        self.productions.insert(0, [value+"'", [value]]) 
        
        #agregar . para todos en el inicio para el trabajo
        for x in self.productions:
            x[1].insert(0,".")
        
        #initial construct
        
        self.clousure([self.productions[0]])
        #seguir mientras hayan datos
        while len(self.ciclo) > 0:
            self.goto(self.ciclo.pop(0))
            
        # print(len(self.transiciones))
        
        #una vez terminada agregar tambien la transicion de aceptaion
        initial_state = self.productions[0][0] #estado que debe de buscar para el accept
        for x in self.conjuntos:
            # print("x: ", x)
            for y in x:
                # print(y)
                accept_index = y[1].index(".")
                if accept_index - 1 >= 0:
                    if y[0] == initial_state and y[1][accept_index-1] == initial_state[:-1]:
                        final_index = self.conjuntos.index(x)
                        self.transiciones.append([self.conjuntos_number[final_index],"$","accept"])
                        # print(x)
        # for y in range(len(self.conjuntos)):
        #         print(f"{self.conjuntos_number[y]}: {self.conjuntos[y]}\n")
        # print("self.transiciones: ",self.transiciones)
        
    def clousure(self, item, elem = None, cicle= None):
        # print("item: ",item)
        closure_Array = []
        closure_Array.extend(item)
        # print("closure_Array: ",closure_Array)
        # print("self.productions: ",self.productions)
        #comenzar a buscar
        largo = 0
        while largo != len(closure_Array):
            largo = len(closure_Array)
            for x in closure_Array:
                # print(x)
                indice = x[1].index(".")
                # print(indice)
                # print(len(x[1])-1)
                if indice + 1 < len(x[1]):
                    indice += 1
                    val= x[1][indice]
                    #buscar todos aquellos que comienzen con el val
                    for y in self.productions:
                        if y[0] == val and y not in closure_Array:
                            closure_Array.append(y)
        # print("closure_Array: ",closure_Array)
        sorted_items = sorted(closure_Array, key=lambda x: x[0])
        # print("closure_Array: ",sorted_items)
        
        if sorted_items not in self.conjuntos:
            self.conjuntos.append(sorted_items)
            self.conjuntos_number.append(self.number)
            self.number += 1
            self.ciclo.append(sorted_items)
            
        #agregar transiciones si elem y ciclo no son vacios
        if elem != None and cicle != None:
            start_index = self.conjuntos.index(cicle)
            end_index = self.conjuntos.index(sorted_items)
            self.transiciones.append([self.conjuntos_number[start_index],elem,self.conjuntos_number[end_index]])
            
        # print("self.conjuntos: ", self.conjuntos)
        
    def goto(self,ciclo):
        #obtener los token o elementos con el cual probar
        # print("sorted_items: ",ciclo)
        elements = []
        for x in ciclo:
            indice = x[1].index(".")
            if indice + 1 < len(x[1]):
                if x[1][indice+1] not in elements: 
                    elements.append(x[1][indice+1])
        # print("elements: ", elements)
        #encontrar todos los que son .elements y apartir de esos mover el . una casilla 
        for x in elements:
            # print("x: ", x)
            temporal = []
            for y in ciclo:
                indice = y[1].index(".")
                if indice + 1 < len(y[1]):
                    # print("y[1]: ", y[1])
                    if y[1][indice+1] == x: 
                        temporal.append(copy.deepcopy(y))
            # print("self.conjuntos antes de mover el .:", self.conjuntos)
            # print("self.productions antes de mover el .: ",self.productions)
            # print("temporal antes de mover el .: ", temporal)
            # print()
            #mover el . una casilla a la derech
            for z in temporal:
                indice = z[1].index(".")
                if indice + 1 < len(z[1]):
                    a = z[1][indice]
                    b = z[1][indice+1]
                    z[1][indice] = b
                    z[1][indice+1]=a
            # print("self.conjuntos: ", self.conjuntos)
            # print("self.productions: ",self.productions)
            # print("temporal: ",temporal)
            #envairlo al closure
            self.clousure(temporal, x, ciclo)
            # input()
            
        
                    