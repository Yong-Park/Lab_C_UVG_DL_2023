from yalReaderV2 import *

class YalpReader:
    def __init__(self, simulation, file):
        self.simulation = simulation
        self.tokenCopy = []
        self.tokens = []
        self.productions = []
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
        self.productions.insert(0, [value, [value+"'"]]) 
        print("self.productions: ",self.productions)
        