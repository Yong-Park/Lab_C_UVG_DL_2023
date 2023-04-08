class Postfix:
    def __init__(self):
        self.stack =[]
        self.output = []

    def transform_postfix(self,c):
        # print(c)
        for l in c:
            # input()
            # print("====================")
            # print(l)
            # print("s: " + str(self.stack))
            # print("o: " + str(self.output))
            if str(l) in "|()*•+?":
                self.stack.append(l)
                # print("before stack: ", self.stack)
                proceso = True
                while(proceso):
                    element = self.stack[len(self.stack)-1]
                    if element == ")":
                        a = len(self.stack)-2
                        while(self.stack[a] != "("):
                            self.output.append(self.stack[a])
                            self.stack[a]=""
                            a = a-1
                        self.stack[a] = ""
                        self.stack[self.stack.index(")")] = ""
                        while "" in self.stack:
                            self.stack.remove("")
                        proceso = False
                        
                    elif element == "?":
                        if len(self.stack) > 1:
                            if self.stack[len(self.stack)-2] == "*":
                                self.output.append(self.stack[len(self.stack)-1])
                                self.stack.pop(len(self.stack)-1)
                            elif self.stack[len(self.stack)-2] == "+":
                                self.output.append(self.stack[len(self.stack)-1])
                                self.stack.pop(len(self.stack)-1)
                            elif self.stack[len(self.stack)-2] == "?":
                                self.output.append(self.stack[len(self.stack)-1])
                                self.stack.pop(len(self.stack)-1)
                            else:
                                proceso = False
                        else:
                            proceso = False
                            
                    elif element == "*":
                        if len(self.stack) > 1:
                            if self.stack[len(self.stack)-2] == "*":
                                self.output.append(self.stack[len(self.stack)-1])
                                self.stack.pop(len(self.stack)-1)
                            elif self.stack[len(self.stack)-2] == "+":
                                self.output.append(self.stack[len(self.stack)-1])
                                self.stack.pop(len(self.stack)-1)
                            elif self.stack[len(self.stack)-2] == "?":
                                self.output.append(self.stack[len(self.stack)-1])
                                self.stack.pop(len(self.stack)-1)
                            else:
                                proceso = False
                        else:
                            proceso = False
                                
                    elif element =="+":
                        if len(self.stack) > 1:
                            if self.stack[len(self.stack)-2] == "+":
                                self.output.append(self.stack[len(self.stack)-1])
                                self.stack.pop(len(self.stack)-1) 
                            elif self.stack[len(self.stack)-2] == "*":
                                self.output.append(self.stack[len(self.stack)-1])
                                self.stack.pop(len(self.stack)-1)
                            elif self.stack[len(self.stack)-2] == "?":
                                self.output.append(self.stack[len(self.stack)-1])
                                self.stack.pop(len(self.stack)-1)
                            else:
                                proceso = False
                        else:
                            proceso = False
                                
                    elif element == "•":
                        if len(self.stack) > 1:
                            if self.stack[len(self.stack)-2] == "*":
                                self.output.append(self.stack[len(self.stack)-2])
                                self.stack.pop(len(self.stack)-2)
                            elif self.stack[len(self.stack)-2] == "+":
                                self.output.append(self.stack[len(self.stack)-2])
                                self.stack.pop(len(self.stack)-2)
                            elif self.stack[len(self.stack)-2] == "?":
                                self.output.append(self.stack[len(self.stack)-2])
                                self.stack.pop(len(self.stack)-2)
                            elif self.stack[len(self.stack)-2] == "•":
                                self.output.append(self.stack[len(self.stack)-1])
                                self.stack.pop(len(self.stack)-1)
                            else:
                                proceso = False
                        else:
                            proceso = False
                                
                    elif element == "|":
                        if len(self.stack) > 1:
                            if self.stack[len(self.stack)-2] == "*":
                                self.output.append(self.stack[len(self.stack)-2])
                                self.stack.pop(len(self.stack)-2)
                            elif self.stack[len(self.stack)-2] == "+":
                                self.output.append(self.stack[len(self.stack)-2])
                                self.stack.pop(len(self.stack)-2)
                            elif self.stack[len(self.stack)-2] == "?":
                                self.output.append(self.stack[len(self.stack)-2])
                                self.stack.pop(len(self.stack)-2)
                            elif self.stack[len(self.stack)-2] == "•":
                                self.output.append(self.stack[len(self.stack)-2])
                                self.stack.pop(len(self.stack)-2)
                            elif self.stack[len(self.stack)-2] == "|":
                                self.output.append(self.stack[len(self.stack)-1])
                                self.stack.pop(len(self.stack)-1)
                            else:
                                proceso = False
                        else:
                            proceso = False
                    else:
                        proceso = False
            else:
                self.output.append(l)
            # print("stack: ", self.stack)
            # print("output: ", self.output)
            # print("__________")
        while(len(self.stack) > 0):
            self.output.append(self.stack[len(self.stack)-1])
            self.stack.pop(len(self.stack)-1)

        # print("output: " + str(self.output))
        # print("stack: " + str(self.stack))
        
        #convertir los ascii a su texto otra vez
        # for x in range(len(self.output)):
        #     if type(self.output[x]) == int:
        #          self.output[x] = chr(self.output[x])
        #enviar de regreso
        return self.output