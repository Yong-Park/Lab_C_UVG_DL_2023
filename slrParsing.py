import copy
import pandas as pd
from tabulate import tabulate

class SLRPARSING:
    def __init__(self, transitions, conjuntos, numbers, reglas):
        self.transitions = transitions
        self.conjuntos = conjuntos
        self.reglas = reglas
        # print("self.reglas: ",self.reglas)
        self.Noterminales = []
        
        self.state = numbers
        self.first = []
        self.action_filas = []
        self.action = []
        self.goto_filas = []
        self.goto = []
        
        for x in self.reglas:
            if x[0] not in self.Noterminales:
                self.Noterminales.append(x[0])
                
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
        # print("self.state: ", self.state)
        # print("self.action_filas: ",self.action_filas)
        # print("self.goto_filas: ",self.goto_filas)
        # for x in range(len(self.conjuntos)):
        #     print(f"{x}:{self.conjuntos[x]}")
        # print("====================")
        # for x in range(len(self.reglas)):
        #     print(f"{x}:{self.reglas[x]}")
        first = self.reglas[0][1][0]
        # print("====================")
        # print("first: ",first)
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
            # print("visitados: ",visitados)
            #agarrar los terminales
            agregar = []
            for y in visitados:
                if y in self.action_filas:
                    agregar.append(y)
            if [inicial,agregar] not in self.first:
                self.first.append([inicial,agregar])
        #     print("====================")
        # print("self.first: ",self.first)
        # print("====================")
        # print("self.reglas: ", self.reglas)
        # print("self.conjuntos: ",self.conjuntos)
        
        #armar la action pero con el de follow/replace
        for x in range(len(self.conjuntos)): #ubicacion, seria el primer parametro para el [x, ... ,...]
            for y in self.conjuntos[x]:
                if y[1][len(y[1])-1] == ".":
                    # print("y: ",y)
                    indice = y[1].index(".")
                    if y[1][indice-1] != first:
                        trans_copy = copy.deepcopy(y)
                        trans_copy[1].remove(".")
                        for z in range(len(self.reglas)): #donde poner, seria el ultimo del parametro para el [x, ..., z]
                            if self.reglas[z] == trans_copy:
                                # print(self.conjuntos[x], x) # numero del state
                                # print("\n",trans_copy) # replace z seria este
                                transaction = self.follow(trans_copy[0], first) #transaction sera el parametro [x,w,z]
                                # print("trans_copy[0]: ",trans_copy[0])
                                # print("transaction: ",transaction)
                                # print("_______________________________________________")
                                for w in transaction:
                                    self.action.append([x,w,"r"+str(z)])
                                # print()
                                #enviar y obtener el follow del parametro
        print("self.first: ", self.first)                     
        print("self.goto: ", self.goto)
        print("self.action: ",self.action)
        
    def follow(self, state, accept_state):
        accept_state += "'"
        # print("self.Noterminales ", self.Noterminales)
        # print("state: ",state)
        # print("accept_state: ",accept_state)
        # print("self.reglas: ",self.reglas)
        revisar = []
        revisar.append(state)
        largo = 0
        transactions = []
        #primero encontrar en si este forma parte de alguno otro
        while (largo != len(revisar)):
            largo = len(revisar)
            for y in revisar:
                for x in self.reglas:
                    if y in x[1]:
                        indiceNoterminal = x[1].index(y)
                        # print("indiceNoterminal: ",indiceNoterminal)
                        # print("x: ", x)
                        #revisar si es terminal
                        if indiceNoterminal == len(x[1])-1:
                            # print("============")
                            # print(indiceNoterminal)
                            # print(len(x[1])-1)
                            if x[0] not in revisar:
                                revisar.append(x[0]) 
                            
                        #revisar si no es terminal y la siguiente de el es no terminal tambien
                        else:
                            #agregar el first del siguiente
                            if indiceNoterminal + 1 < len(x[1]):
                                if x[1][indiceNoterminal+1] in self.Noterminales:
                                    for z in self.first:
                                        if z[0] == x[1][indiceNoterminal+1]:
                                            for w in z[1]:
                                                if w not in transactions:
                                                    transactions.append(w)
                        
                        # if x[1][0] in revisar and x[0] not in revisar:
                        #     revisar.append(x[0])
                #         print("transactions: ",transactions)
                #         print("revisar: ", revisar)
                # input()
        # print("aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa")
        #obtener todos sus follow
        # print("revisar: ",revisar)
        # print("self.reglas: ",self.reglas)
        for x in revisar:
            for y in self.reglas:
                if x in y[1]:
                    indice = y[1].index(x)
                    if indice + 1 < len(y[1]) and y[1][indice+1] not in self.Noterminales:
                        if y[1][indice+1] not in transactions:
                            transactions.append(y[1][indice+1])
        #revisar si tiene el estado de aceptacion y en este caso agregar el $
        if accept_state in revisar:
            transactions.append("$")
        
        # print("transactions: ", transactions)
        return transactions
    
    def draw_table(self):
        # Create an empty DataFrame with the specified columns
        columns = self.action_filas + self.goto_filas
        df = pd.DataFrame(columns=columns)

        # Fill the table with data from 'goto' and 'action'
        for row, col, value in self.goto + self.action:
            df.at[row, col] = value

        # Fill NaN values with empty strings
        df.fillna('', inplace=True)

        # Set the index column name
        df.index.name = 'state'

        # Add custom headers
        headers = ['ACTION'] * len(self.action_filas) + ['GOTO'] * len(self.goto_filas)
        df.columns = pd.MultiIndex.from_tuples(zip(headers, df.columns))
        
        # Sort it by state
        df.sort_index(inplace=True)

        # Convert the DataFrame to a table using the 'tabulate' library
        table = tabulate(df, headers='keys', tablefmt='fancy_grid', showindex=True)

        # Display the table in the console
        print(table)

    # realizar simulacion
    def simulate(self, test_token):
        stack_register = []
        symbol_register = []
        inputs_register = []
        #elementos
        stack = []
        symbol = []
        inputs = []
        action = []
        
        #guardar em un array el input
        for x in test_token:
            inputs.append(x[0])
        inputs.append("$")
        # print("input: ",input)
        # print("self.action_filas: ",self.action_filas)
        # print("self.action: ", self.action)
        # print("self.goto_filas: ",self.goto_filas)
        # print("self.goto: ", self.goto)
        # print("self.Noterminales: ",self.Noterminales)
        # print("self.reglas: ",self.reglas)
        symbol.append("$")
        #comenzar la simulacion
        #agregar el primer valor que seria el 0 al stack
        stack.append(0)
        verdad = True
        completado = False
        while(verdad):
            stack_value = stack[len(stack)-1]
            input_value = inputs[0]
            
            #guardar el registro
            stack_register.append(copy.deepcopy(stack))
            symbol_register.append(copy.deepcopy(symbol))
            inputs_register.append(copy.deepcopy(inputs))
            
            # print("stack_value: ",stack_value)
            # print("input_value: ",input_value)
            for x in self.action:
                if stack_value == x[0] and input_value == x[1]:
                    # print("existe")
                    verdad = True
                    # print("x[2]: ",x[2])
                    # print("len(x[2]): ",len(x[2]))
                    #revisar si es shift o replace
                    if x[2][0] == "s":
                        stack.append(int(x[2][1:]))
                        symbol.append(inputs.pop(0))
                        action.append(f"shift to {x[2][1:]}")
                    elif x[2][0] == "r":
                        index = int(x[2][1:])
                        cambio = self.reglas[index]
                        action.append(f"reduced by {cambio[0]} -> {' '.join(cambio[1])}")
                        stacks_elimnar = len(cambio[1])
                        for _ in range(stacks_elimnar):
                            stack.pop(len(stack)-1)
                        temporal_symbol = cambio[1]
                        indices_remplazar = []
                        for y in cambio[1]:
                            for z in range(len(symbol)):
                                if y == symbol[z]:
                                    indices_remplazar.append(z)
                        
                        if len(indices_remplazar) > 1:
                            symbol[indices_remplazar[0]:indices_remplazar[len(indices_remplazar)-1]+1] = cambio[0]
                        else:
                            symbol[indices_remplazar[0]] = cambio[0]
                            
                        stack_value = stack[len(stack)-1]
                        # print("stack_value: ",stack_value)
                        # print("cambio[0]: ",cambio[0])
                        for w in self.goto:
                            # print("w: ",w)
                            if w[0] == stack_value and w[1] == cambio[0]:
                                # print("si existe y es: ", w[2])
                                stack.append(int(w[2]))
                    elif x[2] == "acc":
                        action.append("accept")
                        completado = True
                        verdad = False
                    break
                else:
                    verdad = False
 
            # input()
            # print("======================")
            # print(f"stack: {stack}")
            # print(f"symbol: {symbol}")
            # print(f"inputs: {inputs}")
            # print(f"action: {action}")
            # print("======================")
            
        if completado == True:
            print("Accepted")
        else:
            print("Not accepted")
                        
        data = {'Stack': stack_register, 'Symbol': symbol_register, 'Inputs': inputs_register, 'Action': action}
        df = pd.DataFrame(data)
        df.index.name = 'Line'

        # Convert the DataFrame to a table using the 'tabulate' library
        table = tabulate(df, headers='keys', tablefmt='fancy_grid', showindex=True)

        # Display the table in the console
        print(table)


        # print(f"stack: {stack_register}")
        # print(f"symbol: {symbol_register}")
        # print(f"inputs: {inputs_register}")
        # print(f"action: {action}")
                        