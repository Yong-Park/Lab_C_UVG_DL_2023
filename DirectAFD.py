import string
import graphviz
import os
os.environ["PATH"] += os.pathsep + 'D:/Program Files (x86)/Graphviz2.38/bin/'

class DirectAfd:
    def __init__(self,postfix):
        self.postfix = postfix
        # print("self.postfix: ",self.postfix)
        #agregar el # de ultimo para la cadena
        self.postfix.append('#')
        self.postfix.append('•')
        # Nueva lista vacía que se utiliza para ordenar correspondientemente cuando se obtienen los valores
        self.nueva_lista = []

        self.deletable_firstPos = []
        self.deletable_lastPos = []
        self.deletable_nullable = []

        self.newPostfix = []
        self.nullable= []
        self.firstPos= []
        self.lastPos = []
        self.followPos = [] 
        self.q = []
        self.enumerate()
        self.startConstruct()
        self.follopostConstruct()
    
    #en este se enumeraran los estados correspondientes
    def enumerate(self):
        #generar un listado de numeros de 1 - 1000
        for i in range(1,1000):
            value = i
            self.q.append(value)
        
        #si los valores son distintos a *|.?+ darles un valor numerico
        for x in self.postfix:
            if x not in '*|•?+ε':
                self.newPostfix.append(self.q.pop(0))
            else:
                self.newPostfix.append(x)
        # print("old postfix: ",self.postfix)
        # print("nuevo postfix: ",self.newPostfix)

    #se comenzara a armar lo necesario para obtner los conjuntos y asi en los que eston van a viajar
    def startConstruct(self):
        # print(self.postfix)
        for node in self.newPostfix:
            # print("node: ", node)
            if str(node) in '*|•?+ε':
                if node == '*':
                    self.nullable.append(True)
                    self.firstPos.append(self.deletable_firstPos[len(self.deletable_firstPos)-1])
                    self.lastPos.append(self.deletable_lastPos[len(self.deletable_lastPos)-1])

                    self.deletable_nullable.append(True)
                    self.deletable_firstPos.append(self.deletable_firstPos[len(self.deletable_firstPos)-1])
                    self.deletable_lastPos.append(self.deletable_lastPos[len(self.deletable_lastPos)-1])

                    #eliminar uno de cada uno
                    self.deletable_nullable.pop(len(self.deletable_nullable)-2)
                    self.deletable_firstPos.pop(len(self.deletable_firstPos)-2)
                    self.deletable_lastPos.pop(len(self.deletable_lastPos)-2)

                elif node == '|':
                    #revisar si es nullable
                    c1 = self.deletable_nullable[len(self.deletable_nullable)-2]
                    c2 = self.deletable_nullable[len(self.deletable_nullable)-1]
                    if c1 == True or c2 == True:
                        self.nullable.append(True)
                        self.deletable_nullable.append(True)
                    else:
                        self.nullable.append(False)
                        self.deletable_nullable.append(False)
                    #eliminar las dos primeras del nullable 
                    self.deletable_nullable.pop(len(self.deletable_nullable)-2)
                    self.deletable_nullable.pop(len(self.deletable_nullable)-2)

                    #agregar el firstpos
                    first = []
                    first.extend(self.deletable_firstPos[len(self.deletable_firstPos)-2])
                    first.extend(self.deletable_firstPos[len(self.deletable_firstPos)-1])
                    first.sort()
                    self.firstPos.append(first)
                    self.deletable_firstPos.append(first)
                    #eliminar las dos primeras firstpos
                    self.deletable_firstPos.pop(len(self.deletable_firstPos)-2)
                    self.deletable_firstPos.pop(len(self.deletable_firstPos)-2)

                    #agregar el lastpos
                    last = []
                    last.extend(self.deletable_lastPos[len(self.deletable_lastPos)-2])
                    last.extend(self.deletable_lastPos[len(self.deletable_lastPos)-1])
                    last.sort()
                    self.lastPos.append(last)
                    self.deletable_lastPos.append(last)
                    #eliminar las primeras dos lastpos
                    self.deletable_lastPos.pop(len(self.deletable_lastPos)-2)
                    self.deletable_lastPos.pop(len(self.deletable_lastPos)-2)
                elif node == '•':
                    #revisar si es nullable
                    c1 = self.deletable_nullable[len(self.deletable_nullable)-2]
                    c2 = self.deletable_nullable[len(self.deletable_nullable)-1]
                    if c1 == True and c2 == True:
                        self.nullable.append(True)
                        self.deletable_nullable.append(True)
                    else:
                        self.nullable.append(False)
                        self.deletable_nullable.append(False)
                    #eliminar los dos c1 y c2
                    self.deletable_nullable.pop(len(self.deletable_nullable)-2)
                    self.deletable_nullable.pop(len(self.deletable_nullable)-2)
                    
                    #agregar el firstpos
                    if c1 == True:
                        first = []
                        first.extend(self.deletable_firstPos[len(self.deletable_firstPos)-2])
                        first.extend(self.deletable_firstPos[len(self.deletable_firstPos)-1])
                        first.sort()
                        self.firstPos.append(first)
                        self.deletable_firstPos.append(first)
                        #eliminar las dos primeras first
                        self.deletable_firstPos.pop(len(self.deletable_firstPos)-2)
                        self.deletable_firstPos.pop(len(self.deletable_firstPos)-2)
                    else:
                        first = []
                        first.extend(self.deletable_firstPos[len(self.deletable_firstPos)-2])
                        self.firstPos.append(first)
                        self.deletable_firstPos.append(first)
                        #eliminar las dos primeras first
                        self.deletable_firstPos.pop(len(self.deletable_firstPos)-2)
                        self.deletable_firstPos.pop(len(self.deletable_firstPos)-2)
                    #agregar el lastpos
                    if c2 == True:
                        last = []
                        last.extend(self.deletable_lastPos[len(self.deletable_lastPos)-2])
                        last.extend(self.deletable_lastPos[len(self.deletable_lastPos)-1])
                        last.sort()
                        self.lastPos.append(last)
                        self.deletable_lastPos.append(last)
                        #eliminar las dos primeras last
                        self.deletable_lastPos.pop(len(self.deletable_lastPos)-2)
                        self.deletable_lastPos.pop(len(self.deletable_lastPos)-2)
                    else:
                        last = []
                        last.extend(self.deletable_lastPos[len(self.deletable_lastPos)-1])
                        self.lastPos.append(last)
                        self.deletable_lastPos.append(last)
                        #eliminar las dos primeras last
                        self.deletable_lastPos.pop(len(self.deletable_lastPos)-2)
                        self.deletable_lastPos.pop(len(self.deletable_lastPos)-2)
                elif node == '?':
                    self.nullable.append(True)
                    self.firstPos.append(self.deletable_firstPos[len(self.deletable_firstPos)-1])
                    self.lastPos.append(self.deletable_lastPos[len(self.deletable_lastPos)-1])

                    self.deletable_nullable.append(True)
                    self.deletable_firstPos.append(self.deletable_firstPos[len(self.deletable_firstPos)-1])
                    self.deletable_lastPos.append(self.deletable_lastPos[len(self.deletable_lastPos)-1])

                    #eliminar cada uno
                    self.deletable_nullable.pop(len(self.deletable_nullable)-2)
                    self.deletable_firstPos.pop(len(self.deletable_firstPos)-2)
                    self.deletable_lastPos.pop(len(self.deletable_lastPos)-2)
                elif node == '+':
                    #revisar si es nullabel
                    c1 = self.deletable_nullable[len(self.deletable_nullable)-1]
                    # print(c1)
                    if c1 == True:
                        self.nullable.append(True)
                        self.deletable_nullable.append(True)
                    else:
                        self.nullable.append(False)
                        self.deletable_nullable.append(False)
                    #eliminar el del nullabel
                    self.deletable_nullable.pop(len(self.deletable_nullable)-2)

                    #insertar el firstpos y lastpos
                    self.firstPos.append(self.deletable_firstPos[len(self.deletable_firstPos)-1])
                    self.lastPos.append(self.deletable_lastPos[len(self.deletable_lastPos)-1])

                    self.deletable_firstPos.append(self.deletable_firstPos[len(self.deletable_firstPos)-1])
                    self.deletable_lastPos.append(self.deletable_lastPos[len(self.deletable_lastPos)-1])

                    #eliminar uno de fist y las
                    self.deletable_firstPos.pop(len(self.deletable_firstPos)-2)
                    self.deletable_lastPos.pop(len(self.deletable_lastPos)-2)

                elif node == 'ε':
                    self.nullable.append(True)
                    self.firstPos.append([])
                    self.lastPos.append([])

                    self.deletable_nullable.append(True)
                    self.deletable_firstPos.append([])
                    self.deletable_lastPos.append([])
            else:
                self.nullable.append(False)
                self.firstPos.append([node])
                self.lastPos.append([node])

                self.deletable_nullable.append(False)
                self.deletable_firstPos.append([node])
                self.deletable_lastPos.append([node])

        #     print("nullable deletable: ",self.deletable_nullable)
        #     print("fistpos deletable: ",self.deletable_firstPos)
        #     print("lastpost deletable: ",self.deletable_lastPos)
        #     print("_____________________")

        # print("_________________Final_________________")
        # print("node: ", self.newPostfix)
        # print("nullable: ", self.nullable)
        # print("firstpos: ", self.firstPos)
        # print("lastpos: ", self.lastPos)
        
    def follopostConstruct(self):
        # print("_________________Followpost construct________")
        #limpiar los deletable
        self.deletable_firstPos = []
        self.deletable_lastPos = []
        # print("self.newPostfix: ", self.newPostfix)
        # print("self.postfix: ", self.postfix)

        #guardar todos los valores para el followpost
        for val in range(len(self.newPostfix)):
            if str(self.newPostfix[val]) not in "*?•+|":
                self.followPos.append([self.newPostfix[val]])
        
        for val in range(len(self.newPostfix)):
            # print(self.newPostfix[val])     
            isnodes = []
            addnodes = []
            
            if self.newPostfix[val] == "*":
                isnodes.extend(self.deletable_lastPos[len(self.deletable_lastPos)-1])
                addnodes.extend(self.deletable_firstPos[len(self.deletable_firstPos)-1])
                # print("isnodes: ",isnodes )
                # print("addnodes: ",addnodes )
                
                for nod in range(len(self.followPos)):
                    if self.followPos[nod][0] in isnodes:
                        if len(self.followPos[nod]) > 1:
                            for x in addnodes:
                                if x not in self.followPos[nod][1]:
                                    self.followPos[nod][1].append(x)
                            self.followPos[nod][1].sort()
                        else:
                            self.followPos[nod].append(addnodes)

                self.deletable_firstPos.append(self.firstPos[val])
                self.deletable_lastPos.append(self.lastPos[val])

                self.deletable_lastPos.pop(len(self.deletable_lastPos)-2)
                self.deletable_firstPos.pop(len(self.deletable_firstPos)-2)
                            
            elif self.newPostfix[val] == "+":
                isnodes.extend(self.deletable_lastPos[len(self.deletable_lastPos)-1])
                addnodes.extend(self.deletable_firstPos[len(self.deletable_firstPos)-1])
                # print("isnodes: ",isnodes )
                # print("addnodes: ",addnodes )
                
                for nod in range(len(self.followPos)):
                    if self.followPos[nod][0] in isnodes:
                        if len(self.followPos[nod]) > 1:
                            for x in addnodes:
                                if x not in self.followPos[nod][1]:
                                    self.followPos[nod][1].append(x)
                            self.followPos[nod][1].sort()
                        else:
                            self.followPos[nod].append(addnodes)
                            
                self.deletable_firstPos.append(self.firstPos[val])
                self.deletable_lastPos.append(self.lastPos[val])

                self.deletable_lastPos.pop(len(self.deletable_lastPos)-2)
                self.deletable_firstPos.pop(len(self.deletable_firstPos)-2)
            
            elif self.newPostfix[val] == "•":
                c1 = self.deletable_lastPos[len(self.deletable_lastPos)-2]
                c2 = self.deletable_firstPos[len(self.deletable_firstPos)-1]
                isnodes.extend(c1)
                addnodes.extend(c2)
                # print("isnodes: ",isnodes )
                # print("addnodes: ",addnodes )
                
                for nod in range(len(self.followPos)):
                    if self.followPos[nod][0] in isnodes:
                        if len(self.followPos[nod]) > 1:
                            for x in addnodes:
                                if x not in self.followPos[nod][1]:
                                    self.followPos[nod][1].append(x)
                            self.followPos[nod][1].sort()
                        else:
                            self.followPos[nod].append(addnodes)

                self.deletable_firstPos.append(self.firstPos[val])
                self.deletable_lastPos.append(self.lastPos[val])

                self.deletable_firstPos.pop(len(self.deletable_firstPos)-2)
                self.deletable_firstPos.pop(len(self.deletable_firstPos)-2)

                self.deletable_lastPos.pop(len(self.deletable_lastPos)-2)
                self.deletable_lastPos.pop(len(self.deletable_lastPos)-2)


            elif self.newPostfix[val] == '|':
                
                self.deletable_firstPos.append(self.firstPos[val])
                self.deletable_lastPos.append(self.lastPos[val])

                self.deletable_firstPos.pop(len(self.deletable_firstPos)-2)
                self.deletable_firstPos.pop(len(self.deletable_firstPos)-2)

                self.deletable_lastPos.pop(len(self.deletable_lastPos)-2)
                self.deletable_lastPos.pop(len(self.deletable_lastPos)-2)
                
            elif self.newPostfix[val] == '?':
                
                self.deletable_firstPos.append(self.firstPos[val])
                self.deletable_lastPos.append(self.lastPos[val])

                self.deletable_firstPos.pop(len(self.deletable_firstPos)-2)

                self.deletable_lastPos.pop(len(self.deletable_lastPos)-2)
            elif "#" in str(self.newPostfix[val]):
                print(self.newPostfix[val])
            else:
                self.deletable_firstPos.append(self.firstPos[val])
                self.deletable_lastPos.append(self.lastPos[val])

            # print("follopos: ", self.followPos)
            # print("fistpos deletable: ",self.deletable_firstPos)
            # print("lastpost deletable: ",self.deletable_lastPos)
            
        #agregar el ultimo un signo ∅ ya que es el #              
        self.followPos[len(self.followPos)-1].append(["∅"])
         
        #revisar de cada uno de los followpos construidos y revisar si entre ellos tiene #
        # print("self.followPos: ",self.followPos )
        # print("self.newPostfix: ", self.newPostfix)
        for lar in range(len(self.followPos)):
            for value in range(len(self.newPostfix)):
                if self.followPos[lar][0] == self.newPostfix[value]:
                    if "#" in self.postfix[value]:
                        self.followPos[lar][1] = ["∅"]
                        # print("self.followPos: ",self.followPos[lar][1] )
                        # print(self.postfix[value])
                        # print(self.newPostfix[value])
                        # print("=========")
        
        # print("___________")
        # print("followpos: ",self.followPos)
        
    def Dstate(self):
        # print("==========Dstates===============")
        # #nodo inicial
        # print("self.postfix: ", self.postfix)
        # print("self.newPostfix: ",self.newPostfix)
        # print("self.followPos: ", self.followPos)
       
        # print("self.firstPos: ", self.firstPos[len(self.firstPos)-1])
        # print("self.lastPos: ",self.lastPos)
        sNode = self.firstPos[len(self.firstPos)-1]
        # print("snode: ", sNode)
        # print("followpos: ", self.followPos)
        
        #nodo final
        final = []
        for x in self.followPos:
            if "∅" in x[1]:
                final.append(x[0])
        # print("final: ", final)
        #aqui tendra todos los nodos de los cuales viajara
        P0 = []
        P0.append(sNode)
        #obtener las variables que utiliza
        self.variables = []
        for x in self.postfix:
            if x not in "|•*+?":
                if "#" not in x:
                    if x not in self.variables:
                        # if type(x) == int:
                        #     print("x: ",x)
                        self.variables.append(x)
        # print("variables: ", self.variables)
        
        tabla = []
        for x in P0:                #[1,2,3]
            # print("x: ", x)
            conjuntos = []
            conjuntos.append(x)
            for alfa in self.variables:  #a, b
                movement = []
                movement.append(alfa)
                con = []
                for y in x:         #1,2,3
                    # print("y: ", y)
                    for l in range(len(self.postfix)):
                        if self.newPostfix[l] == y and self.postfix[l] == alfa:
                            # print("aceptado: ",self.newPostfix[l])
                            for w in self.followPos:
                                if w[0] == y:
                                    for z in w[1]:
                                        if z not in con:
                                            con.append(z)
                con.sort()
                # print("con: ",con)
                if con not in P0 and len(con) != 0:
                    P0.append(con)
                if len(con) != 0:
                    movement.append(con)
                    conjuntos.append(movement)
                # print("movement: ",movement)
                # print("conjuntos: ", conjuntos)
                if conjuntos not in tabla:
                    tabla.append(conjuntos)
        #     print("________")
        # print("tabla: ", tabla)
        # convertilos en el parametro correcto
        for sub_array in tabla:
            if len(sub_array) > 1:
                for i in range(1,len(sub_array)):
                    # print(sub_array)
                    # print(len(sub_array))
                    
                    # print(sub_array[i][0])
                    new_element = [sub_array[0], sub_array[i][0], sub_array[i][1]]
                    self.nueva_lista.append(new_element)
            else:
                self.nueva_lista.append(sub_array)

        # Impresión de la nueva lista
        # print("nueva lista: ", self.nueva_lista)
        
        #convertir la nueva lista en A,B,C ...
        q = list(string.ascii_uppercase)
        #obtener todos los nodos
        node = []
        alfanode = []
        for x in self.nueva_lista:
            if x[0] not in node:
                node.append(x[0])
                alfanode.append(q.pop(0))
        # print("node: ",node)
        # print("alfanode: ",alfanode)
        
        #comenzar a reemplazarlo por alfabetos
        # print("nueva lista: ", self.nueva_lista)
        for x in self.nueva_lista:
            # print("x: ", x)
            if len(x) > 1:
                for y in range(len(node)):
                    # print(node[y])
                    # print(len(node[y]))
                    if x[0] == node[y]:
                        x[0] = alfanode[y]
                    if x[2] == node[y]:
                        x[2] = alfanode[y]
            else:
                for y in range(len(node)):
                    # print(node[y])
                    # print(len(node[y]))
                    if x[0] == node[y]:
                        x[0] = "vacio"
        
        self.nueva_lista = [sublista for sublista in self.nueva_lista if 'vacio' not in sublista]
        
    
        # print("nueva lista actualizada: ", self.nueva_lista)
        
        start = []
        end = []
        endHash = []
        #obtener los nuevos iniciales y finales
        
        # print("node: ", node)
        for ele in range(len(node)):
            if node[ele] == sNode:
                start.extend(alfanode[ele])
            for f in final:
                if f in node[ele]:
                    end.extend(alfanode[ele])
                    for val in range(len(self.newPostfix)):
                        if f == self.newPostfix[val]:
                            endHash.append(self.postfix[val])
        # print("final: ", final)
        #en caso que solo es un nodo
        if len(node) == 1:
            end.extend(alfanode[0])
        #se guardan los nuevos iniciales y finales correspondientes
        # print(start)
        # print(endHash)
        # print(end)
        
        sfPoint=[]
        # print("start: ",start)
        # print("end: ", end)
        sfPoint.append(start)
        sfPoint.append(end)  
        sfPoint.append(endHash)
            
        
        return [self.nueva_lista,sfPoint]
    
    def DirectGraph(self,directAFD,sfPoint):
        # print(sfPoint)
        inicio = sfPoint[0]
        final = sfPoint[1]
        q_list = []
        q = list(string.ascii_uppercase)
        # print("directAFD: ",directAFD)

        #guardar los valores de q utilizados
        for l in directAFD:
            for q_search in q:
                if q_search == l[0]:
                    if q_search not in q_list:
                        q_list.append(q_search)
                if q_search == l[2]:
                    if q_search not in q_list:
                        q_list.append(q_search)

        f = graphviz.Digraph(comment = "afd Directo")
        inicio_listo = True
        # print("final: ", final)
        
        for name in q_list:
            # print(name)
            if name in final:
                f.node(str(name), shape="doublecircle",fillcolor="#ee3b3b",style="filled")
            elif name in inicio:
                f.node(str(name),fillcolor="#7fff00",style="filled")
            else:
                f.node(str(name))
        f.node("", shape="plaintext")
        for l in directAFD:
            # print("l: ",l)
            for val in inicio:
                if val in l and l[0] == val:
                    if(inicio_listo):
                        # print(val)
                        # print(l[0])
                        f.edge("",str(l[0]),label = "")
                        inicio_listo = False
            if len(l) > 1:
                if type(l[1]) == int:
                    print("l[1]: ",l[1])
                    l[1] = chr(l[1])
                f.edge(str(l[0]),str(l[2]),label = str(l[1]))
            else:
                # print("l[0]: ", l[0])
                f.node(str(l[0]))
        f.render("afd Directo", view = True)
        
                
                
                