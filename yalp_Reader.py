from yalReaderV2 import *

class YalpReader:
    def __init__(self, simulation, file):
        self.simulation = simulation
        self.tokenCopy = []
        self.tokens = []
        self.productions = []
        self.conjuntos = []
        self.ciclo = []
        self.transiciones = []
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
        reglas = False
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
        
        print("self.tokenCopy: ", self.tokenCopy)
        print("tokens: ", self.tokens)
        print("self.productions: ",self.productions)
        
    def subsetConstruction(self):
        #crear el inicial
        value = self.productions[0][0]
        self.productions.insert(0, [value+"'", [value]]) 
        
        #agregar . para todos en el inicio para el trabajo
        for x in self.productions:
            x[1].insert(0,".")
        
        #initial construct
        print("self.productions: ",self.productions)
        self.clousure([self.productions[0]])
        #seguir mientras hayan datos
        while len(self.ciclo) > 0:
            print("self.ciclo: ",self.ciclo)
            self.goto(self.ciclo.pop(0))          
        
    def clousure(self, item):
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
        print("closure_Array: ",sorted_items)
        if sorted_items not in self.conjuntos:
            self.conjuntos.append(sorted_items)
            self.ciclo.append(sorted_items)
            
        # print("self.conjuntos: ", self.conjuntos)
        
    def goto(self,sorted_items):
        #obtener los token o elementos con el cual probar
        print("sorted_items: ",sorted_items)
        elements = []
        for x in sorted_items:
            indice = x[1].index(".")
            if indice + 1 <= len(x[1]):
                if x[1][indice+1] not in elements: 
                    elements.append(x[1][indice+1])
        print("elements: ", elements)
        
        #encontrar todos los que son .elements y apartir de esos mover el . una casilla 
        for x in elements:
            print("x: ", x)
            temporal = []
            for y in sorted_items:
                indice = y[1].index(".")
                if indice + 1 < len(y[1]):
                    # print("y[1]: ", y[1])
                    if y[1][indice+1] == x: 
                        temporal.append(y)
            print("temporal antes de mover el .: ", temporal)
            #mover el . una casilla a la derech
            for z in temporal:
                indice = z[1].index(".")
                if indice + 1 < len(z[1]):
                    a = z[1][indice]
                    b = z[1][indice+1]
                    z[1][indice] = b
                    z[1][indice+1]=a
            print("temporal: ",temporal)
            #envairlo al closure
            self.clousure(temporal)
            break
            
        
                    